# ventas/models.py
"""
Define los modelos de la base de datos para la aplicación 'ventas'.
...
"""

from django.db import models
from django.utils import timezone
from inventario.models import Producto
from decimal import Decimal # <-- ¡AÑADIR ESTA IMPORTACIÓN!

class OrdenCompra(models.Model):
    """
    Representa el encabezado de una orden de compra (venta).
    ...
    """
    
    class EstadoPago(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        ABONADA = 'ABONADA', 'Abonada'
        PAGADA = 'PAGADA', 'Pagada'
    
    numero_venta = models.CharField(max_length=15, unique=True, editable=False, blank=True)
    fecha = models.DateTimeField(default=timezone.now)
    cliente = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    total_costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_utilidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    estado_pago = models.CharField(
        max_length=10,
        choices=EstadoPago.choices,
        default=EstadoPago.PENDIENTE
    )
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "Órdenes de Compra"
        ordering = ['-fecha'] # Ordenar por defecto de más nueva a más antigua

    # --- MÉTODOS EN LA UBICACIÓN CORRECTA ---
    @property
    def saldo_pendiente(self):
        """ Calcula cuánto falta por pagar. """
        return self.total - self.monto_pagado

    def registrar_pago(self, monto_abono):
        """
        Lógica de negocio para registrar un pago.
        Actualiza el monto_pagado y el estado_pago.
        """
        if monto_abono <= 0:
            return # No hacer nada si el monto es cero o negativo

        # --- LÍNEA CORREGIDA ---
        # Usar 'Decimal' del módulo 'decimal', no 'models.Decimal'
        monto_abono = Decimal(monto_abono)
        # --- FIN DE CORRECCIÓN ---

        self.monto_pagado += monto_abono
        
        if self.monto_pagado >= self.total:
            self.monto_pagado = self.total # Evitar pagar de más
            self.estado_pago = self.EstadoPago.PAGADA
        elif self.monto_pagado > 0:
            self.estado_pago = self.EstadoPago.ABONADA
        else:
            self.estado_pago = self.EstadoPago.PENDIENTE
            
        self.save()
    # --- FIN DE MÉTODOS ---

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para generar un 'numero_venta' único.
        ...
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new and not self.numero_venta:
            year = self.fecha.year if self.fecha else timezone.now().year
            self.numero_venta = f"OC-{year}-{self.id:04d}"
            OrdenCompra.objects.filter(pk=self.pk).update(numero_venta=self.numero_venta)
            self.refresh_from_db(fields=['numero_venta'])

    def __str__(self):
        """Representación en texto del modelo (ej. en el Admin)."""
        return self.numero_venta or f"Orden #{self.id}"

class DetalleOrden(models.Model):
    """
    Representa una línea de producto dentro de una OrdenCompra.
    ...
    """
    orden = models.ForeignKey(OrdenCompra, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    costo_unitario_en_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

    @property
    def total_linea(self):
        if self.cantidad is not None and self.precio_unitario is not None:
            return self.cantidad * self.precio_unitario
        return 0
    
    @property
    def utilidad_linea(self):
        """ Calcula la utilidad de esta línea específica. """
        if self.cantidad is not None and self.precio_unitario is not None:
            costo_total_linea = self.cantidad * self.costo_unitario_en_venta
            return self.total_linea - costo_total_linea
        return 0