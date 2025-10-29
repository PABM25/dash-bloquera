# ventas/models.py
"""
Define los modelos de la base de datos para la aplicación 'ventas'.

Incluye la 'OrdenCompra' (el encabezado de la venta) y
'DetalleOrden' (las líneas de productos de esa venta).
"""

from django.db import models
from django.utils import timezone # Para obtener el año actual
from inventario.models import Producto # Importa el modelo Producto de otra app

class OrdenCompra(models.Model):
    """
    Representa el encabezado de una orden de compra (venta).

    Almacena la información del cliente, la fecha y el total calculado.
    Genera automáticamente un número de venta único (ej. OC-2025-0001)
    al guardarse por primera vez.
    """
    # Campo para el número de venta autogenerado.
    numero_venta = models.CharField(max_length=15, unique=True, editable=False, blank=True)
    # Fecha de creación automática.
    fecha = models.DateTimeField(auto_now_add=True)
    # Datos del cliente.
    cliente = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    # Total calculado de la orden.
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "Órdenes de Compra"
        ordering = ['-fecha'] # Ordenar por defecto de más nueva a más antigua

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para generar un 'numero_venta' único.

        Si el objeto es nuevo (is_new = True), primero lo guarda
        para obtener un 'pk' (ID), y luego usa ese ID para construir
        el 'numero_venta'. Finalmente, actualiza el objeto solo con
        ese campo para evitar recursión.
        """
        # Comprueba si el objeto se está creando (no tiene pk)
        is_new = self.pk is None
        # Llama al 'save' original para crear el objeto y obtener un ID
        super().save(*args, **kwargs)
        
        # Si es nuevo y 'numero_venta' aún no está asignado:
        if is_new and not self.numero_venta:
            # Generar numero_venta: OC-YYYY-ID (ej: OC-2025-0005)
            year = self.fecha.year if self.fecha else timezone.now().year
            self.numero_venta = f"OC-{year}-{self.id:04d}"
            # Usar .update() para guardar solo este campo y evitar un bucle infinito
            OrdenCompra.objects.filter(pk=self.pk).update(numero_venta=self.numero_venta)
            # Actualiza la instancia en memoria con el nuevo valor
            self.refresh_from_db(fields=['numero_venta'])

    def __str__(self):
        """Representación en texto del modelo (ej. en el Admin)."""
        return self.numero_venta or f"Orden #{self.id}"

class DetalleOrden(models.Model):
    """
    Representa una línea de producto dentro de una OrdenCompra.

    Conecta la OrdenCompra con un Producto específico, guardando
    la cantidad y el precio unitario al momento de la venta.
    """
    # Relación con la orden padre. 'related_name' permite acceder
    # a los detalles desde una orden (ej. orden.detalles.all())
    orden = models.ForeignKey(OrdenCompra, related_name='detalles', on_delete=models.CASCADE)
    # Relación con el producto vendido.
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    # Datos de la línea de venta.
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """Representación en texto (ej. "5 x Cemento")."""
        return f"{self.cantidad} x {self.producto.nombre}"

    @property
    def total_linea(self):
        """
        Calcula el total para esta línea (Cantidad * Precio).
        Se usa como una propiedad (campo calculado) en lugar de
        guardarlo en la base de datos, ya que se puede derivar.
        """
        if self.cantidad is not None and self.precio_unitario is not None:
            return self.cantidad * self.precio_unitario
        return 0