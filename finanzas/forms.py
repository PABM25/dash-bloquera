# finanzas/forms.py
"""
Define los formularios para la aplicación 'finanzas'.
"""
from django import forms
from .models import Gasto

class GastoForm(forms.ModelForm):
    """
    Formulario (ModelForm) para crear y editar Gastos.
    """
    class Meta:
        model = Gasto
        # Incluir todos los campos editables
        fields = ['fecha', 'categoria', 'descripcion', 'monto', 'tipo_proyecto']
        # Definir widgets para mejor UX y clases de Bootstrap
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_proyecto': forms.Select(attrs={'class': 'form-control'}),
        }