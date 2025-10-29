# ventas/admin.py
"""
Configuración del Admin para la app 'ventas'.
"""
from django.contrib import admin
from .models import OrdenCompra, DetalleOrden

class DetalleOrdenInline(admin.TabularInline):
    """
    Define que los 'DetalleOrden' se puedan editar "en línea"
    dentro de la página de 'OrdenCompra'.
    """
    model = DetalleOrden
    extra = 1 # Muestra 1 fila vacía por defecto
    fields = ('producto', 'cantidad', 'precio_unitario')
    # 'autocomplete_fields' usa un widget de búsqueda en lugar de un <select>
    # (muy útil si tienes miles de productos).
    autocomplete_fields = ['producto'] 

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    """
    Personaliza la vista de 'OrdenCompra' en el admin.
    """
    # Columnas a mostrar en la lista
    list_display = ('numero_venta', 'cliente', 'fecha', 'total', 'rut')
    # Campos que se pueden usar en la barra de búsqueda
    search_fields = ('numero_venta', 'cliente', 'rut')
    # Filtros que aparecen en el panel derecho
    list_filter = ('fecha',)
    date_hierarchy = 'fecha' # Navegación por fechas tipo "drill-down"
    inlines = [DetalleOrdenInline] # Añade el editor en línea de detalles
    # Campos que no se pueden editar (se calculan automáticamente)
    readonly_fields = ('numero_venta', 'total')