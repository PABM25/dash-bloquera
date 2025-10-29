# inventario/urls.py
"""
Define las rutas (URLs) para la aplicación 'inventario'.
"""
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Rutas del CRUD
    path('', views.inventario, name='lista'), # Vista de lista
    path('crear/', views.crear_producto, name='crear'), # Vista de creación
    path('editar/<int:pk>/', views.editar_producto, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar'),
    
    # Ruta de la API de Stock (para JS)
    path('api/get_stock/<int:producto_id>/', views.get_stock_producto, name='api_get_stock'),
]