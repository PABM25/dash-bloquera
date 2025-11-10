# inventario/models.py
"""
Define el modelo de la base de datos para la aplicación 'inventario'.
"""
from django.db import models

class Producto(models.Model):
    """
    Representa un producto o material en el inventario.
    
    Almacena el nombre, la cantidad en stock y una descripción.
    Incluye métodos para manipular el stock de forma segura.
    """
    nombre = models.CharField(max_length=100, unique=True)
    stock = models.PositiveIntegerField(default=0)
    precio_costo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        help_text="Cuánto cuesta adquirir este producto."
    )
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        """Representación en texto (ej. "Cemento (500)")."""
        return f"{self.nombre} ({self.stock})"

    def disminuir_stock(self, cantidad):
        """
        Método de negocio para reducir el stock.
        Valida que haya stock suficiente antes de guardar.

        Args:
            cantidad (int): La cantidad a disminuir.

        Returns:
            bool: True si la operación fue exitosa, False si no hay stock.
        """
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save() # Guarda el cambio en la BD
            return True
        return False # No hay stock suficiente

    def aumentar_stock(self, cantidad):
        """
        Método de negocio para aumentar el stock (ej. devoluciones).
        """
        self.stock += cantidad
        self.save()

    class Meta:
        verbose_name_plural = "Productos"