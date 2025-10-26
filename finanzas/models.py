# finanzas/models.py
from django.db import models
from datetime import date
# Importar Trabajador si necesitas relacionarlo explícitamente, aunque no parece necesario aquí
# from recursos_humanos.models import Trabajador

class Gasto(models.Model):
    CATEGORIAS_GASTO = [
        ('SALARIO', 'Salario'),
        ('MATERIAL', 'Materiales de Construcción'),
        ('TRANSPORTE', 'Transporte y Combustible'),
        ('MAQUINARIA', 'Mantenimiento de Maquinaria'),
        ('ADMIN', 'Gastos Administrativos'),
        ('OTRO', 'Otro Gasto'),
    ]
    # Reutilizar TIPO_PROYECTO de Trabajador (importar o redefinir)
    TIPO_PROYECTO = [
        ('CONSTRUCTORA', 'Constructora'),
        ('BLOQUERA', 'Bloquera'),
    ]
    fecha = models.DateField(default=date.today)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS_GASTO, default='OTRO')
    descripcion = models.TextField() # Cambiado a TextField para más espacio
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_proyecto = models.CharField(max_length=20, choices=TIPO_PROYECTO, default='CONSTRUCTORA')

    def __str__(self):
        # Usar f-string para formateo más limpio
        return f"{self.fecha.strftime('%d-%m-%Y')} - {self.get_categoria_display()} - ${self.monto:,.0f}"

    class Meta:
        verbose_name_plural = "Gastos"
        ordering = ['-fecha'] # Ordenar por defecto