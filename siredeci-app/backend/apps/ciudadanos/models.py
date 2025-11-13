from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.utils import timezone
from apps.usuarios.models import Usuario


class Ciudadano(models.Model):
    """
    Modelo de Ciudadano
    Registra la información de los ciudadanos que realizan denuncias
    """
    
    ESTADOS_CUENTA = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Suspendido', 'Suspendido'),
    ]
    
    dni_validator = RegexValidator(
        regex=r'^\d{8}$',
        message='El DNI debe tener exactamente 8 dígitos numéricos'
    )
    
    id_ciudadano = models.AutoField(primary_key=True)
    codigo_ciudadano = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Ciudadano'
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
        null=True,
        blank=True,
        validators=[EmailValidator()],
        verbose_name='Correo Electrónico'
    )
    direccion = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Dirección'
    )
    fecha_emision_dni = models.DateField(
        verbose_name='Fecha de Emisión del DNI'
    )
    fecha_registro = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha de Registro'
    )
    es_anonimo = models.BooleanField(
        default=False,
        verbose_name='Es Anónimo'
    )
    estado_cuenta = models.CharField(
        max_length=20,
        choices=ESTADOS_CUENTA,
        default='Activo',
        verbose_name='Estado de Cuenta'
    )
    id_usuario = models.OneToOneField(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ciudadano',
        verbose_name='Usuario'
    )
    
    class Meta:
        db_table = 'ciudadano'
        verbose_name = 'Ciudadano'
        verbose_name_plural = 'Ciudadanos'
        indexes = [
            models.Index(fields=['dni'], name='idx_ciudadano_dni'),
            models.Index(fields=['estado_cuenta'], name='idx_ciudadano_estado'),
        ]
    
    def __str__(self):
        return f"{self.codigo_ciudadano} - {self.nombre} {self.apellido}"
    
    def save(self, *args, **kwargs):
        # Generar código de ciudadano si no existe
        if not self.codigo_ciudadano:
            last_ciudadano = Ciudadano.objects.all().order_by('id_ciudadano').last()
            if last_ciudadano:
                new_id = last_ciudadano.id_ciudadano + 1
            else:
                new_id = 1
            self.codigo_ciudadano = f'CIU-{new_id:05d}'
        super().save(*args, **kwargs)
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del ciudadano"""
        return f"{self.nombre} {self.apellido}"


class CiudadanoTelefono(models.Model):
    """
    Modelo de Teléfonos del Ciudadano
    Números de teléfono asociados a ciudadanos (multivaluado)
    """
    
    telefono_validator = RegexValidator(
        regex=r'^[0-9+\-\s()]{7,20}$',
        message='El teléfono debe tener entre 7 y 20 caracteres y solo puede contener números, +, -, espacios y paréntesis'
    )
    
    id_ciudadano_telefono = models.AutoField(primary_key=True)
    id_ciudadano = models.ForeignKey(
        Ciudadano,
        on_delete=models.CASCADE,
        related_name='telefonos',
        verbose_name='Ciudadano'
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
        db_table = 'ciudadano_telefono'
        verbose_name = 'Teléfono de Ciudadano'
        verbose_name_plural = 'Teléfonos de Ciudadanos'
        unique_together = [['id_ciudadano', 'telefono']]
        indexes = [
            models.Index(fields=['id_ciudadano'], name='idx_ciud_tel_ciudadano'),
        ]
    
    def __str__(self):
        return f"{self.telefono} ({'Principal' if self.es_principal else 'Secundario'})"
