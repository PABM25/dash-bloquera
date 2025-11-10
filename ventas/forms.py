# ventas/forms.py
from django import forms
from django.forms.models import inlineformset_factory
from django.forms import DateInput # Importación añadida
from .models import OrdenCompra, DetalleOrden
from inventario.models import Producto # Importar Producto

class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        # Se añade 'fecha'
        fields = ['fecha', 'cliente', 'rut', 'direccion']
        widgets = {
            # Nuevo widget para el selector de fecha
            'fecha': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), # Textarea
        }

class DetalleOrdenForm(forms.ModelForm):
    # Opcional: Filtrar productos con stock > 0 si lo deseas
    # producto = forms.ModelChoiceField(queryset=Producto.objects.filter(stock__gt=0),
    #                                  widget=forms.Select(attrs={'class': 'form-control producto-select'}))

    class Meta:
        model = DetalleOrden
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control producto-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control cantidad-input', 'value': 1, 'min': 1}), # Añadido min=1
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control precio-input'}),
        }

DetalleOrdenFormSet = inlineformset_factory(
    OrdenCompra,
    DetalleOrden,
    form=DetalleOrdenForm,
    extra=1, # Número de formularios vacíos a mostrar
    can_delete=True,
    can_delete_extra=True # Permitir borrar formularios añadidos dinámicamente
)