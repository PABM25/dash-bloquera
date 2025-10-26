# recursos_humanos/views.py
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Trabajador, Asistencia
from .forms import TrabajadorForm, AsistenciaManualForm, CalculoSalarioForm
from finanzas.models import Gasto # Importar Gasto para registrar pago
from datetime import date

# --- Vistas de Trabajadores (CRUD) ---

@login_required
def lista_trabajadores(request):
    trabajadores = Trabajador.objects.all()
    return render(request, 'recursos_humanos/lista_trabajadores.html', {'trabajadores': trabajadores}) # Ajustado

@login_required
def crear_trabajador(request):
    if request.method == 'POST':
        form = TrabajadorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Trabajador creado exitosamente.")
            return redirect('recursos_humanos:lista_trabajadores') # Ajustado
    else:
        form = TrabajadorForm()
    return render(request, 'recursos_humanos/crear_trabajador.html', {'form': form}) # Ajustado

@login_required
def editar_trabajador(request, pk):
    trabajador = get_object_or_404(Trabajador, pk=pk)
    if request.method == 'POST':
        form = TrabajadorForm(request.POST, instance=trabajador)
        if form.is_valid():
            form.save()
            messages.success(request, "Trabajador actualizado exitosamente.")
            return redirect('recursos_humanos:lista_trabajadores') # Ajustado
    else:
        form = TrabajadorForm(instance=trabajador)
    return render(request, 'recursos_humanos/editar_trabajador.html', {'form': form, 'trabajador': trabajador}) # Ajustado

@login_required
def eliminar_trabajador(request, pk):
    trabajador = get_object_or_404(Trabajador, pk=pk)
    if request.method == 'POST':
        nombre_trabajador = trabajador.nombre
        trabajador.delete()
        messages.success(request, f"Trabajador '{nombre_trabajador}' eliminado exitosamente.")
        return redirect('recursos_humanos:lista_trabajadores') # Ajustado
    return render(request, 'core/confirmar_eliminar.html', { # Reutiliza plantilla core
        'object': trabajador,
        'cancel_url': reverse('recursos_humanos:lista_trabajadores') # Ajustado
    })

# --- Vistas de Asistencia y Salarios ---

@login_required
def asistencia_manual(request):
    if request.method == 'POST':
        form = AsistenciaManualForm(request.POST)
        if form.is_valid():
            trabajador = form.cleaned_data['trabajador']
            fecha = form.cleaned_data['fecha']
            tipo_proyecto = form.cleaned_data['tipo_proyecto']
            # Comprobar si ya existe
            existe, creada = Asistencia.objects.get_or_create(
                trabajador=trabajador, fecha=fecha, tipo_proyecto=tipo_proyecto
            )
            if creada:
                messages.success(request, "Asistencia registrada exitosamente.")
            else:
                messages.warning(request, "Esta asistencia ya fue registrada anteriormente.") # Cambiado a warning
            return redirect('recursos_humanos:asistencia_confirmacion') # Ajustado
        else:
            # Si el formulario no es válido, mostrar errores
             messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = AsistenciaManualForm()
    return render(request, 'recursos_humanos/asistencia_manual.html', {'form': form}) # Ajustado

@login_required
def asistencia_confirmacion(request):
    return render(request, 'recursos_humanos/asistencia_confirmacion.html') # Ajustado

@login_required
def calcular_salario(request):
    context = {}
    if request.method == 'POST':
        form = CalculoSalarioForm(request.POST)
        if form.is_valid():
            trabajador = form.cleaned_data['trabajador']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            tipo_proyecto = form.cleaned_data['tipo_proyecto']

            if trabajador.salario_por_dia is None or trabajador.salario_por_dia <= 0:
                messages.error(request, f"El trabajador {trabajador.nombre} no tiene un salario por día definido.")
                context['form'] = form # Pasar el formulario de vuelta con el error
            else:
                asistencias_qs = Asistencia.objects.filter(
                    trabajador=trabajador,
                    fecha__range=[fecha_inicio, fecha_fin],
                    tipo_proyecto=tipo_proyecto
                )
                asistencias_count = asistencias_qs.count()
                salario_total = asistencias_count * trabajador.salario_por_dia

                context['mensaje'] = f"Cálculo para {trabajador.nombre} ({fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')})"
                context['asistencias'] = asistencias_count
                context['salario_total'] = salario_total
                # Pasar datos necesarios para el formulario de registro de gasto
                context['form_data'] = {
                    'trabajador': trabajador.id,
                    'fecha_inicio': fecha_inicio.isoformat(),
                    'fecha_fin': fecha_fin.isoformat(),
                    'tipo_proyecto': tipo_proyecto,
                    'salario_total': float(salario_total) # Convertir Decimal a float para JSON/hidden input
                }
                context['form'] = form # Pasar el formulario original también
        else:
             messages.error(request, "Por favor corrige los errores en el formulario.")
             context['form'] = form # Pasar el formulario con errores
    else: # Método GET
        context['form'] = CalculoSalarioForm()

    return render(request, 'recursos_humanos/calcular_salario.html', context) # Ajustado

@login_required
def registrar_pago_gasto(request):
    if request.method == 'POST':
        trabajador_id = request.POST.get('trabajador')
        fecha_inicio_str = request.POST.get('fecha_inicio')
        fecha_fin_str = request.POST.get('fecha_fin')
        tipo_proyecto = request.POST.get('tipo_proyecto')
        salario_total_str = request.POST.get('salario_total')

        if not all([trabajador_id, fecha_inicio_str, fecha_fin_str, tipo_proyecto, salario_total_str]):
            messages.error(request, "Faltan datos para registrar el gasto.")
            return redirect('recursos_humanos:calcular_salario') # Ajustado

        try:
            trabajador = Trabajador.objects.get(pk=trabajador_id)
            salario_total = float(salario_total_str) # Ya debería ser float
            if salario_total < 0:
                 raise ValueError("Monto inválido.")

            # Crear el objeto Gasto
            Gasto.objects.create(
                fecha=date.today(),
                categoria='SALARIO',
                descripcion=f"Pago salario a {trabajador.nombre} por período {fecha_inicio_str} al {fecha_fin_str} ({tipo_proyecto})",
                monto=salario_total,
                tipo_proyecto=tipo_proyecto
            )
            messages.success(request, f"Salario de ${salario_total:,.0f} para {trabajador.nombre} registrado como Gasto.")
            return redirect('finanzas:lista_gastos') # Redirige a la lista de gastos

        except Trabajador.DoesNotExist:
            messages.error(request, "Trabajador no encontrado.")
        except ValueError:
            messages.error(request, "Monto de salario inválido.")
        except Exception as e:
            messages.error(request, f"Error inesperado al registrar el gasto: {e}")

        return redirect('recursos_humanos:calcular_salario') # Si hay error, vuelve a calcular

    # Si no es POST, redirigir
    return redirect('recursos_humanos:calcular_salario') # Ajustado