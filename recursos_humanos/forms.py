# recursos_humanos/forms.py
from django import forms
from .models import Trabajador

class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['nombre', 'rut', 'direccion', 'telefono', 'email', 'tipo_proyecto', 'cargo', 'salario_por_dia']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), # Ajustado a Textarea
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo_proyecto': forms.Select(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'salario_por_dia': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AsistenciaManualForm(forms.Form):
    # Usa el modelo importado
    trabajador = forms.ModelChoiceField(queryset=Trabajador.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    # Usa las choices del modelo
    tipo_proyecto = forms.ChoiceField(choices=Trabajador.TIPO_PROYECTO, widget=forms.Select(attrs={'class': 'form-control'}))

class CalculoSalarioForm(forms.Form):
    # Usa el modelo importado
    trabajador = forms.ModelChoiceField(queryset=Trabajador.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    # Usa las choices del modelo
    tipo_proyecto = forms.ChoiceField(choices=Trabajador.TIPO_PROYECTO, widget=forms.Select(attrs={'class': 'form-control'}))