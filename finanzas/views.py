# finanzas/views.py
"""
Define las vistas (lógica) para la aplicación 'finanzas'.
Maneja el CRUD simple para el modelo Gasto.
"""
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Gasto
from .forms import GastoForm

@login_required
def lista_gastos(request):
    """Muestra una lista de todos los gastos registrados."""
    gastos = Gasto.objects.all().order_by('-fecha')
    return render(request, 'finanzas/lista_gastos.html', {'gastos': gastos})

@login_required
def registrar_gasto(request):
    """Maneja la creación (GET/POST) de un nuevo gasto."""
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Gasto registrado exitosamente.")
            return redirect('finanzas:lista_gastos')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else: # GET
        form = GastoForm()
    return render(request, 'finanzas/registrar_gasto.html', {'form': form})

@login_required
def editar_gasto(request, pk):
    """Maneja la edición (GET/POST) de un gasto existente."""
    gasto = get_object_or_404(Gasto, pk=pk)
    if request.method == 'POST':
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            messages.success(request, "Gasto actualizado exitosamente.")
            return redirect('finanzas:lista_gastos')
        else:
             messages.error(request, "Por favor corrige los errores en el formulario.")
    else: # GET
        form = GastoForm(instance=gasto)
    return render(request, 'finanzas/editar_gasto.html', {'form': form, 'gasto': gasto})

@login_required
def eliminar_gasto(request, pk):
    """Maneja la eliminación (GET/POST) de un gasto."""
    gasto = get_object_or_404(Gasto, pk=pk)
    if request.method == 'POST':
        # Guardar info antes de borrar para el mensaje
        fecha_gasto = gasto.fecha.strftime('%d-%m-%Y')
        monto_gasto = gasto.monto
        gasto.delete()
        messages.success(request, f"Gasto de ${monto_gasto:,.0f} del {fecha_gasto} eliminado.")
        return redirect('finanzas:lista_gastos')
    
    # Reutiliza la plantilla genérica de confirmación de 'core'
    return render(request, 'core/confirmar_eliminar.html', {
        'object': gasto,
        'cancel_url': reverse('finanzas:lista_gastos')
    })