# finanzas/models.py
"""
Define los modelos de la base de datos para la aplicación 'finanzas'.
"""
from django.db import models
from datetime import date

class Gasto(models.Model):
    """
    Representa un gasto operativo o de salario.
    """
    
    # Opciones predefinidas para el campo 'categoria'
    CATEGORIAS_GASTO = [
        ('SALARIO', 'Salario'),
        ('MATERIAL', 'Materiales de Construcción'),
        ('TRANSPORTE', 'Transporte y Combustible'),
        ('MAQUINARIA', 'Mantenimiento de Maquinaria'),
        ('ADMIN', 'Gastos Administrativos'),
        ('OTRO', 'Otro Gasto'),
    ]
    
    # Opciones predefinidas para el proyecto (duplicadas de 'recursos_humanos'
    # para mantener la app desacoplada, aunque podría importarse).
    TIPO_PROYECTO = [
        ('CONSTRUCTORA', 'Constructora'),
        ('BLOQUERA', 'Bloquera'),
    ]
    
    fecha = models.DateField(default=date.today)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS_GASTO, default='OTRO')
    descripcion = models.TextField() # Permite descripciones largas
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_proyecto = models.CharField(max_length=20, choices=TIPO_PROYECTO, default='CONSTRUCTORA')

    def __str__(self):
        """
        Representación en texto (ej. "29-10-2025 - Salario - $500.000").
        Usa formato 'f-string' y formateo de moneda (:,.0f).
        """
        return f"{self.fecha.strftime('%d-%m-%Y')} - {self.get_categoria_display()} - ${self.monto:,.0f}"

    class Meta:
        verbose_name_plural = "Gastos"
        ordering = ['-fecha'] # Ordenar por defecto (más nuevos primero)