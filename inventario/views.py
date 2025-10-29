# inventario/views.py
"""
Define las vistas (lógica) para la aplicación 'inventario'.

Incluye el CRUD (Crear, Leer, Actualizar, Eliminar) para Productos
y una vista de API simple para consultar el stock desde JavaScript.
"""

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Producto
from .forms import ProductoForm

@login_required
def inventario(request):
    """Muestra la lista de todos los productos en el inventario."""
    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'inventario/inventario.html', {'productos': productos})

@login_required
def crear_producto(request):
    """Maneja la creación (GET/POST) de un nuevo producto."""
    titulo = "Agregar Nuevo Producto"
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado.")
            return redirect('inventario:lista')
    else:
        form = ProductoForm()
    return render(request, 'inventario/crear_producto.html', {'form': form, 'titulo': titulo})

@login_required
def editar_producto(request, pk):
    """Maneja la edición (GET/POST) de un producto existente."""
    producto = get_object_or_404(Producto, pk=pk)
    titulo = f"Editar Producto: {producto.nombre}"
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado.")
            return redirect('inventario:lista')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/crear_producto.html', {'form': form, 'producto': producto, 'titulo': titulo})

@login_required
def eliminar_producto(request, pk):
    """Maneja la eliminación (GET/POST) de un producto."""
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f"Producto '{nombre_producto}' eliminado.")
        return redirect('inventario:lista')
    
    # Reutiliza la plantilla genérica de confirmación de 'core'
    return render(request, 'core/confirmar_eliminar.html', {
        'object': producto,
        'cancel_url': reverse('inventario:lista')
    })

# --- API para JavaScript ---

@login_required
def get_stock_producto(request, producto_id):
    """
    Vista de API simple que devuelve el stock de un producto en formato JSON.
    Es consumida por el JavaScript del formulario 'crear_orden'.
    
    Args:
        producto_id (int): El ID del producto a consultar.
        
    Returns:
        JsonResponse: {'stock': int} o {'error': str}
    """
    try:
        producto = Producto.objects.get(pk=producto_id)
        return JsonResponse({'stock': producto.stock})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)