# ventas/admin.py
from django.contrib import admin
from .models import OrdenCompra, DetalleOrden

class DetalleOrdenInline(admin.TabularInline):
    model = DetalleOrden
    extra = 1 # Cuántas filas vacías mostrar al crear/editar
    fields = ('producto', 'cantidad', 'precio_unitario')
    # readonly_fields = ('total_linea',) # No puedes hacer readonly un @property directamente aquí
    autocomplete_fields = ['producto'] # Facilita la selección si hay muchos productos

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ('numero_venta', 'cliente', 'fecha', 'total', 'rut')
    search_fields = ('numero_venta', 'cliente', 'rut')
    list_filter = ('fecha',)
    date_hierarchy = 'fecha' # Navegación por fechas
    inlines = [DetalleOrdenInline] # Añadir detalles en línea
    readonly_fields = ('numero_venta', 'total') # El total se calcula, el número se autogenera

    # Opcional: Recalcular total si se edita desde el admin (más robusto hacerlo en el modelo o formset)
    # def save_formset(self, request, form, formset, change):
    #     instances = formset.save(commit=False)
    #     total_orden_recalculado = 0
    #     valid_instances_to_save = []
    #     for instance in instances:
    #         # Solo procesar si no se va a borrar y tiene producto
    #         should_delete = formset.can_delete and formset._should_delete_form(formset.forms[instances.index(instance)])
    #         if not should_delete and instance.producto:
    #             # instance.save() # Guardar instancia para que tenga PK si es nueva
    #             valid_instances_to_save.append(instance)
    #             total_orden_recalculado += instance.total_linea

        # Guardar instancias válidas primero
    #     for instance in valid_instances_to_save:
    #          instance.save()

        # Actualizar el total de la orden principal si cambió
    #     if form.instance.total != total_orden_recalculado:
    #         form.instance.total = total_orden_recalculado
    #         form.instance.save(update_fields=['total']) # Guardar solo el total

    #     formset.save_m2m() # Guardar relaciones m2m si las hubiera
    #     # Llamar al método original para manejar el borrado
    #     super().save_formset(request, form, formset, change)


# No es necesario registrar DetalleOrden por separado si se usa Inline
# @admin.register(DetalleOrden)
# class DetalleOrdenAdmin(admin.ModelAdmin):
#     list_display = ('orden', 'producto', 'cantidad', 'precio_unitario', 'total_linea')
#     list_filter = ('orden', 'producto')