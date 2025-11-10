import pytest
from django.urls import reverse
from django.contrib.auth.models import User

# 'client' es un fixture de pytest-django que simula un navegador
@pytest.mark.django_db
def test_dashboard_redirecciona_sin_login(client):
    """Prueba que el home (dashboard) redirige al login si el usuario no está autenticado."""
    url = reverse('core:home')
    response = client.get(url)
    
    # 302 es el código para "Redirección"
    assert response.status_code == 302
    # Verifica que redirige a la URL de login
    assert response.url.startswith(reverse('core:login'))

@pytest.mark.django_db
def test_dashboard_carga_con_login(client):
    """Prueba que el dashboard carga correctamente para un usuario autenticado."""
    # 1. Configuración: Crear un usuario y loguearlo
    user = User.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    # 2. Acción: Acceder al home
    url = reverse('core:home')
    response = client.get(url)

    # 3. Verificación
    assert response.status_code == 200
    # Verifica que se usó la plantilla correcta
    assert 'core/home.html' in [t.name for t in response.templates]
    # Verifica que el contexto (datos) se está enviando
    assert 'total_ventas' in response.context
    assert 'asistencia_del_mes' in response.context