# recursos_humanos/forms.py
"""
Define los formularios para la aplicación 'recursos_humanos'.
"""
from django import forms
from .models import Trabajador # Importa el modelo

class TrabajadorForm(forms.ModelForm):
    """Formulario para crear y editar Trabajadores."""
    class Meta:
        model = Trabajador
        fields = ['nombre', 'rut', 'direccion', 'telefono', 'email', 'tipo_proyecto', 'cargo', 'salario_por_dia']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo_proyecto': forms.Select(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'salario_por_dia': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AsistenciaManualForm(forms.Form):
    """
    Formulario estándar (no ModelForm) para registrar asistencia manual.
    Permite seleccionar un trabajador, fecha y tipo de proyecto.
    """
    # ModelChoiceField crea un <select> a partir de un QuerySet
    trabajador = forms.ModelChoiceField(queryset=Trabajador.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    # ChoiceField usa las opciones definidas en el modelo
    tipo_proyecto = forms.ChoiceField(choices=Trabajador.TIPO_PROYECTO, widget=forms.Select(attrs={'class': 'form-control'}))

class CalculoSalarioForm(forms.Form):
    """
    Formulario estándar (no ModelForm) para la vista de cálculo de salario.
    Solo define los campos necesarios para filtrar las asistencias.
    """
    trabajador = forms.ModelChoiceField(queryset=Trabajador.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    tipo_proyecto = forms.ChoiceField(choices=Trabajador.TIPO_PROYECTO, widget=forms.Select(attrs={'class': 'form-control'}))