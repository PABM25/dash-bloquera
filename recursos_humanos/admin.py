# recursos_humanos/admin.py
"""
Configuración del Admin para la app 'recursos_humanos'.
"""
from django.contrib import admin
from .models import Trabajador, Asistencia

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    """Personaliza la vista de 'Trabajador'."""
    list_display = ('nombre', 'rut', 'telefono', 'email', 'tipo_proyecto', 'cargo', 'salario_por_dia')
    search_fields = ('nombre', 'rut')
    list_filter = ('tipo_proyecto', 'cargo')

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    """Personaliza la vista de 'Asistencia'."""
    list_display = ('trabajador', 'fecha', 'tipo_proyecto')
    list_filter = ('fecha', 'tipo_proyecto', 'trabajador')
    date_hierarchy = 'fecha'