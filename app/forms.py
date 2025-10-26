# app/forms.py
from django import forms
from .models import *
from django.forms.models import inlineformset_factory
# --- Importaciones Añadidas ---
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from django.contrib.auth.models import User
# --- FIN ---

# ... (RegistroForm y otros formularios existentes) ...
class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = '' # Ocultar ayuda de contraseña

# --- NUEVO FORMULARIO ---
class EditProfileForm(UserChangeForm):
    # Omitimos la contraseña aquí, Django tiene una vista separada para eso
    password = None 

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
        }
        widgets = { # Asegurar que usen las clases de Bootstrap
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
# --- FIN DE LO NUEVO ---

# ... (ProductoForm y el resto de formularios existentes) ...
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
        fields = ['nombre', 'rut', 'direccion', 'telefono', 'email', 'tipo_proyecto', 'cargo', 'salario_por_dia']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo_proyecto': forms.Select(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'salario_por_dia': forms.NumberInput(attrs={'class': 'form-control'}),
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