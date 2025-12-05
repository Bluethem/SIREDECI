from rest_framework import serializers
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import hashlib
from .models import Denuncia, Ubicacion, Evidencia, Seguimiento
from apps.categorias.models import Categoria
from apps.ciudadanos.models import Ciudadano


class UbicacionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Ubicacion"""
    
    # Hacer que algunos campos sean opcionales en el serializer
    referencia = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    codigo_postal = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    class Meta:
        model = Ubicacion
        fields = [
            'id_ubicacion', 'codigo_ubicacion', 'latitud', 'longitud',
            'direccion', 'referencia', 'distrito', 'codigo_postal'
        ]
        read_only_fields = ['id_ubicacion', 'codigo_ubicacion']


class EvidenciaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Evidencia"""
    
    class Meta:
        model = Evidencia
        fields = [
            'id_evidencia', 'codigo_evidencia', 'nombre_archivo',
            'ruta_almacenamiento', 'tipo_archivo', 'tamaño_bytes',
            'fecha_carga'
        ]
        read_only_fields = ['id_evidencia', 'codigo_evidencia', 'fecha_carga']


class SeguimientoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Seguimiento (historial de la denuncia)"""

    class Meta:
        model = Seguimiento
        fields = [
            'id_seguimiento', 'codigo_seguimiento', 'estado_anterior', 'estado_nuevo',
            'fecha_hora', 'comentario', 'es_visible'
        ]
        read_only_fields = ['id_seguimiento', 'codigo_seguimiento', 'fecha_hora']


class DenunciaListSerializer(serializers.ModelSerializer):
    """Serializer para listar denuncias (vista resumida)"""
    
    categoria_nombre = serializers.CharField(source='id_categoria.nombre', read_only=True)
    categoria_codigo = serializers.CharField(source='id_categoria.codigo_categoria', read_only=True)
    distrito = serializers.CharField(source='id_ubicacion.distrito', read_only=True)
    direccion = serializers.CharField(source='id_ubicacion.direccion', read_only=True)
    
    class Meta:
        model = Denuncia
        fields = [
            'id_denuncia', 'codigo_denuncia', 'titulo', 'descripcion',
            'fecha_registro', 'fecha_actualizacion', 'estado', 'prioridad',
            'numero_seguimiento', 'categoria_nombre', 'categoria_codigo',
            'distrito', 'direccion'
        ]


class DenunciaDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalle de denuncia (vista completa)"""
    
    ubicacion = UbicacionSerializer(source='id_ubicacion', read_only=True)
    evidencias = EvidenciaSerializer(many=True, read_only=True)
    seguimientos = SeguimientoSerializer(many=True, read_only=True)
    categoria = serializers.SerializerMethodField()
    ciudadano = serializers.SerializerMethodField()
    
    class Meta:
        model = Denuncia
        fields = [
            'id_denuncia', 'codigo_denuncia', 'titulo', 'descripcion',
            'fecha_registro', 'fecha_actualizacion', 'estado', 'prioridad',
            'es_anonima', 'numero_seguimiento', 'requiere_validacion',
            'categoria', 'ubicacion', 'evidencias', 'seguimientos', 'ciudadano'
        ]
    
    def get_categoria(self, obj):
        if obj.id_categoria:
            return {
                'id': obj.id_categoria.id_categoria,
                'codigo': obj.id_categoria.codigo_categoria,
                'nombre': obj.id_categoria.nombre,
                'icono': obj.id_categoria.icono if hasattr(obj.id_categoria, 'icono') else None
            }
        return None
    
    def get_ciudadano(self, obj):
        if obj.id_ciudadano and not obj.es_anonima:
            return {
                'id': obj.id_ciudadano.id_ciudadano,
                'nombre': obj.id_ciudadano.nombre,
                'apellido': obj.id_ciudadano.apellido,
                'email': obj.id_ciudadano.email
            }
        return None


class DenunciaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear denuncias"""
    
    # Nested serializers para crear ubicación y evidencias en la misma request
    ubicacion = UbicacionSerializer(write_only=True)
    evidencias_data = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False,
        allow_empty=True
    )
    
    # Read-only fields para la respuesta
    codigo_denuncia = serializers.CharField(read_only=True)
    numero_seguimiento = serializers.CharField(read_only=True)
    fecha_registro = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Denuncia
        fields = [
            'titulo', 'descripcion', 'id_categoria', 'id_ciudadano',
            'es_anonima', 'prioridad', 'ubicacion', 'evidencias_data',
            'codigo_denuncia', 'numero_seguimiento', 'fecha_registro',
            'id_denuncia'
        ]
    
    def validate(self, data):
        """Validaciones personalizadas"""
        # Si no es anónima, debe tener ciudadano
        if not data.get('es_anonima', False) and not data.get('id_ciudadano'):
            raise serializers.ValidationError({
                'id_ciudadano': 'Se requiere un ciudadano para denuncias no anónimas'
            })
        
        # Si es anónima, no debe tener ciudadano
        if data.get('es_anonima', False):
            data['id_ciudadano'] = None
        
        return data
    
    def create(self, validated_data):
        """Crear denuncia con ubicación y evidencias"""
        
        # Extraer datos nested
        ubicacion_data = validated_data.pop('ubicacion')
        evidencias_files = validated_data.pop('evidencias_data', [])
        
        # Crear ubicación
        ubicacion = Ubicacion.objects.create(**ubicacion_data)
        
        # Crear denuncia
        validated_data['id_ubicacion'] = ubicacion
        denuncia = Denuncia.objects.create(**validated_data)
        
        # Crear evidencias si existen
        for evidencia_file in evidencias_files:
            # Construir ruta base para la denuncia
            relative_path = f'evidencias/{denuncia.codigo_denuncia}/{evidencia_file.name}'

            # Calcular hash del archivo (SHA-256)
            file_bytes = evidencia_file.read()
            sha256_hash = hashlib.sha256(file_bytes).hexdigest()

            # Si ya existe una evidencia con este hash, omitir para evitar duplicados
            if Evidencia.objects.filter(hash_archivo=sha256_hash).exists():
                continue

            # Guardar archivo en el storage usando el contenido leído
            saved_path = default_storage.save(relative_path, ContentFile(file_bytes))

            # Crear registro de Evidencia
            Evidencia.objects.create(
                nombre_archivo=evidencia_file.name,
                ruta_almacenamiento=saved_path,
                tipo_archivo=getattr(evidencia_file, 'content_type', ''),
                tamaño_bytes=len(file_bytes),
                hash_archivo=sha256_hash,
                id_denuncia=denuncia
            )

        return denuncia


class DenunciaUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar denuncias (solo campos permitidos)"""
    
    class Meta:
        model = Denuncia
        fields = ['estado', 'prioridad']
    
    def validate_estado(self, value):
        """Validar transiciones de estado permitidas"""
        instance = self.instance
        if instance:
            # Definir transiciones válidas
            transiciones_validas = {
                # Desde registrado permitimos pasar a revisión, asignado o rechazado
                'Registrado': ['En revisión', 'Asignado', 'Rechazada'],
                'En revisión': ['Asignado', 'Rechazada'],
                'Asignado': ['En proceso', 'Rechazada'],
                # Desde "En proceso" se permite pasar a "Resuelta", "Rechazada" o cerrar directamente
                'En proceso': ['Resuelta', 'Rechazada', 'Cerrada'],
                'Resuelta': ['Cerrada'],
                'Rechazada': [],
                'Cerrada': []
            }
            
            if instance.estado in ['Resuelta', 'Cerrada', 'Rechazada']:
                raise serializers.ValidationError(
                    f'No se puede cambiar el estado de una denuncia {instance.estado}'
                )
            
            if value not in transiciones_validas.get(instance.estado, []):
                raise serializers.ValidationError(
                    f'No se puede cambiar de {instance.estado} a {value}'
                )
        
        return value
