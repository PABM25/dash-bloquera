# finanzas/views.py
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Gasto
from .forms import GastoForm

@login_required
def lista_gastos(request):
    gastos = Gasto.objects.all().order_by('-fecha') # Orden definido en Meta
    return render(request, 'finanzas/lista_gastos.html', {'gastos': gastos}) # Ajustado

@login_required
def registrar_gasto(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Gasto registrado exitosamente.")
            return redirect('finanzas:lista_gastos') # Ajustado
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = GastoForm()
    return render(request, 'finanzas/registrar_gasto.html', {'form': form}) # Ajustado

@login_required
def editar_gasto(request, pk):
    gasto = get_object_or_404(Gasto, pk=pk)
    if request.method == 'POST':
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            messages.success(request, "Gasto actualizado exitosamente.")
            return redirect('finanzas:lista_gastos') # Ajustado
        else:
             messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = GastoForm(instance=gasto)
    # Pasar 'gasto' al contexto es útil si quieres mostrar info extra en la plantilla
    return render(request, 'finanzas/editar_gasto.html', {'form': form, 'gasto': gasto}) # Ajustado

@login_required
def eliminar_gasto(request, pk):
    gasto = get_object_or_404(Gasto, pk=pk)
    if request.method == 'POST':
        # Guardar info antes de borrar para el mensaje
        fecha_gasto = gasto.fecha.strftime('%d-%m-%Y')
        monto_gasto = gasto.monto
        gasto.delete()
        messages.success(request, f"Gasto de ${monto_gasto:,.0f} del {fecha_gasto} eliminado.")
        return redirect('finanzas:lista_gastos') # Ajustado
    return render(request, 'core/confirmar_eliminar.html', { # Reutiliza plantilla core
        'object': gasto, # Pasar el objeto gasto para mostrar su info
        'cancel_url': reverse('finanzas:lista_gastos') # Ajustado
    })