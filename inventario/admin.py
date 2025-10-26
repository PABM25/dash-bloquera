# inventario/admin.py
from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'stock', 'descripcion')
    search_fields = ('nombre',)
    list_editable = ('stock',) # Permite editar el stock directamente desde la lista