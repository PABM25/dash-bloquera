# recursos_humanos/urls.py
from django.urls import path
from . import views

app_name = 'recursos_humanos'

urlpatterns = [
    # --- Trabajadores ---
    path('', views.lista_trabajadores, name='lista_trabajadores'),
    path('crear/', views.crear_trabajador, name='crear_trabajador'),
    path('editar/<int:pk>/', views.editar_trabajador, name='editar_trabajador'),
    path('eliminar/<int:pk>/', views.eliminar_trabajador, name='eliminar_trabajador'),

    # --- Asistencia y Salarios ---
    path('asistencia/', views.asistencia_manual, name='asistencia_manual'), # Cambiado url
    path('asistencia/confirmacion/', views.asistencia_confirmacion, name='asistencia_confirmacion'),
    path('salarios/calcular/', views.calcular_salario, name='calcular_salario'), # Cambiado url
    path('salarios/registrar_gasto/', views.registrar_pago_gasto, name='registrar_pago_gasto'), # Cambiado url
]