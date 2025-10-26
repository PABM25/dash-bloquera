# core/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.models import User
from .forms import RegistroForm, EditProfileForm

# Importaciones necesarias para 'home' - AJUSTA LAS RUTAS
from datetime import date
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractYear
import json
# Asegúrate de importar los modelos necesarios desde sus nuevas apps
from ventas.models import OrdenCompra
from finanzas.models import Gasto
from recursos_humanos.models import Asistencia


# --- Vistas de Autenticación ---

class CustomLoginView(LoginView):
    template_name = 'core/login.html' # Ajustado
    redirect_authenticated_user = True

def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Has iniciado sesión.')
            return redirect('core:home') # Ajustado
    else:
        form = RegistroForm()
    return render(request, 'core/register.html', {'form': form}) # Ajustado

# --- Vista Home ---

# Función auxiliar (movida desde la antigua app/views.py)
# Asegúrate que las importaciones de OrdenCompra y Gasto sean correctas
def reporte_graficos_data():
    ventas_qs = OrdenCompra.objects.annotate(
        mes=ExtractMonth('fecha'), ano=ExtractYear('fecha')
    ).values('mes', 'ano').annotate(total_ventas=Sum('total')).order_by('ano', 'mes')

    gastos_qs = Gasto.objects.annotate(
        mes=ExtractMonth('fecha'), ano=ExtractYear('fecha')
    ).values('mes', 'ano').annotate(total_gastos=Sum('monto')).order_by('ano', 'mes')

    meses_ventas = {f"{v['ano']}-{str(v['mes']).zfill(2)}" for v in ventas_qs}
    meses_gastos = {f"{g['ano']}-{str(g['mes']).zfill(2)}" for g in gastos_qs}
    meses_etiquetas = sorted(list(meses_ventas.union(meses_gastos)))

    ventas_dict = {f"{v['ano']}-{str(v['mes']).zfill(2)}": v for v in ventas_qs}
    gastos_dict = {f"{g['ano']}-{str(g['mes']).zfill(2)}": g for g in gastos_qs}

    ventas_final = [ventas_dict.get(mes, {'total_ventas': 0}) for mes in meses_etiquetas]
    gastos_final = [gastos_dict.get(mes, {'total_gastos': 0}) for mes in meses_etiquetas]

    return meses_etiquetas, ventas_final, gastos_final

@login_required
def home(request):
    hoy = date.today()
    primer_dia_mes = hoy.replace(day=1)
    # Asegúrate que la importación de Asistencia sea correcta
    asistencia_del_mes = Asistencia.objects.filter(fecha__gte=primer_dia_mes).count()

    meses_etiquetas, ventas_mensuales, gastos_mensuales = reporte_graficos_data()

    datos_ventas_lista = [float(v.get('total_ventas', 0)) for v in ventas_mensuales]
    datos_gastos_lista = [float(g.get('total_gastos', 0)) for g in gastos_mensuales]

    total_ventas = sum(datos_ventas_lista)
    total_gastos = sum(datos_gastos_lista)

    # Evitar división por cero si no hay ventas ni gastos
    total_general = total_ventas + total_gastos
    porcentaje_ventas = (total_ventas / total_general * 100) if total_general > 0 else 0
    porcentaje_gastos = (total_gastos / total_general * 100) if total_general > 0 else 0

    context = {
        'asistencia_del_mes': asistencia_del_mes,
        'total_ventas': total_ventas,
        'total_gastos': total_gastos,
        'meses_etiquetas_json': json.dumps(meses_etiquetas),
        'datos_ventas_json': json.dumps(datos_ventas_lista),
        'datos_gastos_json': json.dumps(datos_gastos_lista),
        'porcentaje_ventas': round(porcentaje_ventas, 1),
        'porcentaje_gastos': round(porcentaje_gastos, 1),
    }
    return render(request, 'core/home.html', context) # Ajustado

# --- Vistas de Configuración de Usuario ---

@login_required
def user_settings(request):
    return render(request, 'core/user_settings.html') # Ajustado

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado!')
            return redirect('core:user_settings') # Ajustado
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'core/edit_profile.html', {'form': form}) # Ajustado

class CustomPasswordChangeView(PasswordChangeView):
    template_name='core/password_change_form.html' # Ajustado
    success_url = reverse_lazy('core:password_change_done') # Ajustado