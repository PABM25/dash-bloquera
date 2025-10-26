# app/urls.py
from django.urls import path
from .views import * # Asegúrate que esto importe todo (*)
from django.conf import settings
from django.conf.urls.static import static
# --- Importar Vistas de Contraseña ---
from django.contrib.auth import views as auth_views 
# Quitamos CustomPasswordChangeDoneView porque usamos la default especificando plantilla
from .views import CustomPasswordChangeView 
# --- FIN ---

urlpatterns = [
    # --- Vistas de Autenticación ---
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
    
    # --- NUEVAS URLS DE CONFIGURACIÓN ---
    path('settings/', user_settings, name='user_settings'),
    path('settings/profile/', edit_profile, name='edit_profile'),
    # Usamos la vista personalizada para el formulario
    path('settings/password_change/', 
         CustomPasswordChangeView.as_view(), 
         name='password_change'),
    # Usamos la vista por defecto de Django para la página de éxito,
    # especificando nuestra plantilla directamente aquí.
    path('settings/password_change/done/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='app/password_change_done.html'), 
         name='password_change_done'),
    # --- FIN DE URLS NUEVAS ---

    # --- Vistas Principales ---
    path('', home, name='home'),
    path('crear/', crear_orden, name='crear_orden'),
    path('ordenes/', lista_ordenes, name='lista_ordenes'), 
    path('orden/<int:orden_id>/', detalle_orden, name='detalle_orden'),
    path('orden/<int:orden_id>/descargar_pdf/', descargar_orden_pdf, name='descargar_orden_pdf'),
    path('orden/<int:orden_id>/descargar_jpg/', descargar_orden_jpg, name='descargar_orden_jpg'),
    path('orden/<int:orden_id>/descargar_docx/', descargar_orden_docx, name='descargar_orden_docx'),
    
    # --- Trabajadores ---
    path('trabajadores/', lista_trabajadores, name='lista_trabajadores'),
    path('crear_trabajador/', crear_trabajador, name='crear_trabajador'),
    path('trabajador/editar/<int:pk>/', editar_trabajador, name='editar_trabajador'), 
    path('trabajador/eliminar/<int:pk>/', eliminar_trabajador, name='eliminar_trabajador'), 

    # --- Asistencia y Salarios ---
    path('asistencia_manual/', asistencia_manual, name='asistencia_manual'),
    path('asistencia/confirmacion/', asistencia_confirmacion, name='asistencia_confirmacion'),
    path('calcular_salario/', calcular_salario, name='calcular_salario'), 
    path('registrar_pago_gasto/', registrar_pago_gasto, name='registrar_pago_gasto'), 

    # --- Inventario ---
    path('inventario/', inventario, name='inventario'),
    path('inventario/crear/', crear_producto, name='crear_producto'),
    path('inventario/editar/<int:pk>/', editar_producto, name='editar_producto'),
    path('inventario/eliminar/<int:pk>/', eliminar_producto, name='eliminar_producto'),
    
    # --- Gastos ---
    path('gastos/', lista_gastos, name='lista_gastos'),
    path('gastos/registrar/', registrar_gasto, name='registrar_gasto'),
    path('gastos/editar/<int:pk>/', editar_gasto, name='editar_gasto'), 
    path('gastos/eliminar/<int:pk>/', eliminar_gasto, name='eliminar_gasto'), 

    # --- APIs (para JavaScript) ---
    path('api/get_stock_producto/<int:producto_id>/', get_stock_producto, name='get_stock_producto'), 
]

# Configuración de archivos estáticos para desarrollo
if settings.DEBUG:
    static_root = getattr(settings, 'STATIC_ROOT', None)
    if static_root:
        urlpatterns += static(settings.STATIC_URL, document_root=static_root)
    elif settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])