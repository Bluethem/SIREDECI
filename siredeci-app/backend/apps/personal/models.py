from django.db import models
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
        verbose_name='Área Responsable'
    )
    id_usuario = models.OneToOneField(
        Usuario,
        on_delete=models.PROTECT,
        related_name='personal',
        verbose_name='Usuario'
    )
    
    class Meta:
        db_table = 'personal_municipal'
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
