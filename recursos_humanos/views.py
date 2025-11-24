# recursos_humanos/views.py
"""
Maneja la lógica de las vistas para la aplicación 'recursos_humanos'.

Incluye:
- CRUD para el modelo Trabajador.
- Registro manual de Asistencia (evitando duplicados).
- Cálculo de Salario basado en asistencias en un rango de fechas.
- Registro del pago de salario como un Gasto en la app 'finanzas'.
"""

# --- Importaciones de Django ---
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import JsonResponse # <-- ¡IMPORTACIÓN AÑADIDA!
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date

# --- Importaciones de Modelos y Forms ---
from .models import Trabajador, Asistencia
from .forms import TrabajadorForm, AsistenciaManualForm, CalculoSalarioForm
from finanzas.models import Gasto # Importación clave para cruzar apps

# --- Vistas de Trabajadores (CRUD) ---

@login_required
def lista_trabajadores(request):
    """Muestra una lista de todos los trabajadores."""
    trabajadores = Trabajador.objects.all()
    return render(request, 'recursos_humanos/lista_trabajadores.html', {'trabajadores': trabajadores})

@login_required
def crear_trabajador(request):
    """Maneja la creación (GET/POST) de un nuevo trabajador."""
    if request.method == 'POST':
        form = TrabajadorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Trabajador creado exitosamente.")
            return redirect('recursos_humanos:lista_trabajadores')
    else:
        form = TrabajadorForm()
    return render(request, 'recursos_humanos/crear_trabajador.html', {'form': form})

@login_required
def editar_trabajador(request, pk):
    """Maneja la edición (GET/POST) de un trabajador existente."""
    trabajador = get_object_or_404(Trabajador, pk=pk)
    if request.method == 'POST':
        form = TrabajadorForm(request.POST, instance=trabajador)
        if form.is_valid():
            form.save()
            messages.success(request, "Trabajador actualizado exitosamente.")
            return redirect('recursos_humanos:lista_trabajadores')
    else:
        form = TrabajadorForm(instance=trabajador)
    return render(request, 'recursos_humanos/editar_trabajador.html', {'form': form, 'trabajador': trabajador})

@login_required
def eliminar_trabajador(request, pk):
    """Maneja la eliminación (GET/POST) de un trabajador."""
    trabajador = get_object_or_404(Trabajador, pk=pk)
    if request.method == 'POST':
        nombre_trabajador = trabajador.nombre
        trabajador.delete()
        messages.success(request, f"Trabajador '{nombre_trabajador}' eliminado exitosamente.")
        return redirect('recursos_humanos:lista_trabajadores')
    
    # Reutiliza la plantilla genérica de confirmación de 'core'
    return render(request, 'core/confirmar_eliminar.html', {
        'object': trabajador,
        'cancel_url': reverse('recursos_humanos:lista_trabajadores')
    })

# --- Vistas de Asistencia y Salarios ---

@login_required
def asistencia_manual(request):
    """
    Registra manualmente una asistencia para un trabajador en una fecha.
    Utiliza 'get_or_create' para evitar registrar duplicados.
    """
    if request.method == 'POST':
        form = AsistenciaManualForm(request.POST)
        if form.is_valid():
            trabajador = form.cleaned_data['trabajador']
            fecha = form.cleaned_data['fecha']
            tipo_proyecto = form.cleaned_data['tipo_proyecto']
            
            # get_or_create previene duplicados (basado en 'unique_together' del modelo)
            asistencia, creada = Asistencia.objects.get_or_create(
                trabajador=trabajador, 
                fecha=fecha, 
                tipo_proyecto=tipo_proyecto
            )
            
            if creada:
                messages.success(request, "Asistencia registrada exitosamente.")
            else:
                messages.warning(request, "Esta asistencia ya fue registrada anteriormente.")
            
            return redirect('recursos_humanos:asistencia_confirmacion')
        else:
             messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = AsistenciaManualForm()
    return render(request, 'recursos_humanos/asistencia_manual.html', {'form': form})

@login_required
def asistencia_confirmacion(request):
    """Página de "éxito" simple mostrada después de registrar asistencia."""
    return render(request, 'recursos_humanos/asistencia_confirmacion.html')

@login_required
def calcular_salario(request):
    """
    Calcula el salario de un trabajador en un rango de fechas.

    Esta vista no guarda nada, solo calcula y muestra el resultado.
    También prepara un formulario oculto para que el usuario pueda
    confirmar y enviar estos datos a la vista 'registrar_pago_gasto'.
    """
    context = {}
    if request.method == 'POST':
        form = CalculoSalarioForm(request.POST)
        if form.is_valid():
            trabajador = form.cleaned_data['trabajador']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            tipo_proyecto = form.cleaned_data['tipo_proyecto']

            # Validar que el trabajador tenga un salario/día asignado
            if trabajador.salario_por_dia is None or trabajador.salario_por_dia <= 0:
                messages.error(request, f"El trabajador {trabajador.nombre} no tiene un salario por día definido.")
                context['form'] = form
            else:
                # 1. Contar las asistencias en el rango
                asistencias_qs = Asistencia.objects.filter(
                    trabajador=trabajador,
                    fecha__range=[fecha_inicio, fecha_fin],
                    tipo_proyecto=tipo_proyecto
                )
                asistencias_count = asistencias_qs.count()
                
                # 2. Calcular salario
                salario_total = asistencias_count * trabajador.salario_por_dia

                # 3. Preparar contexto para el template
                context['mensaje'] = f"Cálculo para {trabajador.nombre} ({fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')})"
                context['asistencias'] = asistencias_count
                context['salario_total'] = salario_total
                
                # 4. Pasar los datos al formulario 'registrar_pago_gasto'
                context['form_data'] = {
                    'trabajador': trabajador.id,
                    'fecha_inicio': fecha_inicio.isoformat(),
                    'fecha_fin': fecha_fin.isoformat(),
                    'tipo_proyecto': tipo_proyecto,
                    'salario_total': float(salario_total) # Convertir Decimal a float
                }
                context['form'] = form
        else:
             messages.error(request, "Por favor corrige los errores en el formulario.")
             context['form'] = form
    else: # Método GET
        context['form'] = CalculoSalarioForm()

    return render(request, 'recursos_humanos/calcular_salario.html', context)

@login_required
def registrar_pago_gasto(request):
    """
    Recibe un POST (desde 'calcular_salario') y crea un registro
    en el modelo 'Gasto' de la app 'finanzas'.
    """
    if request.method == 'POST':
        # 1. Obtener datos del formulario POST
        trabajador_id = request.POST.get('trabajador')
        fecha_inicio_str = request.POST.get('fecha_inicio')
        fecha_fin_str = request.POST.get('fecha_fin')
        tipo_proyecto = request.POST.get('tipo_proyecto')
        salario_total_str = request.POST.get('salario_total')

        # 2. Validar que todos los datos necesarios llegaron
        if not all([trabajador_id, fecha_inicio_str, fecha_fin_str, tipo_proyecto, salario_total_str]):
            messages.error(request, "Faltan datos para registrar el gasto.")
            return redirect('recursos_humanos:calcular_salario')

        try:
            trabajador = Trabajador.objects.get(pk=trabajador_id)
            salario_total = float(salario_total_str)
            if salario_total < 0:
                 raise ValueError("Monto inválido.")

            # 3. Crear el Gasto en la app 'finanzas'
            Gasto.objects.create(
                fecha=date.today(), # Fecha del pago es hoy
                categoria='SALARIO', # Categoría fija
                descripcion=f"Pago salario a {trabajador.nombre} por período {fecha_inicio_str} al {fecha_fin_str} ({tipo_proyecto})",
                monto=salario_total,
                tipo_proyecto=tipo_proyecto
            )
            messages.success(request, f"Salario de ${salario_total:,.0f} para {trabajador.nombre} registrado como Gasto.")
            return redirect('finanzas:lista_gastos') # Redirigir a la lista de gastos

        except Trabajador.DoesNotExist:
            messages.error(request, "Trabajador no encontrado.")
        except ValueError:
            messages.error(request, "Monto de salario inválido.")
        except Exception as e:
            messages.error(request, f"Error inesperado al registrar el gasto: {e}")

        # Si hay error, volver a la página de cálculo
        return redirect('recursos_humanos:calcular_salario')

    # Si no es POST, redirigir
    return redirect('recursos_humanos:calcular_salario')


# --- VISTAS DEL CALENDARIO (AÑADIDAS AL FINAL) ---

@login_required
def calendario_asistencia(request):
    """
    Muestra la página HTML que contendrá el calendario.
    """
    return render(request, 'recursos_humanos/calendario_asistencia.html')


@login_required
def asistencia_feed(request):
    """
    Esta es la vista de API que FullCalendar llamará.
    Devuelve las asistencias en formato JSON.
    """
    # FullCalendar envía las fechas 'start' y 'end' de la vista actual
    start = request.GET.get('start')
    end = request.GET.get('end')

    if not start or not end:
        return JsonResponse({'error': 'Faltan parámetros start/end'}, status=400)

    # Cargar asistencias con el trabajador relacionado para optimizar
    asistencias = Asistencia.objects.filter(
        fecha__range=[start, end]
    ).select_related('trabajador')

    eventos = []
    for asistencia in asistencias:
        # Creamos un "evento" por cada asistencia registrada
        eventos.append({
            'title': f'{asistencia.trabajador.nombre} ({asistencia.get_tipo_proyecto_display()})',
            'start': asistencia.fecha.isoformat(), # Formato YYYY-MM-DD
            'allDay': True,
            # (Opcional) Asignar un color por tipo de proyecto
            'color': '#28a745' if asistencia.tipo_proyecto == 'CONSTRUCTORA' else '#17a2b8'
        })

    # 'safe=False' es necesario porque estamos devolviendo una lista
    return JsonResponse(eventos, safe=False)