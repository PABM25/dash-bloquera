import pytest
from .models import Producto

# El marcador 'django_db' asegura que la base de datos de prueba esté disponible
@pytest.mark.django_db
def test_disminuir_stock_exitoso():
    """Prueba que el stock se reduce correctamente si hay suficiente."""
    # 1. Configuración (Arrange)
    producto = Producto.objects.create(nombre="Cemento", stock=100)

    # 2. Acción (Act)
    resultado = producto.disminuir_stock(20)

    # 3. Verificación (Assert)
    producto.refresh_from_db() # Recargar datos desde la BD
    assert resultado == True
    assert producto.stock == 80

@pytest.mark.django_db
def test_disminuir_stock_insuficiente():
    """Prueba que el stock no cambia si se pide más de lo disponible."""
    # 1. Configuración (Arrange)
    producto = Producto.objects.create(nombre="Bloques", stock=10)

    # 2. Acción (Act)
    resultado = producto.disminuir_stock(50)

    # 3. Verificación (Assert)
    producto.refresh_from_db()
    assert resultado == False
    assert producto.stock == 10 # El stock no debe cambiar