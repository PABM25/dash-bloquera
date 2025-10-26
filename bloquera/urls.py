# bloquera/urls.py
from django.contrib import admin
from django.urls import path, include # Importar include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Incluir URLs de las nuevas apps
    # La app 'core' maneja la raíz y autenticación
    path('', include('core.urls')),
    # Las otras apps bajo sus propios prefijos y namespaces
    path('inventario/', include('inventario.urls', namespace='inventario')),
    path('personal/', include('recursos_humanos.urls', namespace='recursos_humanos')),
    path('ventas/', include('ventas.urls', namespace='ventas')),
    path('finanzas/', include('finanzas.urls', namespace='finanzas')),

    # La línea original 'path('', include('app.urls')),' se elimina.
    # Ya no necesitas 'path('accounts/', include('django.contrib.auth.urls')),'
]

# Configuración para servir archivos estáticos y media en DESARROLLO
if settings.DEBUG:
    # Servir archivos estáticos desde STATICFILES_DIRS
    if settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    # Si tienes archivos MEDIA_URL y MEDIA_ROOT configurados:
    # from django.conf.urls.static import static
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)