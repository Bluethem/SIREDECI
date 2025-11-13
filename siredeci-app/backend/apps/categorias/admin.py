from django.contrib import admin
from .models import AreaResponsable, Categoria


@admin.register(AreaResponsable)
class AreaResponsableAdmin(admin.ModelAdmin):
    list_display = ['codigo_area', 'nombre', 'email', 'telefono', 'capacidad_maxima', 'esta_activo']
    list_filter = ['esta_activo']
    search_fields = ['codigo_area', 'nombre', 'email']
    readonly_fields = ['codigo_area']


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['codigo_categoria', 'nombre', 'id_area_responsable', 'tiempo_respuesta_promedio', 'esta_activo']
    list_filter = ['esta_activo', 'id_area_responsable']
    search_fields = ['codigo_categoria', 'nombre']
    readonly_fields = ['codigo_categoria']
