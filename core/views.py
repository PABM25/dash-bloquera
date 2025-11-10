# core/views.py
"""
Define las vistas para la aplicación 'core'.

Esto incluye la página principal (dashboard), las vistas de autenticación
(login, registro) y las vistas de configuración de perfil de usuario.
"""

# --- Importaciones de Django ---
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.models import User

# --- Importaciones de Formularios Locales ---
from .forms import RegistroForm, EditProfileForm

# --- Importaciones para el Dashboard ---
from datetime import date
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractYear
import json
# Importación de modelos de otras apps (clave para el dashboard)
from ventas.models import OrdenCompra
from finanzas.models import Gasto
from recursos_humanos.models import Asistencia


# --- Vistas de Autenticación ---

class CustomLoginView(LoginView):
    """
    Vista personalizada para el login.
    Simplemente especifica la plantilla a usar y redirige
    a los usuarios que ya están autenticados.
    """
    template_name = 'core/login.html'
    redirect_authenticated_user = True

def register(request):
    """
    Maneja el registro de un nuevo usuario.
    Si el método es POST y el formulario es válido, crea el usuario,
    lo autentica automáticamente (login) y lo redirige al 'home'.
    """
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Autentica al usuario recién registrado
            messages.success(request, '¡Registro exitoso! Has iniciado sesión.')
            return redirect('core:home')
    else: # Método GET
        form = RegistroForm()
    return render(request, 'core/register.html', {'form': form})

# --- Vista Home (Dashboard) ---

def reporte_graficos_data():
    """
    Función auxiliar para obtener y procesar los datos
    de los gráficos de tendencias (Utilidad vs Gastos).
    """
    # 1. Obtener utilidad agrupada por mes/año
    ventas_qs = OrdenCompra.objects.annotate(
        mes=ExtractMonth('fecha'), ano=ExtractYear('fecha')
    ).values('mes', 'ano').annotate(total_utilidad_mes=Sum('total_utilidad')).order_by('ano', 'mes')

    # 2. Obtener gastos agrupados por mes/año
    gastos_qs = Gasto.objects.annotate(
        mes=ExtractMonth('fecha'), ano=ExtractYear('fecha')
    ).values('mes', 'ano').annotate(total_gastos=Sum('monto')).order_by('ano', 'mes')

    # 3. Crear un conjunto unificado de todas las etiquetas
    meses_ventas = {f"{v['ano']}-{str(v['mes']).zfill(2)}" for v in ventas_qs}
    meses_gastos = {f"{g['ano']}-{str(g['mes']).zfill(2)}" for g in gastos_qs}
    meses_etiquetas = sorted(list(meses_ventas.union(meses_gastos)))

    # 4. Convertir los QuerySets en diccionarios para acceso rápido
    ventas_dict = {f"{v['ano']}-{str(v['mes']).zfill(2)}": v for v in ventas_qs}
    gastos_dict = {f"{g['ano']}-{str(g['mes']).zfill(2)}": g for g in gastos_qs}

    # 5. Crear las listas finales de datos
    ventas_final = [ventas_dict.get(mes, {'total_utilidad_mes': 0}) for mes in meses_etiquetas]
    gastos_final = [gastos_dict.get(mes, {'total_gastos': 0}) for mes in meses_etiquetas]

    return meses_etiquetas, ventas_final, gastos_final

@login_required # Proteger la vista, solo para usuarios autenticados
def home(request):
    """
    Vista principal del Dashboard.
    Recopila todos los datos para las tarjetas KPI y los gráficos.
    """
    # --- KPIs (Indicadores Clave) ---
    hoy = date.today()
    primer_dia_mes = hoy.replace(day=1)
    # KPI 1: Asistencias del mes
    asistencia_del_mes = Asistencia.objects.filter(fecha__gte=primer_dia_mes).count()

    # --- Datos de Gráficos ---
    meses_etiquetas, ventas_mensuales, gastos_mensuales = reporte_graficos_data() 

    datos_utilidad_lista = [float(v.get('total_utilidad_mes', 0)) for v in ventas_mensuales]
    datos_gastos_lista = [float(g.get('total_gastos', 0)) for g in gastos_mensuales]

    # --- CÁLCULOS DE KPI MODIFICADOS ---
    
    # 1. Totales de Ventas (Ingresos)
    total_ingresos_historico = OrdenCompra.objects.aggregate(Sum('total'))['total__sum'] or 0
    
    # 2. Total Dinero Cobrado (Flujo de Caja)
    total_dinero_cobrado = OrdenCompra.objects.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0
    
    # 3. Total Cuentas por Cobrar (Pendiente)
    total_cuentas_por_cobrar = total_ingresos_historico - total_dinero_cobrado
    
    # 4. Total Utilidad (Rentabilidad)
    total_utilidad_historica = sum(datos_utilidad_lista)
    
    # 5. Total Gastos (Egresos)
    total_gastos = sum(datos_gastos_lista)
    
    # --- FIN DE CÁLCULOS DE KPI ---


    # Cálculo de porcentajes para gráfico de dona (Utilidad vs Gastos)
    total_comparativo = total_utilidad_historica + total_gastos
    porcentaje_utilidad = (total_utilidad_historica / total_comparativo * 100) if total_comparativo > 0 else 0
    porcentaje_gastos = (total_gastos / total_comparativo * 100) if total_comparativo > 0 else 0


    # --- Contexto para la Plantilla ---
    context = {
        'asistencia_del_mes': asistencia_del_mes,
        
        # --- NUEVOS VALORES DE CONTEXTO ---
        'total_ingresos': total_ingresos_historico, 
        'total_dinero_cobrado': total_dinero_cobrado,
        'total_cuentas_por_cobrar': total_cuentas_por_cobrar,
        'total_utilidad': total_utilidad_historica, 
        'total_gastos': total_gastos,
        # --- FIN DE NUEVOS VALORES ---
        
        'meses_etiquetas_json': json.dumps(meses_etiquetas),
        'datos_utilidad_json': json.dumps(datos_utilidad_lista), 
        'datos_gastos_json': json.dumps(datos_gastos_lista),
        
        'porcentaje_utilidad': round(porcentaje_utilidad, 1), 
        'porcentaje_gastos': round(porcentaje_gastos, 1),
    }
    return render(request, 'core/home.html', context)

# --- Vistas de Configuración de Usuario ---

@login_required
def user_settings(request):
    """Muestra la página principal de configuración de cuenta."""
    return render(request, 'core/user_settings.html')

@login_required
def edit_profile(request):
    """
    Maneja la edición del perfil del usuario (nombre, email, etc.).
    Usa el formulario 'EditProfileForm'.
    """
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado!')
            return redirect('core:user_settings')
    else: # Método GET
        form = EditProfileForm(instance=request.user)
    return render(request, 'core/edit_profile.html', {'form': form})

class CustomPasswordChangeView(PasswordChangeView):
    """
    Vista personalizada para cambiar la contraseña.
    Solo define la plantilla y la URL de éxito.
    """
    template_name='core/password_change_form.html'
    success_url = reverse_lazy('core:password_change_done')