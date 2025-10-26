from django.contrib import admin
# Asegúrate de importar DetalleOrden
from .models import OrdenCompra, Trabajador, Asistencia, Producto, Gasto, DetalleOrden

# --- NUEVO ---
# Esto define cómo se mostrarán los productos DENTRO de la orden de compra
class DetalleOrdenInline(admin.TabularInline):
    model = DetalleOrden
    extra = 1  # Cuántas filas vacías mostrar
    fields = ('producto', 'cantidad', 'precio_unitario')
    readonly_fields = () # Puedes añadir campos aquí si no quieres que se editen

# Configuración del panel de administración para el modelo OrdenCompra (ACTUALIZADO)
@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista del admin (Quitamos los campos viejos)
    list_display = ('numero_venta', 'cliente', 'fecha', 'total', 'rut')

    # Campos por los que se puede buscar (Quitamos producto__nombre)
    search_fields = ('numero_venta', 'cliente', 'rut')
    
    # Campos por los que se puede filtrar (Quitamos producto)
    list_filter = ('fecha',)
    
    # --- NUEVO ---
    # Añadimos los detalles (productos) para que se editen en línea
    inlines = [DetalleOrdenInline]

    # Para que el total se recalcule (Opcional, pero recomendado)
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        total_orden = 0
        for instance in instances:
            if not instance._state.adding and instance.pk is None: # Omitir formularios vacíos
                continue
            instance.save()
            total_orden += instance.total_linea
        
        form.instance.total = total_orden
        form.instance.save()
        formset.save_m2m()


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