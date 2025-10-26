# inventario/urls.py
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Corregido: 'inventario' -> 'lista' para coincidir con redirect y url tags
    path('', views.inventario, name='lista'),
    # Corregido: 'crear_producto' -> 'crear'
    path('crear/', views.crear_producto, name='crear'),
     # Corregido: 'editar_producto' -> 'editar'
    path('editar/<int:pk>/', views.editar_producto, name='editar'),
     # Corregido: 'eliminar_producto' -> 'eliminar'
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar'),
    # La API (nombre parece correcto)
    path('api/get_stock/<int:producto_id>/', views.get_stock_producto, name='api_get_stock'),
]