# inventario/urls.py
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.inventario, name='lista'),
    path('crear/', views.crear_producto, name='crear'),
    path('editar/<int:pk>/', views.editar_producto, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar'),
    # La API
    path('api/get_stock/<int:producto_id>/', views.get_stock_producto, name='api_get_stock'),
]