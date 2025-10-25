from django.db import models
from datetime import date

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
    numero_venta = models.CharField(max_length=10, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    def save(self, *args, **kwargs):
        self.total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "Órdenes de Compra"

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
    

    def __str__(self):
        return self.nombre
        
    class Meta:
        verbose_name_plural = "Trabajadores"

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
        unique_together = ('trabajador', 'fecha', 'tipo_proyecto') # Evita duplicados para el mismo trabajador, fecha y proyecto

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


