from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import RegexValidator, EmailValidator
from apps.usuarios.models import Usuario
from apps.categorias.models import AreaResponsable


class PersonalMunicipal(models.Model):
    """
    Modelo de Personal Municipal
    Empleados del municipio que gestionan las denuncias
    """
    
    ESTADOS_LABORALES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Vacaciones', 'Vacaciones'),
        ('Licencia', 'Licencia'),
        ('Desvinculado', 'Desvinculado'),
    ]
    
    dni_validator = RegexValidator(
        regex=r'^\d{8}$',
        message='El DNI debe tener exactamente 8 dígitos numéricos'
    )
    
    id_personal = models.AutoField(primary_key=True)
    codigo_personal = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Personal'
    )
    dni = models.CharField(
        max_length=8,
        unique=True,
        validators=[dni_validator],
        verbose_name='DNI'
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre'
    )
    apellido = models.CharField(
        max_length=100,
        verbose_name='Apellido'
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        validators=[EmailValidator()],
        verbose_name='Correo Electrónico'
    )
    cargo = models.CharField(
        max_length=100,
        verbose_name='Cargo'
    )
    fecha_ingreso = models.DateField(
        verbose_name='Fecha de Ingreso'
    )
    estado_laboral = models.CharField(
        max_length=20,
        choices=ESTADOS_LABORALES,
        default='Activo',
        verbose_name='Estado Laboral'
    )
    especialidad = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Especialidad'
    )
    id_area_responsable = models.ForeignKey(
        AreaResponsable,
        on_delete=models.PROTECT,
        related_name='personal',
        verbose_name='Área Responsable',
        db_column='id_area_responsable'
    )
    id_usuario = models.OneToOneField(
        Usuario,
        on_delete=models.PROTECT,
        related_name='personal',
        verbose_name='Usuario',
        db_column='id_usuario'
    )
    
    class Meta:
        db_table = 'personalmunicipal'
        verbose_name = 'Personal Municipal'
        verbose_name_plural = 'Personal Municipal'
        indexes = [
            models.Index(fields=['id_area_responsable'], name='idx_personal_area'),
            models.Index(fields=['estado_laboral'], name='idx_personal_estado'),
        ]
    
    def __str__(self):
        return f"{self.codigo_personal} - {self.nombre} {self.apellido}"
    
    def save(self, *args, **kwargs):
        # Generar código de personal si no existe
        if not self.codigo_personal:
            last_personal = PersonalMunicipal.objects.all().order_by('id_personal').last()
            if last_personal:
                new_id = last_personal.id_personal + 1
            else:
                new_id = 1
            self.codigo_personal = f'PER-{new_id:05d}'
        super().save(*args, **kwargs)


class PersonalTelefono(models.Model):
    """
    Números de teléfono asociados al personal municipal
    """
    
    telefono_validator = RegexValidator(
        regex=r'^[0-9+\-\s()]{7,20}$',
        message='El teléfono debe tener entre 7 y 20 caracteres y solo puede contener números, +, -, espacios y paréntesis'
    )
    
    id_personal_telefono = models.AutoField(primary_key=True)
    id_personal = models.ForeignKey(
        PersonalMunicipal,
        on_delete=models.CASCADE,
        related_name='telefonos',
        verbose_name='Personal',
        db_column='id_personal'
    )
    telefono = models.CharField(
        max_length=20,
        validators=[telefono_validator],
        verbose_name='Teléfono'
    )
    es_principal = models.BooleanField(
        default=True,
        verbose_name='Es Principal'
    )
    
    class Meta:
        db_table = 'personaltelefono'
        verbose_name = 'Teléfono de Personal'
        verbose_name_plural = 'Teléfonos de Personal'
        unique_together = ['id_personal', 'telefono']
        indexes = [
            models.Index(fields=['id_personal'], name='idx_personal_telefono_personal'),
        ]
    
    def __str__(self):
        return f"{self.id_personal.nombre} - {self.telefono}"


class Asignacion(models.Model):
    """
    Asignación de denuncia a personal municipal
    """
    
    id_asignacion = models.AutoField(primary_key=True)
    codigo_asignacion = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Asignación'
    )
    fecha_asignacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Asignación'
    )
    motivo_asignacion = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Motivo de Asignación'
    )
    es_activa = models.BooleanField(
        default=True,
        verbose_name='Está Activa'
    )
    fecha_finalizacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Finalización'
    )
    id_denuncia = models.ForeignKey(
        'denuncias.Denuncia',
        on_delete=models.PROTECT,
        related_name='asignaciones',
        verbose_name='Denuncia',
        db_column='id_denuncia'
    )
    id_personal_asignado = models.ForeignKey(
        PersonalMunicipal,
        on_delete=models.PROTECT,
        related_name='asignaciones_recibidas',
        verbose_name='Personal Asignado',
        db_column='id_personal_asignado'
    )
    id_personal_asignador = models.ForeignKey(
        PersonalMunicipal,
        on_delete=models.PROTECT,
        related_name='asignaciones_realizadas',
        verbose_name='Personal Asignador',
        db_column='id_personal_asignador'
    )
    
    class Meta:
        db_table = 'asignacion'
        verbose_name = 'Asignación'
        verbose_name_plural = 'Asignaciones'
        indexes = [
            models.Index(fields=['id_denuncia'], name='idx_asignacion_denuncia'),
            models.Index(fields=['es_activa'], name='idx_asignacion_activa'),
            models.Index(fields=['id_personal_asignado'], name='idx_asignacion_personal'),
        ]
    
    def __str__(self):
        return f"{self.codigo_asignacion} - {self.id_denuncia.codigo_denuncia}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_asignacion:
            last_asignacion = Asignacion.objects.all().order_by('id_asignacion').last()
            if last_asignacion:
                new_id = last_asignacion.id_asignacion + 1
            else:
                new_id = 1
            self.codigo_asignacion = f'ASG-{new_id:05d}'
        super().save(*args, **kwargs)
    
    def clean(self):
        if self.fecha_finalizacion and self.fecha_finalizacion <= self.fecha_asignacion:
            raise ValidationError('La fecha de finalización debe ser posterior a la fecha de asignación')


class Tramitacion(models.Model):
    """
    Proceso de gestión y resolución de una denuncia
    """
    
    ESTADOS = [
        ('En proceso', 'En proceso'),
        ('Finalizado', 'Finalizado'),
        ('Suspendido', 'Suspendido'),
        ('Cancelado', 'Cancelado'),
    ]
    
    id_tramitacion = models.AutoField(primary_key=True)
    codigo_tramitacion = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Tramitación'
    )
    fecha_inicio = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Inicio'
    )
    fecha_finalizacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Finalización'
    )
    accion_realizada = models.TextField(
        verbose_name='Acción Realizada'
    )
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    costo_estimado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Costo Estimado'
    )
    estado_tramitacion = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='En proceso',
        verbose_name='Estado de Tramitación'
    )
    id_asignacion = models.OneToOneField(
        Asignacion,
        on_delete=models.PROTECT,
        related_name='tramitacion',
        verbose_name='Asignación',
        db_column='id_asignacion'
    )
    
    class Meta:
        db_table = 'tramitacion'
        verbose_name = 'Tramitación'
        verbose_name_plural = 'Tramitaciones'
        indexes = [
            models.Index(fields=['estado_tramitacion'], name='idx_tramitacion_estado'),
        ]
    
    def __str__(self):
        return f"{self.codigo_tramitacion} - {self.estado_tramitacion}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_tramitacion:
            last_tramitacion = Tramitacion.objects.all().order_by('id_tramitacion').last()
            if last_tramitacion:
                new_id = last_tramitacion.id_tramitacion + 1
            else:
                new_id = 1
            self.codigo_tramitacion = f'TRM-{new_id:05d}'
        super().save(*args, **kwargs)
    
    def clean(self):
        if self.fecha_finalizacion and self.fecha_finalizacion <= self.fecha_inicio:
            raise ValidationError('La fecha de finalización debe ser posterior a la fecha de inicio')
        if self.costo_estimado and self.costo_estimado < 0:
            raise ValidationError('El costo estimado debe ser positivo o cero')
