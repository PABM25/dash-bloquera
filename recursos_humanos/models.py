# recursos_humanos/models.py
from django.db import models
from datetime import date

class Trabajador(models.Model):
    TIPO_PROYECTO = [
        ('CONSTRUCTORA', 'Constructora'),
        ('BLOQUERA', 'Bloquera'),
    ]
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    tipo_proyecto = models.CharField(max_length=20, choices=TIPO_PROYECTO, default='CONSTRUCTORA')
    cargo = models.CharField(max_length=100, blank=True, null=True)
    salario_por_dia = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Salario a pagar por día trabajado"
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Trabajadores"

class Asistencia(models.Model):
    # Reutilizamos TIPO_PROYECTO de Trabajador para consistencia
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today)
    tipo_proyecto = models.CharField(max_length=20, choices=Trabajador.TIPO_PROYECTO, default='CONSTRUCTORA')

    def __str__(self):
        return f"Asistencia de {self.trabajador.nombre} el {self.fecha}"

    class Meta:
        verbose_name_plural = "Asistencias"
        unique_together = ('trabajador', 'fecha', 'tipo_proyecto')