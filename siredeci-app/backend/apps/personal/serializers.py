from rest_framework import serializers
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from apps.usuarios.models import Usuario
from apps.usuarios.utils import get_codigos_roles
from apps.personal.models import PersonalMunicipal


class LoginAdminSerializer(serializers.Serializer):
    """
    Serializer para el login de administradores (Personal Municipal)
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Buscar usuario por email
            try:
                usuario = Usuario.objects.get(email=email)
            except Usuario.DoesNotExist:
                raise serializers.ValidationError({
                    'error': 'Credenciales inválidas',
                    'message': 'El email o contraseña proporcionados son incorrectos.'
                })

            # Obtener roles del usuario
            codigos_roles = list(get_codigos_roles(usuario))

            es_admin_sistemico = any(r in ['ROL-001', 'ROL-002', 'ROL-006'] for r in codigos_roles)
            es_personal_municipal = any(r in ['ROL-003', 'ROL-004'] for r in codigos_roles)

            # Verificar estado de la cuenta del usuario
            if usuario.estado_cuenta != 'Activo':
                raise serializers.ValidationError({
                    'error': 'Cuenta inactiva',
                    'message': f'Su cuenta está {usuario.estado_cuenta.lower()}. Contacte al administrador.'
                })

            personal = None

            # Para roles operativos municipales sí es obligatorio tener PersonalMunicipal activo
            if es_personal_municipal:
                try:
                    personal = PersonalMunicipal.objects.get(id_usuario=usuario)
                except PersonalMunicipal.DoesNotExist:
                    raise serializers.ValidationError({
                        'error': 'Acceso no autorizado',
                        'message': 'Este usuario no tiene un registro de personal municipal asociado.'
                    })

                if personal.estado_laboral != 'Activo':
                    raise serializers.ValidationError({
                        'error': 'Personal inactivo',
                        'message': f'Su estado laboral es {personal.estado_laboral}. Contacte al administrador.'
                    })

            # Si no es ni admin sistémico ni personal municipal, no tiene acceso al panel interno
            if not es_admin_sistemico and not es_personal_municipal:
                raise serializers.ValidationError({
                    'error': 'Acceso no autorizado',
                    'message': 'Este usuario no tiene roles válidos para el panel administrativo.'
                })

            password_is_valid = False
            stored_hash = usuario.password_hash or ''

            # 1) Intentar validar con los hashers configurados en Django
            if stored_hash:
                password_is_valid = check_password(password, stored_hash)

            # 2) Compatibilidad con hashes legacy tipo bcrypt plano "$2b$..."
            if not password_is_valid and stored_hash.startswith('$2b$'):
                try:
                    import bcrypt

                    password_is_valid = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
                    if password_is_valid:
                        # Rehash con el hasher por defecto de Django para futuros logins
                        usuario.password_hash = make_password(password)
                except Exception:
                    password_is_valid = False

            # 3) Compatibilidad temporal con contraseñas en texto plano
            #    (caso de ambientes de desarrollo o scripts de carga inicial)
            if not password_is_valid and stored_hash and not stored_hash.startswith('$2b$'):
                if password == stored_hash:
                    password_is_valid = True

            if not password_is_valid:
                # Incrementar intentos de login fallidos
                usuario.intentos_login += 1
                if usuario.intentos_login >= 5:
                    usuario.estado_cuenta = 'Bloqueado'
                    usuario.fecha_bloqueo = timezone.now()
                usuario.save()

                raise serializers.ValidationError({
                    'error': 'Credenciales inválidas',
                    'message': 'El email o contraseña proporcionados son incorrectos.'
                })

            # Si la autenticación es exitosa, resetear intentos y actualizar último acceso
            usuario.intentos_login = 0
            usuario.ultimo_acceso = timezone.now()
            usuario.save()

            attrs['usuario'] = usuario
            attrs['personal'] = personal

            return attrs
        else:
            raise serializers.ValidationError({
                'error': 'Datos incompletos',
                'message': 'Debe proporcionar email y contraseña.'
            })


class PersonalMunicipalSerializer(serializers.ModelSerializer):
    """
    Serializer para información del Personal Municipal
    """
    area_responsable_nombre = serializers.CharField(
        source='id_area_responsable.nombre',
        read_only=True
    )

    class Meta:
        model = PersonalMunicipal
        fields = [
            'id_personal',
            'codigo_personal',
            'dni',
            'nombre',
            'apellido',
            'email',
            'cargo',
            'estado_laboral',
            'especialidad',
            'area_responsable_nombre'
        ]


class LoginAdminResponseSerializer(serializers.Serializer):
    """
    Serializer para la respuesta del login
    """
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = serializers.DictField()
    personal = PersonalMunicipalSerializer()

