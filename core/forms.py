# core/forms.py
"""
Define los formularios personalizados para la gestión de usuarios.
"""
from django import forms
from .models import *
from django.forms.models import inlineformset_factory

# Importaciones de formularios de autenticación de Django
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from django.contrib.auth.models import User

class RegistroForm(UserCreationForm):
    """
    Formulario de registro de nuevos usuarios.
    Hereda de UserCreationForm y añade campos (nombre, apellido, email).
    """
    class Meta:
        model = User
        # Campos que se mostrarán en el formulario
        fields = ['username', 'first_name', 'last_name', 'email']
        # Etiquetas personalizadas en español
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
        }
    
    def __init__(self, *args, **kwargs):
        """
        Sobrescribe el constructor para añadir la clase 'form-control'
        de Bootstrap a todos los campos y ocultar la ayuda de contraseña.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = '' # Ocultar ayuda de contraseña

class EditProfileForm(UserChangeForm):
    """
    Formulario para editar el perfil de un usuario existente.
    Hereda de UserChangeForm.
    """
    # Ocultamos el campo de contraseña, ya que se maneja
    # en una vista separada (PasswordChangeView).
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
        # Widgets para asegurar que los campos usen clases de Bootstrap
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }