from django.contrib import admin
from .models import PersonalMunicipal


@admin.register(PersonalMunicipal)
class PersonalMunicipalAdmin(admin.ModelAdmin):
    list_display = ['codigo_personal', 'dni', 'nombre', 'apellido', 'cargo', 'id_area_responsable', 'estado_laboral']
    list_filter = ['estado_laboral', 'id_area_responsable']
    search_fields = ['codigo_personal', 'dni', 'nombre', 'apellido', 'email']
    readonly_fields = ['codigo_personal']
