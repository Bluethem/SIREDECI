from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['codigo_usuario', 'nombre_usuario', 'email', 'estado_cuenta', 'fecha_creacion']
    list_filter = ['estado_cuenta', 'requiere_mfa']
    search_fields = ['codigo_usuario', 'nombre_usuario', 'email']
    readonly_fields = ['codigo_usuario', 'fecha_creacion', 'ultimo_acceso']
