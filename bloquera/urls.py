# bloquera/urls.py
"""
Configuración principal de URLs (URLconf) para el proyecto bloquera.

Este archivo es el "enrutador" principal. Dirige las peticiones de URL
a las aplicaciones correspondientes (core, inventario, ventas, etc.).
"""

from django.contrib import admin
from django.urls import path, include # 'include' es clave para enlazar otras apps
from django.conf import settings # Para acceder a settings.DEBUG
from django.conf.urls.static import static # Para servir archivos en desarrollo

urlpatterns = [
    # 1. Ruta del Panel de Administración de Django
    path('admin/', admin.site.urls),

    # 2. Rutas de las Aplicaciones
    # Incluye las URLs de la app 'core' en la raíz (ej. '/', '/login/', '/settings/')
    path('', include('core.urls')), 
    
    # Incluye las apps bajo sus propios prefijos (namespaces)
    # Ej. /inventario/lista/, /inventario/crear/
    path('inventario/', include('inventario.urls', namespace='inventario')),
    # Ej. /personal/lista_trabajadores/, /personal/asistencia/
    path('personal/', include('recursos_humanos.urls', namespace='recursos_humanos')),
    # Ej. /ventas/lista/, /ventas/crear/
    path('ventas/', include('ventas.urls', namespace='ventas')),
    # Ej. /finanzas/lista_gastos/, /finanzas/registrar/
    path('finanzas/', include('finanzas.urls', namespace='finanzas')),
]

# --- Configuración para Desarrollo (DEBUG=True) ---
if settings.DEBUG:
    
    if hasattr(settings, "MEDIA_URL") and hasattr(settings, "MEDIA_ROOT"):
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)