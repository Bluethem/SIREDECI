from django.contrib import admin
from .models import Ciudadano, CiudadanoTelefono


class CiudadanoTelefonoInline(admin.TabularInline):
    model = CiudadanoTelefono
    extra = 1


@admin.register(Ciudadano)
class CiudadanoAdmin(admin.ModelAdmin):
    list_display = ['codigo_ciudadano', 'dni', 'nombre_completo', 'email', 'estado_cuenta', 'fecha_registro']
    list_filter = ['estado_cuenta', 'es_anonimo']
    search_fields = ['codigo_ciudadano', 'dni', 'nombre', 'apellido', 'email']
    readonly_fields = ['codigo_ciudadano', 'fecha_registro']
    inlines = [CiudadanoTelefonoInline]
    
    def nombre_completo(self, obj):
        return obj.nombre_completo
    nombre_completo.short_description = 'Nombre Completo'
