# app/models.py
from django.db import models
from datetime import date

# ... (Modelo Producto y OrdenCompra sin cambios) ...
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

class OrdenCompra(models.Model):
    # Convertimos numero_venta para que se genere automáticamente
    numero_venta = models.CharField(max_length=15, unique=True, editable=False, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, blank=True, null=True) # Quitamos unique=True si puede repetirse
    direccion = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "Órdenes de Compra"
        ordering = ['-fecha'] # Opcional: Ordenar por defecto

    def save(self, *args, **kwargs):
        is_new = self.pk is None # Guardamos si es una instancia nueva ANTES de guardar

        # Primero guardamos para obtener un ID si es nuevo
        super().save(*args, **kwargs)

        if is_new and not self.numero_venta: # Generar solo si es nuevo Y no tiene número aún
            # Formato: OC-año-ID (ej: OC-2025-0001)
            self.numero_venta = f"OC-{self.fecha.year}-{self.id:04d}"
            # Volvemos a guardar SOLO este campo para evitar bucles
            super().save(update_fields=['numero_venta'])

    def __str__(self):
        return self.numero_venta or f"Orden #{self.id}"

class DetalleOrden(models.Model):
    orden = models.ForeignKey(OrdenCompra, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
    @property
    def total_linea(self):
        return self.cantidad * self.precio_unitario

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
    
    # --- CAMPO AÑADIDO ---
    salario_por_dia = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        help_text="Salario a pagar por día trabajado"
    )
    # --- FIN DE LO AÑADIDO ---

    def __str__(self):
        return self.nombre
        
    class Meta:
        verbose_name_plural = "Trabajadores"

# ... (Modelo Asistencia y Gasto sin cambios) ...
class Asistencia(models.Model):
    TIPO_PROYECTO = [
        ('CONSTRUCTORA', 'Constructora'),
        ('BLOQUERA', 'Bloquera'),
    ]
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today)
    tipo_proyecto = models.CharField(max_length=20, choices=TIPO_PROYECTO, default='CONSTRUCTORA')

    def __str__(self):
        return f"Asistencia de {self.trabajador.nombre} el {self.fecha}"

    class Meta:
        verbose_name_plural = "Asistencias"
        unique_together = ('trabajador', 'fecha', 'tipo_proyecto')

class Gasto(models.Model):
    CATEGORIAS_GASTO = [
        ('SALARIO', 'Salario'),
        ('MATERIAL', 'Materiales de Construcción'),
        ('TRANSPORTE', 'Transporte y Combustible'),
        ('MAQUINARIA', 'Mantenimiento de Maquinaria'),
        ('ADMIN', 'Gastos Administrativos'),
        ('OTRO', 'Otro Gasto'),
    ]
    TIPO_PROYECTO = [
        ('CONSTRUCTORA', 'Constructora'),
        ('BLOQUERA', 'Bloquera'),
    ]
    fecha = models.DateField(default=date.today)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS_GASTO, default='OTRO')
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_proyecto = models.CharField(max_length=20, choices=TIPO_PROYECTO, default='CONSTRUCTORA')

    def __str__(self):
        return f"{self.fecha} - {self.categoria} - ${self.monto}"

    class Meta:
        verbose_name_plural = "Gastos"