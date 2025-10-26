# inventario/views.py
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Producto
from .forms import ProductoForm

@login_required
def inventario(request):
    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'inventario/inventario.html', {'productos': productos}) # Ajustado

@login_required
def crear_producto(request):
    titulo = "Agregar Nuevo Producto"
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado.")
            return redirect('inventario:lista') # Ajustado
    else:
        form = ProductoForm()
    return render(request, 'inventario/crear_producto.html', {'form': form, 'titulo': titulo}) # Ajustado

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    titulo = f"Editar Producto: {producto.nombre}"
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado.")
            return redirect('inventario:lista') # Ajustado
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/editar_producto.html', {'form': form, 'producto': producto, 'titulo': titulo}) # Ajustado

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f"Producto '{nombre_producto}' eliminado.")
        return redirect('inventario:lista') # Ajustado
    # Reutiliza la plantilla de core para confirmar eliminación
    return render(request, 'core/confirmar_eliminar.html', { # Ajustado
        'object': producto,
        'cancel_url': reverse('inventario:lista') # Ajustado
    })

# --- API para JavaScript ---
@login_required
def get_stock_producto(request, producto_id):
    try:
        producto = Producto.objects.get(pk=producto_id)
        return JsonResponse({'stock': producto.stock})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)