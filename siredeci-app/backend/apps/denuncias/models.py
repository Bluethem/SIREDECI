from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.ciudadanos.models import Ciudadano
from apps.categorias.models import Categoria
from apps.usuarios.models import Usuario
import uuid


class Ubicacion(models.Model):
    """
    Modelo de Ubicación
    Información geográfica de la denuncia
    """
    
    id_ubicacion = models.AutoField(primary_key=True)
    codigo_ubicacion = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Ubicación'
    )
    latitud = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        verbose_name='Latitud'
    )
    longitud = models.DecimalField(
        max_digits=11,
        decimal_places=8,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        verbose_name='Longitud'
    )
    direccion = models.CharField(
        max_length=200,
        verbose_name='Dirección'
    )
    referencia = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Referencia'
    )
    distrito = models.CharField(
        max_length=100,
        verbose_name='Distrito'
    )
    codigo_postal = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name='Código Postal'
    )
    
    class Meta:
        db_table = 'ubicacion'
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'
        indexes = [
            models.Index(fields=['distrito'], name='idx_ubicacion_distrito'),
            models.Index(fields=['latitud', 'longitud'], name='idx_ubicacion_coordenadas'),
        ]
    
    def __str__(self):
        return f"{self.codigo_ubicacion} - {self.direccion}"
    
    def save(self, *args, **kwargs):
        # Generar código de ubicación si no existe
        if not self.codigo_ubicacion:
            last_ubicacion = Ubicacion.objects.all().order_by('id_ubicacion').last()
            if last_ubicacion:
                new_id = last_ubicacion.id_ubicacion + 1
            else:
                new_id = 1
            self.codigo_ubicacion = f'UBI-{new_id:05d}'
        super().save(*args, **kwargs)


class Denuncia(models.Model):
    """
    Modelo de Denuncia
    Registro de un problema o incidencia reportado por un ciudadano
    """
    
    ESTADOS = [
        ('Registrado', 'Registrado'),
        ('En revisión', 'En revisión'),
        ('Asignado', 'Asignado'),
        ('En proceso', 'En proceso'),
        ('Resuelta', 'Resuelta'),
        ('Rechazada', 'Rechazada'),
        ('Cerrada', 'Cerrada'),
    ]
    
    PRIORIDADES = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
        ('Urgente', 'Urgente'),
    ]
    
    id_denuncia = models.AutoField(primary_key=True)
    codigo_denuncia = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Denuncia'
    )
    titulo = models.CharField(
        max_length=100,
        verbose_name='Título'
    )
    descripcion = models.TextField(
        verbose_name='Descripción'
    )
    fecha_registro = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha de Registro'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Actualización'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='Registrado',
        verbose_name='Estado'
    )
    prioridad = models.CharField(
        max_length=20,
        choices=PRIORIDADES,
        default='Media',
        verbose_name='Prioridad'
    )
    es_anonima = models.BooleanField(
        default=False,
        verbose_name='Es Anónima'
    )
    numero_seguimiento = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Seguimiento'
    )
    requiere_validacion = models.BooleanField(
        default=True,
        verbose_name='Requiere Validación'
    )
    id_ciudadano = models.ForeignKey(
        Ciudadano,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='denuncias',
        verbose_name='Ciudadano',
        db_column='id_ciudadano'
    )
    id_categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='denuncias',
        verbose_name='Categoría',
        db_column='id_categoria'
    )
    id_ubicacion = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        related_name='denuncias',
        verbose_name='Ubicación',
        db_column='id_ubicacion'
    )
    
    class Meta:
        db_table = 'denuncia'
        verbose_name = 'Denuncia'
        verbose_name_plural = 'Denuncias'
        indexes = [
            models.Index(fields=['estado'], name='idx_denuncia_estado'),
            models.Index(fields=['prioridad'], name='idx_denuncia_prioridad'),
            models.Index(fields=['fecha_registro'], name='idx_denuncia_fecha_registro'),
            models.Index(fields=['id_ciudadano'], name='idx_denuncia_ciudadano'),
            models.Index(fields=['id_categoria'], name='idx_denuncia_categoria'),
        ]
    
    def __str__(self):
        return f"{self.codigo_denuncia} - {self.titulo}"
    
    def save(self, *args, **kwargs):
        # Generar código de denuncia si no existe
        if not self.codigo_denuncia:
            year = timezone.now().year
            last_denuncia = Denuncia.objects.filter(
                fecha_registro__year=year
            ).order_by('id_denuncia').last()
            
            if last_denuncia:
                # Extraer el número del último código
                last_number = int(last_denuncia.codigo_denuncia.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.codigo_denuncia = f'DEN-{year}-{new_number:05d}'
        
        # Generar número de seguimiento si no existe
        if not self.numero_seguimiento:
            self.numero_seguimiento = f'SEG-{uuid.uuid4().hex[:10].upper()}'
        
        super().save(*args, **kwargs)


class Evidencia(models.Model):
    """
    Modelo de Evidencia
    Archivos multimedia adjuntos a una denuncia
    """
    
    TIPOS_ARCHIVO = [
        ('image/jpeg', 'JPEG'),
        ('image/png', 'PNG'),
        ('image/gif', 'GIF'),
        ('video/mp4', 'MP4'),
        ('application/pdf', 'PDF'),
    ]
    
    id_evidencia = models.AutoField(primary_key=True)
    codigo_evidencia = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Evidencia'
    )
    nombre_archivo = models.CharField(
        max_length=255,
        verbose_name='Nombre del Archivo'
    )
    ruta_almacenamiento = models.CharField(
        max_length=500,
        unique=True,
        verbose_name='Ruta de Almacenamiento'
    )
    tipo_archivo = models.CharField(
        max_length=100,
        choices=TIPOS_ARCHIVO,
        verbose_name='Tipo de Archivo'
    )
    tamaño_bytes = models.BigIntegerField(
        verbose_name='Tamaño en Bytes'
    )
    fecha_carga = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha de Carga'
    )
    hash_archivo = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Hash del Archivo (SHA-256)'
    )
    esta_escaneado = models.BooleanField(
        default=False,
        verbose_name='Está Escaneado'
    )
    id_denuncia = models.ForeignKey(
        Denuncia,
        on_delete=models.CASCADE,
        related_name='evidencias',
        verbose_name='Denuncia',
        db_column='id_denuncia'
    )
    
    class Meta:
        db_table = 'evidencia'
        verbose_name = 'Evidencia'
        verbose_name_plural = 'Evidencias'
        indexes = [
            models.Index(fields=['id_denuncia'], name='idx_evidencia_denuncia'),
            models.Index(fields=['tipo_archivo'], name='idx_evidencia_tipo'),
        ]
    
    def __str__(self):
        return f"{self.codigo_evidencia} - {self.nombre_archivo}"
    
    def save(self, *args, **kwargs):
        # Generar código de evidencia si no existe
        if not self.codigo_evidencia:
            last_evidencia = Evidencia.objects.all().order_by('id_evidencia').last()
            if last_evidencia:
                new_id = last_evidencia.id_evidencia + 1
            else:
                new_id = 1
            self.codigo_evidencia = f'EVI-{new_id:05d}'
        super().save(*args, **kwargs)


class Seguimiento(models.Model):
    """
    Modelo de Seguimiento
    Registro de cambios de estado y actualizaciones de la denuncia
    """
    
    ESTADOS = [
        ('Registrado', 'Registrado'),
        ('En revisión', 'En revisión'),
        ('Asignado', 'Asignado'),
        ('En proceso', 'En proceso'),
        ('Resuelta', 'Resuelta'),
        ('Rechazada', 'Rechazada'),
        ('Cerrada', 'Cerrada'),
    ]
    
    id_seguimiento = models.AutoField(primary_key=True)
    codigo_seguimiento = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Seguimiento'
    )
    estado_anterior = models.CharField(
        max_length=20,
        choices=ESTADOS,
        null=True,
        blank=True,
        verbose_name='Estado Anterior'
    )
    estado_nuevo = models.CharField(
        max_length=20,
        choices=ESTADOS,
        verbose_name='Estado Nuevo'
    )
    fecha_hora = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha y Hora'
    )
    comentario = models.TextField(
        null=True,
        blank=True,
        verbose_name='Comentario'
    )
    es_visible = models.BooleanField(
        default=True,
        verbose_name='Es Visible para el Ciudadano'
    )
    id_denuncia = models.ForeignKey(
        Denuncia,
        on_delete=models.CASCADE,
        related_name='seguimientos',
        verbose_name='Denuncia',
        db_column='id_denuncia'
    )
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='seguimientos',
        verbose_name='Usuario',
        db_column='id_usuario'
    )
    
    class Meta:
        db_table = 'seguimiento'
        verbose_name = 'Seguimiento'
        verbose_name_plural = 'Seguimientos'
        indexes = [
            models.Index(fields=['id_denuncia'], name='idx_seguimiento_denuncia'),
            models.Index(fields=['fecha_hora'], name='idx_seguimiento_fecha'),
        ]
        ordering = ['-fecha_hora']
    
    def __str__(self):
        return f"{self.codigo_seguimiento} - {self.estado_nuevo}"
    
    def save(self, *args, **kwargs):
        # Generar código de seguimiento si no existe
        if not self.codigo_seguimiento:
            last_seguimiento = Seguimiento.objects.all().order_by('id_seguimiento').last()
            if last_seguimiento:
                new_id = last_seguimiento.id_seguimiento + 1
            else:
                new_id = 1
            self.codigo_seguimiento = f'SEG-{new_id:05d}'
        super().save(*args, **kwargs)


class EvidenciaResolucion(models.Model):
    """
    Evidencias fotográficas de la resolución
    """
    
    TIPOS_ARCHIVO = [
        ('image/jpeg', 'JPEG'),
        ('image/png', 'PNG'),
        ('application/pdf', 'PDF'),
    ]
    
    id_evidencia_resolucion = models.AutoField(primary_key=True)
    nombre_archivo = models.CharField(
        max_length=255,
        verbose_name='Nombre del Archivo'
    )
    ruta_almacenamiento = models.CharField(
        max_length=500,
        unique=True,
        verbose_name='Ruta de Almacenamiento'
    )
    tipo_archivo = models.CharField(
        max_length=100,
        choices=TIPOS_ARCHIVO,
        verbose_name='Tipo de Archivo'
    )
    tamaño_bytes = models.BigIntegerField(
        verbose_name='Tamaño en Bytes'
    )
    fecha_carga = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Carga'
    )
    hash_archivo = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Hash del Archivo (SHA-256)'
    )
    id_tramitacion = models.ForeignKey(
        'personal.Tramitacion',
        on_delete=models.CASCADE,
        related_name='evidencias_resolucion',
        verbose_name='Tramitación'
    )
    
    class Meta:
        db_table = 'evidenciaresolucion'
        verbose_name = 'Evidencia de Resolución'
        verbose_name_plural = 'Evidencias de Resolución'
        indexes = [
            models.Index(fields=['id_tramitacion'], name='idx_ev_res_tramitacion'),
        ]
    
    def __str__(self):
        return f"{self.nombre_archivo}"
    
    def clean(self):
        if self.tamaño_bytes <= 0:
            raise ValidationError('El tamaño del archivo debe ser mayor a cero')


class Resolucion(models.Model):
    """
    Resultado final de la atención de una denuncia
    """
    
    TIPOS = [
        ('Resuelta', 'Resuelta'),
        ('Rechazada', 'Rechazada'),
        ('Duplicada', 'Duplicada'),
        ('No procede', 'No procede'),
    ]
    
    id_resolucion = models.AutoField(primary_key=True)
    codigo_resolucion = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Resolución'
    )
    fecha_resolucion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Resolución'
    )
    tipo_resolucion = models.CharField(
        max_length=20,
        choices=TIPOS,
        verbose_name='Tipo de Resolución'
    )
    descripcion_resolucion = models.TextField(
        verbose_name='Descripción de la Resolución'
    )
    tiempo_total_horas = models.IntegerField(
        verbose_name='Tiempo Total en Horas'
    )
    calificacion_ciudadano = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Calificación del Ciudadano (1-5)'
    )
    comentario_ciudadano = models.TextField(
        null=True,
        blank=True,
        verbose_name='Comentario del Ciudadano'
    )
    id_tramitacion = models.ForeignKey(
        'personal.Tramitacion',
        on_delete=models.CASCADE,
        related_name='resoluciones',
        verbose_name='Tramitación',
        db_column='id_tramitacion'
    )
    
    class Meta:
        db_table = 'resolucion'
        verbose_name = 'Resolución'
        verbose_name_plural = 'Resoluciones'
        indexes = [
            models.Index(fields=['tipo_resolucion'], name='idx_resolucion_tipo'),
            models.Index(fields=['fecha_resolucion'], name='idx_resolucion_fecha'),
        ]
    
    def __str__(self):
        return f"{self.codigo_resolucion} - {self.tipo_resolucion}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_resolucion:
            last_resolucion = Resolucion.objects.all().order_by('id_resolucion').last()
            if last_resolucion:
                new_id = last_resolucion.id_resolucion + 1
            else:
                new_id = 1
            self.codigo_resolucion = f'RES-{new_id:05d}'
        super().save(*args, **kwargs)
    
    def clean(self):
        if self.tiempo_total_horas <= 0:
            raise ValidationError('El tiempo total debe ser mayor a cero')
        if self.calificacion_ciudadano and not (1 <= self.calificacion_ciudadano <= 5):
            raise ValidationError('La calificación debe estar entre 1 y 5')
