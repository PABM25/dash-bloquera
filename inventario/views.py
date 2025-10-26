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
    # Corregido: 'inventario/inventario.html' a 'inventario/lista.html' si renombraste la plantilla, o mantenlo si no. Asumo que se llama inventario.html
    return render(request, 'inventario/inventario.html', {'productos': productos})

@login_required
def crear_producto(request):
    titulo = "Agregar Nuevo Producto"
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado.")
            # Corregido: Usar el nombre de URL correcto
            return redirect('inventario:lista')
    else:
        form = ProductoForm()
    # Corregido: 'inventario/crear_producto.html'
    return render(request, 'inventario/crear_producto.html', {'form': form, 'titulo': titulo})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    titulo = f"Editar Producto: {producto.nombre}"
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado.")
             # Corregido: Usar el nombre de URL correcto
            return redirect('inventario:lista')
    else:
        form = ProductoForm(instance=producto)
    # Corregido: 'inventario/editar_producto.html'
    return render(request, 'inventario/editar_producto.html', {'form': form, 'producto': producto, 'titulo': titulo})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f"Producto '{nombre_producto}' eliminado.")
        # Corregido: Usar el nombre de URL correcto
        return redirect('inventario:lista')
    # Reutiliza la plantilla de core para confirmar eliminación (Correcto)
    return render(request, 'core/confirmar_eliminar.html', {
        'object': producto,
         # Corregido: Usar el nombre de URL correcto
        'cancel_url': reverse('inventario:lista')
    })

# --- API para JavaScript --- (Sin cambios necesarios aquí)
@login_required
def get_stock_producto(request, producto_id):
    try:
        producto = Producto.objects.get(pk=producto_id)
        return JsonResponse({'stock': producto.stock})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)