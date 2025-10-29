# finanzas/admin.py
"""
Configuración del Admin para la app 'finanzas'.
"""
from django.contrib import admin
from .models import Gasto

@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    """Personaliza la vista de 'Gasto'."""
    list_display = ('fecha', 'categoria', 'monto', 'tipo_proyecto', 'descripcion_corta')
    list_filter = ('fecha', 'categoria', 'tipo_proyecto')
    search_fields = ('descripcion', 'monto')
    date_hierarchy = 'fecha'

    def descripcion_corta(self, obj):
        """
        Un método personalizado para mostrar solo los primeros 75
        caracteres de la descripción en la lista del admin.
        """
        return (obj.descripcion[:75] + '...') if len(obj.descripcion) > 75 else obj.descripcion
    descripcion_corta.short_description = 'Descripción' # Nombre de la columna