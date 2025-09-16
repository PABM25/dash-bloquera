from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('crear/', crear_orden, name='crear_orden'),
    path('orden/<int:orden_id>/', detalle_orden, name='detalle_orden'),
    path('imprimir/<int:orden_id>/', imprimir_orden, name='imprimir_orden'),
    path('trabajadores/', lista_trabajadores, name='lista_trabajadores'),
    path('crear_trabajador/', crear_trabajador, name='crear_trabajador'),
    # Se eliminan las rutas relacionadas con QR y confirmación de asistencia
    path('asistencia_manual/', asistencia_manual, name='asistencia_manual'),
    path('inventario/', inventario, name='inventario'),
    path('inventario/crear/', crear_producto, name='crear_producto'),
    path('inventario/editar/<int:pk>/', editar_producto, name='editar_producto'),
    path('inventario/eliminar/<int:pk>/', eliminar_producto, name='eliminar_producto'),
    path('gastos/', lista_gastos, name='lista_gastos'),
    path('gastos/registrar/', registrar_gasto, name='registrar_gasto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
