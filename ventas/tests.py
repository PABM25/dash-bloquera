import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from inventario.models import Producto
from .models import OrdenCompra, DetalleOrden

@pytest.mark.django_db
def test_crear_orden_exitosa(client):
    """Prueba el flujo completo de crear una orden, validando la actualización de stock."""
    # 1. Configuración (Arrange)
    # Crear usuario y loguear
    user = User.objects.create_user(username='vendedor', password='pw')
    client.login(username='vendedor', password='pw')
    
    # Crear producto en inventario
    prod = Producto.objects.create(nombre="Arena", stock=50, descripcion="Saco")
    
    # Datos del formulario a enviar
    url = reverse('ventas:crear_orden')
    form_data = {
        'cliente': 'Constructora XYZ',
        'rut': '77.123.456-K',
        'direccion': 'Calle Falsa 123',
        
        # Formset de Detalles
        'detalles-TOTAL_FORMS': '1',
        'detalles-INITIAL_FORMS': '0',
        'detalles-MIN_NUM_FORMS': '0',
        'detalles-MAX_NUM_FORMS': '1000',
        
        'detalles-0-producto': prod.id,
        'detalles-0-cantidad': 10,
        'detalles-0-precio_unitario': 5000,
        'detalles-0-DELETE': '', # No borrar
    }

    # 2. Acción (Act)
    # Usamos client.post() para simular el envío del formulario
    response = client.post(url, data=form_data)

    # 3. Verificación (Assert)
    # Verificar que la orden se creó y redirigió al detalle
    assert response.status_code == 302 # Redirección
    
    # Verificar que la orden existe en la BD
    assert OrdenCompra.objects.count() == 1
    orden = OrdenCompra.objects.first()
    assert orden.cliente == 'Constructora XYZ'
    assert orden.total == 50000 # 10 * 5000
    
    # Verificar que el detalle de la orden existe
    assert DetalleOrden.objects.count() == 1
    
    # ¡Verificación más importante!
    # Comprobar que el stock del producto se redujo
    prod.refresh_from_db()
    assert prod.stock == 40 # 50 (inicial) - 10 (vendidos)