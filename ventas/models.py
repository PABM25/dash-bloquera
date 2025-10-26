# ventas/models.py
from django.db import models
from django.utils import timezone # Para el año en numero_venta
from inventario.models import Producto # Importar Producto

class OrdenCompra(models.Model):
    numero_venta = models.CharField(max_length=15, unique=True, editable=False, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "Órdenes de Compra"
        ordering = ['-fecha']

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs) # Guardar primero para obtener ID si es nuevo
        if is_new and not self.numero_venta:
            # Generar numero_venta: OC-YYYY-ID (ej: OC-2025-0005)
            year = self.fecha.year if self.fecha else timezone.now().year
            self.numero_venta = f"OC-{year}-{self.id:04d}"
            # Guardar solo el campo actualizado para evitar recursión
            OrdenCompra.objects.filter(pk=self.pk).update(numero_venta=self.numero_venta)
            self.refresh_from_db(fields=['numero_venta']) # Actualizar la instancia

    def __str__(self):
        return self.numero_venta or f"Orden #{self.id}"

class DetalleOrden(models.Model):
    # Asegúrate que las ForeignKey apunten correctamente
    orden = models.ForeignKey(OrdenCompra, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) # Viene de 'inventario'
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

    @property
    def total_linea(self):
        # Asegurarse que ambos son numéricos antes de multiplicar
        if self.cantidad is not None and self.precio_unitario is not None:
            return self.cantidad * self.precio_unitario
        return 0