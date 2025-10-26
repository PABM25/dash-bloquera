# inventario/models.py
from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.stock})"

    def disminuir_stock(self, cantidad):
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
            return True
        return False

    def aumentar_stock(self, cantidad):
        self.stock += cantidad
        self.save()

    class Meta:
        verbose_name_plural = "Productos"