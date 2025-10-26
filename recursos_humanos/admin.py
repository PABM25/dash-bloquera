# recursos_humanos/admin.py
from django.contrib import admin
from .models import Trabajador, Asistencia

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'telefono', 'email', 'tipo_proyecto', 'cargo', 'salario_por_dia') # Añadido salario
    search_fields = ('nombre', 'rut')
    list_filter = ('tipo_proyecto', 'cargo') # Añadido filtro por cargo

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'fecha', 'tipo_proyecto')
    list_filter = ('fecha', 'tipo_proyecto', 'trabajador') # Añadido filtro por trabajador
    date_hierarchy = 'fecha' # Para navegar por fechas