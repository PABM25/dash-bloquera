# finanzas/forms.py
from django import forms
from .models import Gasto

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        # Incluir todos los campos relevantes
        fields = ['fecha', 'categoria', 'descripcion', 'monto', 'tipo_proyecto']
        widgets = {
            # Usar DateInput de HTML5 para selector de fecha
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            # Usar Textarea para descripción más larga
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_proyecto': forms.Select(attrs={'class': 'form-control'}),
        }