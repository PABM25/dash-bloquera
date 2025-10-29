# inventario/forms.py
"""
Define los formularios para la aplicación 'inventario'.
"""
from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    """
    Formulario simple (ModelForm) para crear y editar Productos.
    """
    class Meta:
        model = Producto
        fields = ['nombre', 'stock', 'descripcion']
        # Define los widgets para añadir clases de Bootstrap
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }