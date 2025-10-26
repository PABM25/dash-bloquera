# ventas/urls.py
from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('crear/', views.crear_orden, name='crear_orden'),
    # Asegúrate que 'lista_ordenes' es el nombre usado en {% url %} y redirect
    path('lista/', views.lista_ordenes, name='lista_ordenes'),
    # Asegúrate que 'detalle_orden' es el nombre usado en {% url %} y redirect
    path('detalle/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
    path('detalle/<int:orden_id>/pdf/', views.descargar_orden_pdf, name='descargar_orden_pdf'),
    path('detalle/<int:orden_id>/jpg/', views.descargar_orden_jpg, name='descargar_orden_jpg'),
    path('detalle/<int:orden_id>/docx/', views.descargar_orden_docx, name='descargar_orden_docx'),
]