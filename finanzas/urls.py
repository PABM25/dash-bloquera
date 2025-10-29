# finanzas/urls.py
"""
Configuración de URLs (URLconf) para la aplicación 'finanzas'.
"""
from django.urls import path
from . import views

app_name = 'finanzas'

urlpatterns = [
    # Ej. /finanzas/ (Muestra la lista de gastos)
    path('', views.lista_gastos, name='lista_gastos'),
    # Ej. /finanzas/registrar/
    path('registrar/', views.registrar_gasto, name='registrar_gasto'),
    # Ej. /finanzas/editar/5/
    path('editar/<int:pk>/', views.editar_gasto, name='editar_gasto'),
    # Ej. /finanzas/eliminar/5/
    path('eliminar/<int:pk>/', views.eliminar_gasto, name='eliminar_gasto'),
]