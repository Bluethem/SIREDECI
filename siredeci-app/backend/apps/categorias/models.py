from django.db import models
from django.core.validators import RegexValidator, EmailValidator


class AreaResponsable(models.Model):
    """
    Modelo de Área Responsable
    Departamentos o áreas del municipio responsables de atender denuncias
    """
    
    color_validator = RegexValidator(
        regex=r'^#[0-9A-Fa-f]{6}$',
        message='El color debe ser un código hexadecimal válido (ej: #FF5733)'
    )
    
    id_area_responsable = models.AutoField(primary_key=True)
    codigo_area = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Área'
    )
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre'
    )
    descripcion = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='Descripción'
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        validators=[EmailValidator()],
        verbose_name='Correo Electrónico'
    )
    telefono = models.CharField(
        max_length=20,
        verbose_name='Teléfono'
    )
    capacidad_maxima = models.IntegerField(
        default=50,
        verbose_name='Capacidad Máxima'
    )
    esta_activo = models.BooleanField(
        default=True,
        verbose_name='Está Activo'
    )
    id_jefe_area = models.ForeignKey(
        'personal.PersonalMunicipal',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='areas_a_cargo',
        verbose_name='Jefe de Área'
    )
    
    class Meta:
        db_table = 'area_responsable'
        verbose_name = 'Área Responsable'
        verbose_name_plural = 'Áreas Responsables'
        indexes = [
            models.Index(fields=['nombre'], name='idx_area_nombre'),
            models.Index(fields=['esta_activo'], name='idx_area_activo'),
        ]
    
    def __str__(self):
        return f"{self.codigo_area} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        # Generar código de área si no existe
        if not self.codigo_area:
            last_area = AreaResponsable.objects.all().order_by('id_area_responsable').last()
            if last_area:
                new_id = last_area.id_area_responsable + 1
            else:
                new_id = 1
            self.codigo_area = f'ARE-{new_id:03d}'
        super().save(*args, **kwargs)


class Categoria(models.Model):
    """
    Modelo de Categoría
    Clasificación temática de las denuncias
    """
    
    color_validator = RegexValidator(
        regex=r'^#[0-9A-Fa-f]{6}$',
        message='El color debe ser un código hexadecimal válido (ej: #FF5733)'
    )
    
    id_categoria = models.AutoField(primary_key=True)
    codigo_categoria = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Categoría'
    )
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre'
    )
    descripcion = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='Descripción'
    )
    color = models.CharField(
        max_length=7,
        null=True,
        blank=True,
        validators=[color_validator],
        verbose_name='Color'
    )
    icono = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Icono'
    )
    esta_activo = models.BooleanField(
        default=True,
        verbose_name='Está Activo'
    )
    tiempo_respuesta_promedio = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Tiempo Respuesta Promedio (horas)'
    )
    id_area_responsable = models.ForeignKey(
        AreaResponsable,
        on_delete=models.PROTECT,
        related_name='categorias',
        verbose_name='Área Responsable'
    )
    
    class Meta:
        db_table = 'categoria'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        indexes = [
            models.Index(fields=['esta_activo'], name='idx_categoria_activo'),
            models.Index(fields=['id_area_responsable'], name='idx_categoria_area'),
        ]
    
    def __str__(self):
        return f"{self.codigo_categoria} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        # Generar código de categoría si no existe
        if not self.codigo_categoria:
            last_categoria = Categoria.objects.all().order_by('id_categoria').last()
            if last_categoria:
                new_id = last_categoria.id_categoria + 1
            else:
                new_id = 1
            self.codigo_categoria = f'CAT-{new_id:03d}'
        super().save(*args, **kwargs)
