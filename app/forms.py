# app/forms.py
from django import forms
from .models import *
from django.forms.models import inlineformset_factory
# --- Importaciones Añadidas ---
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from django.contrib.auth.models import User
# --- FIN ---

# ... (RegistroForm y otros formularios existentes) ...

# --- FIN DE LO NUEVO ---

# ... (ProductoForm y el resto de formularios existentes) ...


