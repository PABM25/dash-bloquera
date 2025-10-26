# finanzas/urls.py
from django.urls import path
from . import views

app_name = 'finanzas'

urlpatterns = [
    path('', views.lista_gastos, name='lista_gastos'), # Cambiado url base a vacío
    path('registrar/', views.registrar_gasto, name='registrar_gasto'),
    path('editar/<int:pk>/', views.editar_gasto, name='editar_gasto'),
    path('eliminar/<int:pk>/', views.eliminar_gasto, name='eliminar_gasto'),
]