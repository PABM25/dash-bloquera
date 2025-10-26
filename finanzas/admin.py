# finanzas/admin.py
from django.contrib import admin
from .models import Gasto

@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'categoria', 'monto', 'tipo_proyecto', 'descripcion_corta') # Usar descripción corta
    list_filter = ('fecha', 'categoria', 'tipo_proyecto')
    search_fields = ('descripcion', 'monto') # Buscar en descripción
    date_hierarchy = 'fecha' # Navegación por fecha

    # Método para mostrar solo una parte de la descripción en la lista
    def descripcion_corta(self, obj):
        return (obj.descripcion[:75] + '...') if len(obj.descripcion) > 75 else obj.descripcion
    descripcion_corta.short_description = 'Descripción' # Nombre de la columna