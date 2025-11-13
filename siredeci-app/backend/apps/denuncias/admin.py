from django.contrib import admin
from .models import Denuncia, Ubicacion, Evidencia, Seguimiento


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ['codigo_ubicacion', 'direccion', 'distrito', 'latitud', 'longitud']
    list_filter = ['distrito']
    search_fields = ['codigo_ubicacion', 'direccion', 'distrito']
    readonly_fields = ['codigo_ubicacion']


class EvidenciaInline(admin.TabularInline):
    model = Evidencia
    extra = 0
    readonly_fields = ['codigo_evidencia', 'hash_archivo', 'fecha_carga']


class SeguimientoInline(admin.TabularInline):
    model = Seguimiento
    extra = 0
    readonly_fields = ['codigo_seguimiento', 'fecha_hora']


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ['codigo_denuncia', 'titulo', 'estado', 'prioridad', 'id_categoria', 'fecha_registro']
    list_filter = ['estado', 'prioridad', 'es_anonima', 'id_categoria']
    search_fields = ['codigo_denuncia', 'titulo', 'numero_seguimiento']
    readonly_fields = ['codigo_denuncia', 'numero_seguimiento', 'fecha_registro', 'fecha_actualizacion']
    inlines = [EvidenciaInline, SeguimientoInline]


@admin.register(Evidencia)
class EvidenciaAdmin(admin.ModelAdmin):
    list_display = ['codigo_evidencia', 'nombre_archivo', 'tipo_archivo', 'tamaño_bytes', 'esta_escaneado', 'fecha_carga']
    list_filter = ['tipo_archivo', 'esta_escaneado']
    search_fields = ['codigo_evidencia', 'nombre_archivo']
    readonly_fields = ['codigo_evidencia', 'hash_archivo', 'fecha_carga']


@admin.register(Seguimiento)
class SeguimientoAdmin(admin.ModelAdmin):
    list_display = ['codigo_seguimiento', 'id_denuncia', 'estado_anterior', 'estado_nuevo', 'fecha_hora', 'es_visible']
    list_filter = ['estado_nuevo', 'es_visible']
    search_fields = ['codigo_seguimiento']
    readonly_fields = ['codigo_seguimiento', 'fecha_hora']
