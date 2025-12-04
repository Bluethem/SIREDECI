from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.usuarios.models import Usuario
from apps.denuncias.models import Denuncia


class Comunicacion(models.Model):
    """
    Mensajes intercambiados entre personal y ciudadanos
    """
    
    TIPOS_REMITENTE = [
        ('Ciudadano', 'Ciudadano'),
        ('Personal', 'Personal'),
        ('Sistema', 'Sistema'),
    ]
    
    id_comunicacion = models.AutoField(primary_key=True)
    codigo_comunicacion = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Comunicación'
    )
    mensaje = models.TextField(
        verbose_name='Mensaje'
    )
    fecha_envio = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Envío'
    )
    tipo_remitente = models.CharField(
        max_length=20,
        choices=TIPOS_REMITENTE,
        verbose_name='Tipo de Remitente'
    )
    es_leido = models.BooleanField(
        default=False,
        verbose_name='Es Leído'
    )
    requiere_respuesta = models.BooleanField(
        default=False,
        verbose_name='Requiere Respuesta'
    )
    id_denuncia = models.ForeignKey(
        Denuncia,
        on_delete=models.CASCADE,
        related_name='comunicaciones',
        verbose_name='Denuncia'
    )
    id_usuario_remitente = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='comunicaciones_enviadas',
        verbose_name='Usuario Remitente'
    )
    
    class Meta:
        db_table = 'comunicacion'
        verbose_name = 'Comunicación'
        verbose_name_plural = 'Comunicaciones'
        indexes = [
            models.Index(fields=['id_denuncia'], name='idx_comunicacion_denuncia'),
            models.Index(fields=['fecha_envio'], name='idx_comunicacion_fecha'),
            models.Index(fields=['es_leido'], name='idx_comunicacion_leido'),
        ]
        ordering = ['-fecha_envio']
    
    def __str__(self):
        return f"{self.codigo_comunicacion} - {self.tipo_remitente}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_comunicacion:
            last_comunicacion = Comunicacion.objects.all().order_by('id_comunicacion').last()
            if last_comunicacion:
                new_id = last_comunicacion.id_comunicacion + 1
            else:
                new_id = 1
            self.codigo_comunicacion = f'COM-{new_id:05d}'
        super().save(*args, **kwargs)


class PlantillaNotificacion(models.Model):
    """
    Plantilla predefinida para generar notificaciones
    """
    
    TIPOS_EVENTO = [
        ('Registro', 'Registro'),
        ('Actualización', 'Actualización'),
        ('Asignación', 'Asignación'),
        ('Resolución', 'Resolución'),
        ('Rechazo', 'Rechazo'),
        ('Comentario', 'Comentario'),
    ]
    
    id_plantilla = models.AutoField(primary_key=True)
    codigo_plantilla = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Plantilla'
    )
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre'
    )
    tipo_evento = models.CharField(
        max_length=50,
        choices=TIPOS_EVENTO,
        verbose_name='Tipo de Evento'
    )
    asunto = models.CharField(
        max_length=200,
        verbose_name='Asunto'
    )
    cuerpo_mensaje = models.TextField(
        verbose_name='Cuerpo del Mensaje'
    )
    variables = models.TextField(
        blank=True,
        help_text='Variables disponibles en formato JSON',
        verbose_name='Variables'
    )
    esta_activa = models.BooleanField(
        default=True,
        verbose_name='Está Activa'
    )
    
    class Meta:
        db_table = 'plantillanotificacion'
        verbose_name = 'Plantilla de Notificación'
        verbose_name_plural = 'Plantillas de Notificación'
        indexes = [
            models.Index(fields=['tipo_evento'], name='idx_plantilla_tipo_evento'),
            models.Index(fields=['esta_activa'], name='idx_plantilla_activa'),
        ]
    
    def __str__(self):
        return f"{self.codigo_plantilla} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_plantilla:
            last_plantilla = PlantillaNotificacion.objects.all().order_by('id_plantilla').last()
            if last_plantilla:
                new_id = last_plantilla.id_plantilla + 1
            else:
                new_id = 1
            self.codigo_plantilla = f'PLA-{new_id:05d}'
        super().save(*args, **kwargs)


class Notificacion(models.Model):
    """
    Notificaciones generadas para usuarios
    """
    
    CANALES_ENVIO = [
        ('Email', 'Email'),
        ('SMS', 'SMS'),
        ('Push', 'Push'),
        ('Interno', 'Interno'),
    ]
    
    ESTADOS_ENVIO = [
        ('Pendiente', 'Pendiente'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
        ('Fallido', 'Fallido'),
        ('Leído', 'Leído'),
    ]
    
    id_notificacion = models.AutoField(primary_key=True)
    codigo_notificacion = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Notificación'
    )
    tipo_notificacion = models.CharField(
        max_length=50,
        verbose_name='Tipo de Notificación'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    fecha_envio = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Envío'
    )
    canal_envio = models.CharField(
        max_length=20,
        choices=CANALES_ENVIO,
        verbose_name='Canal de Envío'
    )
    estado_envio = models.CharField(
        max_length=20,
        choices=ESTADOS_ENVIO,
        default='Pendiente',
        verbose_name='Estado de Envío'
    )
    mensaje_personalizado = models.TextField(
        verbose_name='Mensaje Personalizado'
    )
    intento_envio = models.IntegerField(
        default=1,
        verbose_name='Intento de Envío'
    )
    id_denuncia = models.ForeignKey(
        Denuncia,
        on_delete=models.CASCADE,
        related_name='notificaciones',
        verbose_name='Denuncia',
        db_column='id_denuncia'
    )
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='notificaciones',
        verbose_name='Usuario',
        db_column='id_usuario'
    )
    id_plantilla = models.ForeignKey(
        PlantillaNotificacion,
        on_delete=models.PROTECT,
        related_name='notificaciones',
        verbose_name='Plantilla',
        db_column='id_plantilla'
    )
    
    class Meta:
        db_table = 'notificacion'
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        indexes = [
            models.Index(fields=['id_usuario'], name='idx_notificacion_usuario'),
            models.Index(fields=['estado_envio'], name='idx_notificacion_estado'),
            models.Index(fields=['fecha_creacion'], name='idx_notificacion_fecha'),
        ]
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.codigo_notificacion} - {self.tipo_notificacion}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_notificacion:
            last_notificacion = Notificacion.objects.all().order_by('id_notificacion').last()
            if last_notificacion:
                new_id = last_notificacion.id_notificacion + 1
            else:
                new_id = 1
            self.codigo_notificacion = f'NOT-{new_id:05d}'
        super().save(*args, **kwargs)
    
    def clean(self):
        if self.intento_envio <= 0:
            raise ValidationError('El intento de envío debe ser mayor a cero')


class ConfiguracionNotificacion(models.Model):
    """
    Preferencias de notificación por usuario
    """
    
    FRECUENCIAS = [
        ('Inmediato', 'Inmediato'),
        ('Diario', 'Diario'),
        ('Semanal', 'Semanal'),
        ('Ninguno', 'Ninguno'),
    ]
    
    id_configuracion = models.AutoField(primary_key=True)
    codigo_configuracion = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Configuración'
    )
    recibir_email = models.BooleanField(
        default=True,
        verbose_name='Recibir Email'
    )
    recibir_sms = models.BooleanField(
        default=False,
        verbose_name='Recibir SMS'
    )
    recibir_push = models.BooleanField(
        default=True,
        verbose_name='Recibir Push'
    )
    frecuencia_resumen = models.CharField(
        max_length=20,
        choices=FRECUENCIAS,
        default='Diario',
        verbose_name='Frecuencia de Resumen'
    )
    horario_preferido = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Horario Preferido'
    )
    id_usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='configuracion_notificacion',
        verbose_name='Usuario',
        db_column='id_usuario'
    )
    
    class Meta:
        db_table = 'configuracionnotificacion'
        verbose_name = 'Configuración de Notificación'
        verbose_name_plural = 'Configuraciones de Notificación'
    
    def __str__(self):
        return f"Configuración - {self.id_usuario.nombre_usuario}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_configuracion:
            last_config = ConfiguracionNotificacion.objects.all().order_by('id_configuracion').last()
            if last_config:
                new_id = last_config.id_configuracion + 1
            else:
                new_id = 1
            self.codigo_configuracion = f'CFG-{new_id:05d}'
        super().save(*args, **kwargs)
