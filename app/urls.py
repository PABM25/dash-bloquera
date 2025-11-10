from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('crear/', crear_orden, name='crear_orden'),
    path('orden/<int:orden_id>/', detalle_orden, name='detalle_orden'),
    path('orden/<int:orden_id>/descargar_pdf/', descargar_orden_pdf, name='descargar_orden_pdf'), # Nombre actualizado
    path('orden/<int:orden_id>/descargar_jpg/', descargar_orden_jpg, name='descargar_orden_jpg'),
    path('orden/<int:orden_id>/descargar_docx/', descargar_orden_docx, name='descargar_orden_docx'), # Añadido
    path('trabajadores/', lista_trabajadores, name='lista_trabajadores'),
    path('crear_trabajador/', crear_trabajador, name='crear_trabajador'),
    path('asistencia_manual/', asistencia_manual, name='asistencia_manual'),
    path('asistencia/confirmacion/', asistencia_confirmacion, name='asistencia_confirmacion'), # Añadido si se usa
    path('inventario/', inventario, name='inventario'),
    path('inventario/crear/', crear_producto, name='crear_producto'),
    path('inventario/editar/<int:pk>/', editar_producto, name='editar_producto'),
    path('inventario/eliminar/<int:pk>/', eliminar_producto, name='eliminar_producto'),
    path('gastos/', lista_gastos, name='lista_gastos'),
    path('gastos/registrar/', registrar_gasto, name='registrar_gasto'),
    # path('gastos/por_categoria/', gastos_por_categoria, name='gastos_por_categoria'), # Descomenta si creas la vista
    # path('confirmacion/', confirmacion_accion, name='confirmacion_accion'), # Descomenta si creas la vista
]

# Configuración de archivos estáticos para desarrollo
if settings.DEBUG:
    static_root = getattr(settings, 'STATIC_ROOT', None)
    if static_root:
        urlpatterns += static(settings.STATIC_URL, document_root=static_root)
    elif settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])