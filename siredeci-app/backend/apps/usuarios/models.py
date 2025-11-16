from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator, EmailValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


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
        
        # Hash de la contraseña manualmente
        if password:
            from django.contrib.auth.hashers import make_password
            user.password_hash = make_password(password)
            
        user.save(using=self._db)
        return user
    
    def create_superuser(self, nombre_usuario, email, password=None, **extra_fields):
        """Crea y guarda un superusuario"""
        # Eliminar campos no compatibles con nuestro modelo
        extra_fields.pop('is_staff', None)
        extra_fields.pop('is_superuser', None)
        
        return self.create_user(nombre_usuario, email, password, **extra_fields)


class Usuario(models.Model):
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
    password_hash = models.CharField(
        max_length=255,
        default='',
        verbose_name='Hash de Contraseña'
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
    
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_authenticated(self):
        return True
    
    def save(self, *args, **kwargs):
        # Auto-generar código de usuario si no existe
        if not self.codigo_usuario:
            last_user = Usuario.objects.all().order_by('id_usuario').last()
            new_id = last_user.id_usuario + 1 if last_user else 1
            self.codigo_usuario = f'USR-{new_id:05d}'
            
        super().save(*args, **kwargs)


class Rol(models.Model):
    """
    Rol de usuario en el sistema con permisos específicos (RBAC)
    """
    
    id_rol = models.AutoField(primary_key=True)
    codigo_rol = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Rol'
    )
    nombre = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Nombre del Rol'
    )
    descripcion = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Descripción'
    )
    nivel = models.PositiveIntegerField(
        verbose_name='Nivel del Rol'
    )
    es_sistema = models.BooleanField(
        default=True,
        verbose_name='Es Rol de Sistema'
    )
    esta_activo = models.BooleanField(
        default=True,
        verbose_name='Está Activo'
    )
    
    class Meta:
        db_table = 'rol'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        indexes = [
            models.Index(fields=['esta_activo'], name='idx_rol_activo'),
            models.Index(fields=['nivel'], name='idx_rol_nivel'),
        ]
    
    def __str__(self):
        return f"{self.codigo_rol} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_rol:
            last_rol = Rol.objects.all().order_by('id_rol').last()
            if last_rol:
                new_id = last_rol.id_rol + 1
            else:
                new_id = 1
            self.codigo_rol = f'ROL-{new_id:05d}'
        super().save(*args, **kwargs)


class Permiso(models.Model):
    """
    Permiso específico para realizar acciones en el sistema
    """
    
    ACCIONES = [
        ('Crear', 'Crear'),
        ('Leer', 'Leer'),
        ('Actualizar', 'Actualizar'),
        ('Eliminar', 'Eliminar'),
        ('Ejecutar', 'Ejecutar'),
    ]
    
    id_permiso = models.AutoField(primary_key=True)
    codigo_permiso = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Permiso'
    )
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre del Permiso'
    )
    descripcion = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Descripción'
    )
    modulo = models.CharField(
        max_length=50,
        verbose_name='Módulo'
    )
    accion = models.CharField(
        max_length=50,
        choices=ACCIONES,
        verbose_name='Acción'
    )
    recurso = models.CharField(
        max_length=50,
        verbose_name='Recurso'
    )
    
    class Meta:
        db_table = 'permiso'
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'
        indexes = [
            models.Index(fields=['modulo'], name='idx_permiso_modulo'),
            models.Index(fields=['accion'], name='idx_permiso_accion'),
        ]
    
    def __str__(self):
        return f"{self.codigo_permiso} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_permiso:
            last_permiso = Permiso.objects.all().order_by('id_permiso').last()
            if last_permiso:
                new_id = last_permiso.id_permiso + 1
            else:
                new_id = 1
            self.codigo_permiso = f'PER-{new_id:05d}'
        super().save(*args, **kwargs)


class UsuarioRol(models.Model):
    """
    Relación entre usuarios y roles (N:M)
    """
    
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        verbose_name='Usuario',
        db_column='id_usuario'
    )
    id_rol = models.ForeignKey(
        Rol,
        on_delete=models.CASCADE,
        verbose_name='Rol',
        db_column='id_rol'
    )
    fecha_asignacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Asignación'
    )
    es_activo = models.BooleanField(
        default=True,
        verbose_name='Está Activo'
    )
    
    class Meta:
        db_table = 'usuariorol'
        verbose_name = 'Usuario Rol'
        verbose_name_plural = 'Usuarios Roles'
        unique_together = ['id_usuario', 'id_rol']
        indexes = [
            models.Index(fields=['id_usuario'], name='idx_usuario_rol_usuario'),
            models.Index(fields=['id_rol'], name='idx_usuario_rol_rol'),
        ]
    
    def __str__(self):
        return f"{self.id_usuario.nombre_usuario} - {self.id_rol.nombre}"


class RolPermiso(models.Model):
    """
    Relación entre roles y permisos (N:M)
    """
    
    id_rol = models.ForeignKey(
        Rol,
        on_delete=models.CASCADE,
        verbose_name='Rol',
        db_column='id_rol'
    )
    id_permiso = models.ForeignKey(
        Permiso,
        on_delete=models.CASCADE,
        verbose_name='Permiso',
        db_column='id_permiso'
    )
    fecha_asignacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Asignación'
    )
    
    class Meta:
        db_table = 'rolpermiso'
        verbose_name = 'Rol Permiso'
        verbose_name_plural = 'Roles Permisos'
        unique_together = ['id_rol', 'id_permiso']
        indexes = [
            models.Index(fields=['id_rol'], name='idx_rol_permiso_rol'),
            models.Index(fields=['id_permiso'], name='idx_rol_permiso_permiso'),
        ]
    
    def __str__(self):
        return f"{self.id_rol.nombre} - {self.id_permiso.nombre}"


class Sesion(models.Model):
    """
    Sesión de usuario en el sistema
    """
    
    id_sesion = models.AutoField(primary_key=True)
    codigo_sesion = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Sesión'
    )
    token = models.CharField(
        max_length=500,
        unique=True,
        verbose_name='Token de Sesión'
    )
    fecha_inicio = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Inicio'
    )
    fecha_expiracion = models.DateTimeField(
        verbose_name='Fecha de Expiración'
    )
    direccion_ip = models.GenericIPAddressField(
        verbose_name='Dirección IP'
    )
    user_agent = models.TextField(
        max_length=500,
        verbose_name='User Agent'
    )
    esta_activa = models.BooleanField(
        default=True,
        verbose_name='Está Activa'
    )
    ultima_actividad = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actividad'
    )
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        verbose_name='Usuario'
    )
    
    class Meta:
        db_table = 'sesion'
        verbose_name = 'Sesión'
        verbose_name_plural = 'Sesiones'
        indexes = [
            models.Index(fields=['esta_activa'], name='idx_sesion_activa'),
            models.Index(fields=['id_usuario'], name='idx_sesion_usuario'),
            models.Index(fields=['fecha_expiracion'], name='idx_sesion_expiracion'),
        ]
    
    def __str__(self):
        return f"{self.codigo_sesion} - {self.id_usuario.nombre_usuario}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_sesion:
            last_sesion = Sesion.objects.all().order_by('id_sesion').last()
            if last_sesion:
                new_id = last_sesion.id_sesion + 1
            else:
                new_id = 1
            self.codigo_sesion = f'SES-{new_id:05d}'
        super().save(*args, **kwargs)
    
    def clean(self):
        if self.fecha_expiracion <= self.fecha_inicio:
            raise ValidationError('La fecha de expiración debe ser posterior a la fecha de inicio')


class LogAuditoria(models.Model):
    """
    Registro de auditoría del sistema
    """
    
    RESULTADOS = [
        ('Exitoso', 'Exitoso'),
        ('Fallido', 'Fallido'),
        ('Advertencia', 'Advertencia'),
    ]
    
    id_log = models.AutoField(primary_key=True)
    codigo_log = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Log'
    )
    tipo_accion = models.CharField(
        max_length=50,
        verbose_name='Tipo de Acción'
    )
    modulo = models.CharField(
        max_length=50,
        verbose_name='Módulo'
    )
    entidad = models.CharField(
        max_length=50,
        verbose_name='Entidad'
    )
    entidad_id = models.CharField(
        max_length=36,
        verbose_name='ID de Entidad'
    )
    fecha_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha y Hora'
    )
    direccion_ip = models.GenericIPAddressField(
        verbose_name='Dirección IP'
    )
    datos_antes = models.TextField(
        blank=True,
        verbose_name='Datos Antes'
    )
    datos_despues = models.TextField(
        blank=True,
        verbose_name='Datos Después'
    )
    resultado = models.CharField(
        max_length=20,
        choices=RESULTADOS,
        verbose_name='Resultado'
    )
    mensaje_error = models.TextField(
        blank=True,
        verbose_name='Mensaje de Error'
    )
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.DO_NOTHING,
        verbose_name='Usuario'
    )
    
    class Meta:
        db_table = 'logauditoria'
        verbose_name = 'Log de Auditoría'
        verbose_name_plural = 'Logs de Auditoría'
        indexes = [
            models.Index(fields=['fecha_hora'], name='idx_log_fecha'),
            models.Index(fields=['modulo'], name='idx_log_modulo'),
            models.Index(fields=['id_usuario'], name='idx_log_usuario'),
            models.Index(fields=['tipo_accion'], name='idx_log_tipo_accion'),
            models.Index(fields=['entidad', 'entidad_id'], name='idx_log_entidad'),
        ]
    
    def __str__(self):
        return f"{self.codigo_log} - {self.tipo_accion} en {self.modulo}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_log:
            last_log = LogAuditoria.objects.all().order_by('id_log').last()
            if last_log:
                new_id = last_log.id_log + 1
            else:
                new_id = 1
            self.codigo_log = f'LOG-{new_id:05d}'
        super().save(*args, **kwargs)
