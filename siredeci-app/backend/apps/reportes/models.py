from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.usuarios.models import Usuario
from apps.categorias.models import AreaResponsable


class Reporte(models.Model):
    """
    Reportes generados por el sistema
    """
    
    TIPOS_REPORTE = [
        ('Ejecutivo', 'Ejecutivo'),
        ('Operativo', 'Operativo'),
        ('Estadístico', 'Estadístico'),
        ('Auditoria', 'Auditoria'),
    ]
    
    FORMATOS_EXPORTACION = [
        ('PDF', 'PDF'),
        ('Excel', 'Excel'),
        ('CSV', 'CSV'),
        ('JSON', 'JSON'),
    ]
    
    ESTADOS_GENERACION = [
        ('Borrador', 'Borrador'),
        ('En progreso', 'En progreso'),
        ('Completado', 'Completado'),
        ('Fallido', 'Fallido'),
    ]
    
    id_reporte = models.AutoField(primary_key=True)
    codigo_reporte = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Reporte'
    )
    tipo_reporte = models.CharField(
        max_length=50,
        choices=TIPOS_REPORTE,
        verbose_name='Tipo de Reporte'
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name='Nombre'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    fecha_generacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Generación'
    )
    fecha_inicio = models.DateField(
        verbose_name='Fecha de Inicio'
    )
    fecha_fin = models.DateField(
        verbose_name='Fecha de Fin'
    )
    formato_exportacion = models.CharField(
        max_length=10,
        choices=FORMATOS_EXPORTACION,
        verbose_name='Formato de Exportación'
    )
    ruta_archivo = models.CharField(
        max_length=500,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Ruta del Archivo'
    )
    es_publico = models.BooleanField(
        default=False,
        verbose_name='Es Público'
    )
    id_usuario_generador = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='reportes_generados',
        verbose_name='Usuario Generador',
        db_column='id_usuario_generador'
    )
    estado_generacion = models.CharField(
        max_length=20,
        choices=ESTADOS_GENERACION,
        default='Borrador',
        verbose_name='Estado de Generación'
    )
    parametros_configuracion = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Parámetros de Configuración'
    )
    
    class Meta:
        db_table = 'reporte'
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'
        indexes = [
            models.Index(fields=['tipo_reporte'], name='idx_reporte_tipo'),
            models.Index(fields=['fecha_generacion'], name='idx_reporte_fecha'),
        ]
        ordering = ['-fecha_generacion']
    
    def __str__(self):
        return f"{self.codigo_reporte} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_reporte:
            last_reporte = Reporte.objects.all().order_by('id_reporte').last()
            if last_reporte:
                new_id = last_reporte.id_reporte + 1
            else:
                new_id = 1
            self.codigo_reporte = f'RPT-{new_id:05d}'
        super().save(*args, **kwargs)
    
    def clean(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError('La fecha de fin debe ser posterior o igual a la fecha de inicio')


class Estadistica(models.Model):
    """
    Métricas y datos estadísticos del sistema (KPIs)
    """
    
    PERIODOS = [
        ('Diario', 'Diario'),
        ('Semanal', 'Semanal'),
        ('Mensual', 'Mensual'),
        ('Trimestral', 'Trimestral'),
        ('Anual', 'Anual'),
    ]
    
    id_estadistica = models.AutoField(primary_key=True)
    codigo_estadistica = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Estadística'
    )
    tipo_metrica = models.CharField(
        max_length=50,
        verbose_name='Tipo de Métrica'
    )
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor'
    )
    unidad_medida = models.CharField(
        max_length=20,
        verbose_name='Unidad de Medida'
    )
    periodo = models.CharField(
        max_length=20,
        choices=PERIODOS,
        verbose_name='Período'
    )
    fecha_calculo = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Cálculo'
    )
    categoria = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Categoría'
    )
    area = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Área'
    )
    zona = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Zona'
    )
    
    class Meta:
        db_table = 'estadistica'
        verbose_name = 'Estadística'
        verbose_name_plural = 'Estadísticas'
        indexes = [
            models.Index(fields=['tipo_metrica'], name='idx_estadistica_tipo_metrica'),
            models.Index(fields=['periodo'], name='idx_estadistica_periodo'),
            models.Index(fields=['fecha_calculo'], name='idx_estadistica_fecha'),
            models.Index(fields=['categoria'], name='idx_estadistica_categoria'),
        ]
        ordering = ['-fecha_calculo']
    
    def __str__(self):
        return f"{self.codigo_estadistica} - {self.tipo_metrica}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_estadistica:
            last_estadistica = Estadistica.objects.all().order_by('id_estadistica').last()
            if last_estadistica:
                new_id = last_estadistica.id_estadistica + 1
            else:
                new_id = 1
            self.codigo_estadistica = f'EST-{new_id:05d}'
        super().save(*args, **kwargs)


class Indicador(models.Model):
    """
    Indicador de desempeño o KPI del sistema
    """
    
    FRECUENCIAS = [
        ('Tiempo real', 'Tiempo real'),
        ('Diario', 'Diario'),
        ('Semanal', 'Semanal'),
        ('Mensual', 'Mensual'),
    ]
    
    TIPOS_VISUALIZACION = [
        ('Gauge', 'Gauge'),
        ('LineChart', 'LineChart'),
        ('BarChart', 'BarChart'),
        ('PieChart', 'PieChart'),
        ('Number', 'Number'),
    ]
    
    id_indicador = models.AutoField(primary_key=True)
    codigo_indicador = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Indicador'
    )
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre'
    )
    descripcion = models.TextField(
        verbose_name='Descripción'
    )
    formula = models.CharField(
        max_length=500,
        verbose_name='Fórmula'
    )
    valor_minimo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Valor Mínimo'
    )
    valor_maximo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Valor Máximo'
    )
    valor_actual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Valor Actual'
    )
    frecuencia_actualizacion = models.CharField(
        max_length=20,
        choices=FRECUENCIAS,
        verbose_name='Frecuencia de Actualización'
    )
    tipo_visualizacion = models.CharField(
        max_length=20,
        choices=TIPOS_VISUALIZACION,
        verbose_name='Tipo de Visualización'
    )
    
    class Meta:
        db_table = 'indicador'
        verbose_name = 'Indicador'
        verbose_name_plural = 'Indicadores'
        indexes = [
            models.Index(fields=['frecuencia_actualizacion'], name='idx_indicador_frecuencia'),
        ]
    
    def __str__(self):
        return f"{self.codigo_indicador} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_indicador:
            last_indicador = Indicador.objects.all().order_by('id_indicador').last()
            if last_indicador:
                new_id = last_indicador.id_indicador + 1
            else:
                new_id = 1
            self.codigo_indicador = f'IND-{new_id:05d}'
        super().save(*args, **kwargs)


class Dashboard(models.Model):
    """
    Panel de control con visualización de indicadores
    """
    
    TIPOS_DASHBOARD = [
        ('Ejecutivo', 'Ejecutivo'),
        ('Operativo', 'Operativo'),
        ('Ciudadano', 'Ciudadano'),
        ('Analítico', 'Analítico'),
    ]
    
    FRECUENCIAS = [
        ('Tiempo real', 'Tiempo real'),
        ('Diario', 'Diario'),
        ('Semanal', 'Semanal'),
    ]
    
    id_dashboard = models.AutoField(primary_key=True)
    codigo_dashboard = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Dashboard'
    )
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    tipo_dashboard = models.CharField(
        max_length=50,
        choices=TIPOS_DASHBOARD,
        verbose_name='Tipo de Dashboard'
    )
    frecuencia_actualizacion = models.CharField(
        max_length=20,
        choices=FRECUENCIAS,
        verbose_name='Frecuencia de Actualización'
    )
    es_publico = models.BooleanField(
        default=False,
        verbose_name='Es Público'
    )
    orden_visualizacion = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Orden de Visualización'
    )
    
    class Meta:
        db_table = 'dashboard'
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboards'
        indexes = [
            models.Index(fields=['tipo_dashboard'], name='idx_dashboard_tipo'),
            models.Index(fields=['es_publico'], name='idx_dashboard_publico'),
        ]
        ordering = ['orden_visualizacion', 'nombre']
    
    def __str__(self):
        return f"{self.codigo_dashboard} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_dashboard:
            last_dashboard = Dashboard.objects.all().order_by('id_dashboard').last()
            if last_dashboard:
                new_id = last_dashboard.id_dashboard + 1
            else:
                new_id = 1
            self.codigo_dashboard = f'DAS-{new_id:05d}'
        super().save(*args, **kwargs)


class DashboardIndicador(models.Model):
    """
    Relación entre dashboards e indicadores con configuración
    """
    
    TIPOS_VISUALIZACION = [
        ('Gauge', 'Gauge'),
        ('LineChart', 'LineChart'),
        ('BarChart', 'BarChart'),
        ('PieChart', 'PieChart'),
        ('Number', 'Number'),
    ]
    
    id_dashboard = models.ForeignKey(
        Dashboard,
        on_delete=models.CASCADE,
        related_name='indicadores_asignados',
        verbose_name='Dashboard',
        db_column='id_dashboard'
    )
    id_indicador = models.ForeignKey(
        Indicador,
        on_delete=models.CASCADE,
        related_name='dashboards_asignados',
        verbose_name='Indicador',
        db_column='id_indicador'
    )
    orden = models.IntegerField(
        verbose_name='Orden'
    )
    tipo_visualizacion = models.CharField(
        max_length=20,
        choices=TIPOS_VISUALIZACION,
        verbose_name='Tipo de Visualización'
    )
    fecha_asignacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Asignación'
    )
    
    class Meta:
        db_table = 'dashboardindicador'
        verbose_name = 'Dashboard Indicador'
        verbose_name_plural = 'Dashboard Indicadores'
        unique_together = ['id_dashboard', 'id_indicador']
        indexes = [
            models.Index(fields=['id_dashboard'], name='idx_dash_ind_dash'),
            models.Index(fields=['id_indicador'], name='idx_dash_ind_indicador'),
        ]
        ordering = ['orden']
    
    def __str__(self):
        return f"{self.id_dashboard.nombre} - {self.id_indicador.nombre}"
    
    def clean(self):
        if self.orden <= 0:
            raise ValidationError('El orden debe ser mayor a cero')


class TendenciaGeografica(models.Model):
    """
    Análisis de tendencias geográficas de denuncias
    """
    
    PERIODOS = [
        ('Diario', 'Diario'),
        ('Semanal', 'Semanal'),
        ('Mensual', 'Mensual'),
        ('Trimestral', 'Trimestral'),
        ('Anual', 'Anual'),
    ]
    
    NIVELES_CRITICIDAD = [
        ('Bajo', 'Bajo'),
        ('Medio', 'Medio'),
        ('Alto', 'Alto'),
        ('Crítico', 'Crítico'),
    ]
    
    id_tendencia = models.AutoField(primary_key=True)
    codigo_tendencia = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Tendencia'
    )
    zona = models.CharField(
        max_length=100,
        verbose_name='Zona'
    )
    distrito = models.CharField(
        max_length=100,
        verbose_name='Distrito'
    )
    cantidad_denuncias = models.IntegerField(
        verbose_name='Cantidad de Denuncias'
    )
    categoria_mas_frecuente = models.CharField(
        max_length=100,
        verbose_name='Categoría Más Frecuente'
    )
    tasa_resolucion = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Tasa de Resolución (%)'
    )
    tiempo_promedio_atencion = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Tiempo Promedio de Atención'
    )
    periodo_analisis = models.CharField(
        max_length=20,
        choices=PERIODOS,
        verbose_name='Período de Análisis'
    )
    nivel_criticidad = models.CharField(
        max_length=20,
        choices=NIVELES_CRITICIDAD,
        verbose_name='Nivel de Criticidad'
    )
    
    class Meta:
        db_table = 'tendenciageografica'
        verbose_name = 'Tendencia Geográfica'
        verbose_name_plural = 'Tendencias Geográficas'
        indexes = [
            models.Index(fields=['zona'], name='idx_tendencia_zona'),
            models.Index(fields=['distrito'], name='idx_tendencia_distrito'),
            models.Index(fields=['periodo_analisis'], name='idx_tendencia_periodo'),
        ]
    
    def __str__(self):
        return f"{self.codigo_tendencia} - {self.distrito}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_tendencia:
            last_tendencia = TendenciaGeografica.objects.all().order_by('id_tendencia').last()
            if last_tendencia:
                new_id = last_tendencia.id_tendencia + 1
            else:
                new_id = 1
            self.codigo_tendencia = f'TEN-{new_id:05d}'
        super().save(*args, **kwargs)
    
    def clean(self):
        if self.cantidad_denuncias < 0:
            raise ValidationError('La cantidad de denuncias debe ser mayor o igual a cero')
        if not (0 <= self.tasa_resolucion <= 100):
            raise ValidationError('La tasa de resolución debe estar entre 0 y 100')
        if self.tiempo_promedio_atencion < 0:
            raise ValidationError('El tiempo promedio de atención debe ser mayor o igual a cero')


class RankingDesempeno(models.Model):
    """
    Ranking de desempeño por área responsable
    """
    
    PERIODOS = [
        ('Diario', 'Diario'),
        ('Semanal', 'Semanal'),
        ('Mensual', 'Mensual'),
        ('Trimestral', 'Trimestral'),
        ('Anual', 'Anual'),
    ]
    
    id_ranking = models.AutoField(primary_key=True)
    codigo_ranking = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código de Ranking'
    )
    periodo_evaluacion = models.CharField(
        max_length=20,
        choices=PERIODOS,
        verbose_name='Período de Evaluación'
    )
    posicion = models.IntegerField(
        verbose_name='Posición'
    )
    puntaje_total = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Puntaje Total'
    )
    denuncias_atendidas = models.IntegerField(
        verbose_name='Denuncias Atendidas'
    )
    tasa_resolucion_area = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Tasa de Resolución del Área (%)'
    )
    tiempo_promedio_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Tiempo Promedio del Área'
    )
    calificacion_promedio = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Calificación Promedio'
    )
    id_area_responsable = models.ForeignKey(
        AreaResponsable,
        on_delete=models.PROTECT,
        related_name='rankings',
        verbose_name='Área Responsable',
        db_column='id_area_responsable'
    )
    
    class Meta:
        db_table = 'rankingdesempeno'
        verbose_name = 'Ranking de Desempeño'
        verbose_name_plural = 'Rankings de Desempeño'
        unique_together = ['id_area_responsable', 'periodo_evaluacion']
        indexes = [
            models.Index(fields=['periodo_evaluacion'], name='idx_ranking_periodo'),
        ]
        ordering = ['posicion']
    
    def __str__(self):
        return f"{self.codigo_ranking} - {self.id_area_responsable.nombre}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_ranking:
            last_ranking = RankingDesempeno.objects.all().order_by('id_ranking').last()
            if last_ranking:
                new_id = last_ranking.id_ranking + 1
            else:
                new_id = 1
            self.codigo_ranking = f'RAN-{new_id:05d}'
        super().save(*args, **kwargs)
    
    def clean(self):
        if self.posicion <= 0:
            raise ValidationError('La posición debe ser mayor a cero')
        if not (0 <= self.puntaje_total <= 100):
            raise ValidationError('El puntaje total debe estar entre 0 y 100')
        if not (0 <= self.tasa_resolucion_area <= 100):
            raise ValidationError('La tasa de resolución del área debe estar entre 0 y 100')
        if self.calificacion_promedio and not (0 <= self.calificacion_promedio <= 5):
            raise ValidationError('La calificación promedio debe estar entre 0 y 5')
