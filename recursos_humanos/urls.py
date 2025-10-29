# recursos_humanos/urls.py
"""
Configuración de URLs (URLconf) para la aplicación 'recursos_humanos'.
"""
from django.urls import path
from . import views

app_name = 'recursos_humanos'

urlpatterns = [
    # --- Trabajadores (CRUD) ---
    # Ej. /personal/ (Lista de trabajadores)
    path('', views.lista_trabajadores, name='lista_trabajadores'),
    # Ej. /personal/crear/
    path('crear/', views.crear_trabajador, name='crear_trabajador'),
    # Ej. /personal/editar/5/
    path('editar/<int:pk>/', views.editar_trabajador, name='editar_trabajador'),
    # Ej. /personal/eliminar/5/
    path('eliminar/<int:pk>/', views.eliminar_trabajador, name='eliminar_trabajador'),

    # --- Asistencia y Salarios ---
    # Ej. /personal/asistencia/
    path('asistencia/', views.asistencia_manual, name='asistencia_manual'),
    # Ej. /personal/asistencia/confirmacion/
    path('asistencia/confirmacion/', views.asistencia_confirmacion, name='asistencia_confirmacion'),
    # Ej. /personal/salarios/calcular/
    path('salarios/calcular/', views.calcular_salario, name='calcular_salario'),
    # Ej. /personal/salarios/registrar_gasto/ (Procesa el pago)
    path('salarios/registrar_gasto/', views.registrar_pago_gasto, name='registrar_pago_gasto'),
]