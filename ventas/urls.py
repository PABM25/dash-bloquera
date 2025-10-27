# ventas/urls.py
from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('crear/', views.crear_orden, name='crear_orden'),
    path('lista/', views.lista_ordenes, name='lista_ordenes'),
    path('detalle/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
    path('detalle/<int:orden_id>/pdf/', views.descargar_orden_pdf, name='descargar_orden_pdf'),
    path('detalle/<int:orden_id>/docx/', views.descargar_orden_docx, name='descargar_orden_docx'),
]