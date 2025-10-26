from django import forms
from .models import *
from django.forms.models import inlineformset_factory

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'stock', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        # ACTUALIZADO: Quitamos numero_venta
        fields = ['cliente', 'direccion', 'rut']
        widgets = {
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DetalleOrdenForm(forms.ModelForm):
    class Meta:
        model = DetalleOrden
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control producto-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control cantidad-input', 'value': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control precio-input'}),
        }

DetalleOrdenFormSet = inlineformset_factory(
    OrdenCompra,
    DetalleOrden,
    form=DetalleOrdenForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True
)

class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['nombre', 'rut', 'direccion', 'telefono', 'email', 'tipo_proyecto', 'cargo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo_proyecto': forms.Select(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AsistenciaManualForm(forms.Form):
    trabajador = forms.ModelChoiceField(queryset=Trabajador.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    tipo_proyecto = forms.ChoiceField(choices=Trabajador.TIPO_PROYECTO, widget=forms.Select(attrs={'class': 'form-control'}))

class CalculoSalarioForm(forms.Form):
    trabajador = forms.ModelChoiceField(queryset=Trabajador.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    tipo_proyecto = forms.ChoiceField(choices=Trabajador.TIPO_PROYECTO, widget=forms.Select(attrs={'class': 'form-control'}))

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['fecha', 'categoria', 'descripcion', 'monto', 'tipo_proyecto']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_proyecto': forms.Select(attrs={'class': 'form-control'}),
        }