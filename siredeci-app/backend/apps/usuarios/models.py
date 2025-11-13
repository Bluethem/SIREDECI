from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator, EmailValidator
from django.utils import timezone


class UsuarioManager(BaseUserManager):
    """Manager personalizado para el modelo Usuario"""
    
    def create_user(self, nombre_usuario, email, password=None, **extra_fields):
        """Crea y guarda un usuario regular"""
        if not email:
            raise ValueError('El email es obligatorio')
        if not nombre_usuario:
            raise ValueError('El nombre de usuario es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(
            nombre_usuario=nombre_usuario,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, nombre_usuario, email, password=None, **extra_fields):
        """Crea y guarda un superusuario"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(nombre_usuario, email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de Usuario del sistema
    Entidad general que representa cualquier usuario del sistema
    """
    
    ESTADOS_CUENTA = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Suspendido', 'Suspendido'),
        ('Bloqueado', 'Bloqueado'),
    ]
    
    id_usuario = models.AutoField(primary_key=True)
    codigo_usuario = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Usuario'
    )
    nombre_usuario = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Nombre de Usuario'
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        validators=[EmailValidator()],
        verbose_name='Correo Electrónico'
    )
    fecha_creacion = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha de Creación'
    )
    ultimo_acceso = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Último Acceso'
    )
    estado_cuenta = models.CharField(
        max_length=20,
        choices=ESTADOS_CUENTA,
        default='Activo',
        verbose_name='Estado de Cuenta'
    )
    intentos_login = models.IntegerField(
        default=0,
        verbose_name='Intentos de Login Fallidos'
    )
    fecha_bloqueo = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Bloqueo'
    )
    requiere_mfa = models.BooleanField(
        default=False,
        verbose_name='Requiere Autenticación Multifactor'
    )
    token_mfa = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Token MFA'
    )
    
    # Campos requeridos por Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'nombre_usuario'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        indexes = [
            models.Index(fields=['estado_cuenta'], name='idx_usuario_estado'),
            models.Index(fields=['ultimo_acceso'], name='idx_usuario_ultimo_acceso'),
        ]
    
    def __str__(self):
        return f"{self.codigo_usuario} - {self.nombre_usuario}"
    
    def save(self, *args, **kwargs):
        # Generar código de usuario si no existe
        if not self.codigo_usuario:
            last_user = Usuario.objects.all().order_by('id_usuario').last()
            if last_user:
                new_id = last_user.id_usuario + 1
            else:
                new_id = 1
            self.codigo_usuario = f'USU-{new_id:05d}'
        super().save(*args, **kwargs)
