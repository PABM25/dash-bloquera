# recursos_humanos/models.py
"""
Define los modelos de la base de datos para 'recursos_humanos'.
"""
from django.db import models
from datetime import date

class Trabajador(models.Model):
    """
    Representa a un empleado o trabajador.
    """
    # Opciones compartidas (usadas también por Asistencia y Gasto)
    TIPO_PROYECTO = [
        ('CONSTRUCTORA', 'Constructora'),
        ('BLOQUERA', 'Bloquera'),
    ]
    
    # Campos de información personal
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    # Campos laborales
    tipo_proyecto = models.CharField(max_length=20, choices=TIPO_PROYECTO, default='CONSTRUCTORA')
    cargo = models.CharField(max_length=100, blank=True, null=True)
    salario_por_dia = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Salario a pagar por día trabajado"
    )

    def __str__(self):
        """Representación en texto."""
        return self.nombre

    class Meta:
        verbose_name_plural = "Trabajadores"

class Asistencia(models.Model):
    """
    Representa un registro de asistencia diaria para un trabajador.
    """
    # Relación con el trabajador
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today)
    # Reutiliza las choices de TIPO_PROYECTO del modelo Trabajador
    tipo_proyecto = models.CharField(max_length=20, choices=Trabajador.TIPO_PROYECTO, default='CONSTRUCTORA')

    def __str__(self):
        """Representación en texto."""
        return f"Asistencia de {self.trabajador.nombre} el {self.fecha}"

    class Meta:
        verbose_name_plural = "Asistencias"
        # Restricción clave: Evita duplicados. Un trabajador no puede
        # tener dos asistencias el mismo día para el mismo tipo de proyecto.
        unique_together = ('trabajador', 'fecha', 'tipo_proyecto')