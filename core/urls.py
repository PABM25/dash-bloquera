# core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views # Importa vistas de core

app_name = 'core'

urlpatterns = [
    # --- Vistas Principales y Autenticación ---
    path('', views.home, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:login'), name='logout'), # Redirige a core:login
    path('register/', views.register, name='register'),

    # --- URLs DE CONFIGURACIÓN ---
    path('settings/', views.user_settings, name='user_settings'),
    path('settings/profile/', views.edit_profile, name='edit_profile'),
    path('settings/password_change/',
         views.CustomPasswordChangeView.as_view(),
         name='password_change'),
    path('settings/password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='core/password_change_done.html'), # Ajustado
         name='password_change_done'),

    # Puedes añadir otras URLs generales aquí si es necesario
]