# ventas/urls.py
"""
Configuración de URLs (URLconf) para la aplicación 'ventas'.
"""
from django.urls import path
from . import views

# Define el espacio de nombres (namespace) para esta app
app_name = 'ventas'

urlpatterns = [
    # Ej. /ventas/crear/
    path('crear/', views.crear_orden, name='crear_orden'),
    # Ej. /ventas/lista/
    path('lista/', views.lista_ordenes, name='lista_ordenes'),
    # Ej. /ventas/detalle/5/
    path('detalle/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
    # Ej. /ventas/detalle/5/pdf/
    path('detalle/<int:orden_id>/pdf/', views.descargar_orden_pdf, name='descargar_orden_pdf'),
    # Ej. /ventas/detalle/5/docx/
    path('detalle/<int:orden_id>/docx/', views.descargar_orden_docx, name='descargar_orden_docx'),
    path('detalle/<int:orden_id>/pagar/', views.registrar_pago_orden, name='registrar_pago_orden'),
]