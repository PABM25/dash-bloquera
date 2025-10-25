from django.contrib import admin
from .models import OrdenCompra, Trabajador, Asistencia, Producto, Gasto

# Configuración del panel de administración para el modelo OrdenCompra
@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista del admin
    list_display = ('numero_venta', 'cliente', 'fecha', 'producto', 'cantidad', 'precio_unitario', 'total', 'rut')

    # Campos por los que se puede buscar
    search_fields = ('numero_venta', 'cliente', 'producto__nombre')  # Permite buscar por el nombre del producto
    
    # Campos por los que se puede filtrar
    list_filter = ('fecha', 'producto')  # Filtro por fecha y producto

# Configuración del panel de administración para el modelo Trabajador
@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'telefono', 'email', 'tipo_proyecto', 'cargo')
    search_fields = ('nombre', 'rut')

# Configuración del panel de administración para el modelo Asistencia
@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    # Ahora solo mostramos los campos que existen en el modelo
    list_display = ('trabajador', 'fecha', 'tipo_proyecto')
    list_filter = ('fecha', 'tipo_proyecto')
    
# Configuración del panel de administración para el modelo Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'stock', 'descripcion')
    search_fields = ('nombre',)
    list_editable = ('stock',) # Permite editar el stock directamente desde la lista
    
# Configuración del panel de administración para el modelo Gasto
@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    # Añadimos 'tipo_proyecto' a la lista para una mejor visualización
    list_display = ('fecha', 'categoria', 'monto', 'tipo_proyecto', 'descripcion')
    list_filter = ('fecha', 'categoria', 'tipo_proyecto')
