# bloquera/urls.py
from django.contrib import admin
from django.urls import path, include # Importar include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Incluir URLs de las nuevas apps
    # La app 'core' maneja la raíz y autenticación
    path('', include('core.urls')), # No necesita namespace si es la raíz
    # Las otras apps bajo sus propios prefijos y namespaces
    path('inventario/', include('inventario.urls', namespace='inventario')),
    path('personal/', include('recursos_humanos.urls', namespace='recursos_humanos')),
    path('ventas/', include('ventas.urls', namespace='ventas')),
    path('finanzas/', include('finanzas.urls', namespace='finanzas')),

]

# Configuración para servir archivos estáticos en DESARROLLO
# Esto sirve archivos desde los directorios en STATICFILES_DIRS
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Usar STATIC_ROOT es más estándar con collectstatic, pero si no usas collectstatic en dev, STATICFILES_DIRS[0] puede funcionar si solo tienes uno.
    # Si tienes archivos MEDIA_URL y MEDIA_ROOT configurados:
    # from django.conf.urls.static import static
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Servir archivos estáticos (solo en desarrollo)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT)

    # Servir archivos multimedia si los usas
    if hasattr(settings, "MEDIA_URL") and hasattr(settings, "MEDIA_ROOT"):
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)