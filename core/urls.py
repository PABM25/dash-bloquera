# core/urls.py
"""
Define las rutas (URLs) para la aplicación 'core'.
"""
from django.urls import path
from django.contrib.auth import views as auth_views # Vistas de autenticación genéricas
from . import views # Importa las vistas personalizadas de core

# 'app_name' define un espacio de nombres para evitar colisiones
# Se usa en las plantillas (ej. {% url 'core:home' %})
app_name = 'core'

urlpatterns = [
    # --- Vistas Principales y Autenticación ---
    path('', views.home, name='home'), # La raíz del sitio
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:login'), name='logout'),
    path('register/', views.register, name='register'),

    # --- URLs DE CONFIGURACIÓN DE USUARIO ---
    path('settings/', views.user_settings, name='user_settings'),
    path('settings/profile/', views.edit_profile, name='edit_profile'),
    
    # Flujo de cambio de contraseña
    path('settings/password_change/',
         views.CustomPasswordChangeView.as_view(), # 1. Formulario para cambiar
         name='password_change'),
    path('settings/password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='core/password_change_done.html'), # 2. Página de éxito
         name='password_change_done'),
]