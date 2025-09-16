from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import *
from reportlab.pdfgen import canvas
import qrcode
from io import BytesIO
from datetime import datetime, timedelta, date
from django.db.models import Sum, F, Count
from django.db.models.functions import ExtractMonth, ExtractYear
import json
from django.core.serializers.json import DjangoJSONEncoder

def home(request):
    """
    Renderiza la página de inicio.
    Calcula los datos para los gráficos de ventas y gastos
    y los pasa al contexto.
    """
    hoy = date.today()
    primer_dia_mes = hoy.replace(day=1)

    # Contar la asistencia del mes
    asistencia_del_mes = Asistencia.objects.filter(fecha__gte=primer_dia_mes).count()

    # Obtener los datos para los gráficos de ventas y gastos
    meses_etiquetas, ventas_mensuales, gastos_mensuales = reporte_graficos_data()

   

    # Total de ventas y gastos
    total_ventas = sum([v['total_ventas'] for v in ventas_mensuales])
    total_gastos = sum([g['total_gastos'] for g in gastos_mensuales])

    context = {
        'asistencia_del_mes': asistencia_del_mes,
        'total_ventas': total_ventas,
        'total_gastos': total_gastos,
        'meses_etiquetas_json': json.dumps(meses_etiquetas),
        'datos_ventas_json': json.dumps([float(v['total_ventas']) for v in ventas_mensuales]),
        'datos_gastos_json': json.dumps([float(g['total_gastos']) for g in gastos_mensuales]),
    }
    return render(request, 'app/home.html', context)


def reporte_graficos_data():
    """
    Genera los datos para los gráficos de ventas y gastos.
    Devuelve: meses_etiquetas, ventas_mensuales, gastos_mensuales
    """
    # Ventas
    ventas_qs = OrdenCompra.objects.annotate(
        mes=ExtractMonth('fecha'),
        ano=ExtractYear('fecha')
    ).values('mes', 'ano').annotate(
        total_ventas=Sum('total')
    ).order_by('ano', 'mes')

    # Gastos
    gastos_qs = Gasto.objects.annotate(
        mes=ExtractMonth('fecha'),
        ano=ExtractYear('fecha')
    ).values('mes', 'ano').annotate(
        total_gastos=Sum('monto')
    ).order_by('ano', 'mes')

    # Crear etiquetas de meses (ej: '2025-01', '2025-02')
    meses_etiquetas = [f"{g['ano']}-{str(g['mes']).zfill(2)}" for g in ventas_qs]

    return meses_etiquetas, list(ventas_qs), list(gastos_qs)


def lista_ordenes(request):
    """
    Muestra una lista de todas las órdenes de compra.
    """
    ordenes = OrdenCompra.objects.all().order_by('-fecha')
    return render(request, 'app/lista_ordenes.html', {'ordenes': ordenes})

def crear_orden(request):
    """
    Crea una nueva orden de compra.
    Valida el stock del producto antes de guardar.
    """
    if request.method == 'POST':
        form = OrdenCompraForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            
            # Validar y disminuir el stock del producto
            producto = orden.producto
            cantidad = orden.cantidad
            
            if producto.stock >= cantidad:
                orden.total = orden.cantidad * orden.precio_unitario
                orden.save()
                producto.disminuir_stock(cantidad)
                return redirect('lista_ordenes')
            else:
                form.add_error('cantidad', 'No hay suficiente stock para este producto.')
    else:
        form = OrdenCompraForm()
    
    return render(request, 'app/crear_orden.html', {'form': form})

def detalle_orden(request, orden_id):
    """
    Muestra el detalle de una orden de compra específica.
    """
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    return render(request, 'app/detalle_orden.html', {'orden': orden})

def imprimir_orden(request, orden_id):
    """
    Genera un PDF para imprimir la orden de compra.
    """
    orden = get_object_or_404(OrdenCompra, pk=orden_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="orden_{orden.numero_venta}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Contenido del PDF
    p.drawString(100, 750, f"Orden de Compra: {orden.numero_venta}")
    p.drawString(100, 730, f"Fecha: {orden.fecha.strftime('%d-%m-%Y')}")
    p.drawString(100, 710, f"Cliente: {orden.cliente}")
    p.drawString(100, 690, f"Dirección: {orden.direccion}")
    p.drawString(100, 670, f"Producto: {orden.producto.nombre}")
    p.drawString(100, 650, f"Cantidad: {orden.cantidad}")
    p.drawString(100, 630, f"Precio Unitario: ${orden.precio_unitario}")
    p.drawString(100, 610, f"Total: ${orden.total}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

# Vistas para Trabajadores y Asistencia
def lista_trabajadores(request):
    """
    Muestra una lista de todos los trabajadores.
    """
    trabajadores = Trabajador.objects.all()
    return render(request, 'app/lista_trabajadores.html', {'trabajadores': trabajadores})

def crear_trabajador(request):
    """
    Crea un nuevo trabajador.
    """
    if request.method == 'POST':
        form = TrabajadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_trabajadores')
    else:
        form = TrabajadorForm()
    
    return render(request, 'app/crear_trabajador.html', {'form': form})

def generar_qr_trabajador(request, trabajador_id):
    """
    Genera un código QR para un trabajador específico.
    """
    trabajador = get_object_or_404(Trabajador, pk=trabajador_id)
    
    # La información codificada en el QR es el RUT del trabajador
    qr_data = trabajador.rut
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    
    return HttpResponse(buffer.getvalue(), content_type="image/png")

def marcar_asistencia(request):
    """
    Registra la asistencia de un trabajador mediante un código QR.
    """
    rut = request.GET.get('rut')
    mensaje = ""
    tipo_proyecto_opciones = Trabajador.TIPO_PROYECTO
    
    if rut:
        try:
            trabajador = Trabajador.objects.get(rut=rut)
            # Verificar si ya existe un registro de asistencia para hoy
            if not Asistencia.objects.filter(trabajador=trabajador, fecha=date.today()).exists():
                # Marcar la asistencia y guardar
                asistencia = Asistencia.objects.create(trabajador=trabajador, tipo_proyecto=trabajador.tipo_proyecto)
                mensaje = f"Asistencia de {trabajador.nombre} marcada con éxito para el proyecto {trabajador.tipo_proyecto}."
            else:
                mensaje = f"La asistencia de {trabajador.nombre} ya ha sido marcada hoy."
        except Trabajador.DoesNotExist:
            mensaje = "Trabajador no encontrado. Por favor, intente de nuevo."
    
    context = {
        'mensaje': mensaje,
        'tipo_proyecto_opciones': tipo_proyecto_opciones
    }
    return render(request, 'app/marcar_asistencia.html', context)

def asistencia_manual(request):
    """
    Registra la asistencia de forma manual.
    """
    if request.method == 'POST':
        form = AsistenciaManualForm(request.POST)
        if form.is_valid():
            asistencia = form.save(commit=False)
            
            # Obtener el tipo de proyecto del trabajador si no se especificó en el form
            if not asistencia.tipo_proyecto:
                asistencia.tipo_proyecto = asistencia.trabajador.tipo_proyecto
            
            asistencia.save()
            return redirect('asistencia_confirmacion')
    else:
        form = AsistenciaManualForm()
        
    return render(request, 'app/asistencia_manual.html', {'form': form})

def asistencia_confirmacion(request):
    """
    Muestra un mensaje de confirmación después de marcar la asistencia.
    """
    mensaje = "La asistencia ha sido registrada exitosamente."
    return render(request, 'app/asistencia_confirmacion.html', {'mensaje': mensaje})



# Vistas para Inventario
def inventario(request):
    """
    Muestra el inventario de productos.
    """
    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'app/inventario.html', {'productos': productos})

def crear_producto(request):
    """
    Crea un nuevo producto en el inventario.
    """
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = ProductoForm()
    
    return render(request, 'app/crear_producto.html', {'form': form})

def editar_producto(request, pk):
    """
    Edita un producto existente.
    """
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'app/editar_producto.html', {'form': form, 'producto': producto})

def eliminar_producto(request, pk):
    """
    Elimina un producto del inventario.
    """
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('inventario')
    
    return render(request, 'app/eliminar_producto.html', {'producto': producto})

# Vistas para Gastos
def lista_gastos(request):
    """
    Muestra una lista de todos los gastos registrados.
    """
    gastos = Gasto.objects.all().order_by('-fecha')
    return render(request, 'app/lista_gastos.html', {'gastos': gastos})


def registrar_gasto(request):
    """
    Registra un nuevo gasto.
    """
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_gastos')
    else:
        form = GastoForm()
        
    return render(request, 'app/registrar_gasto.html', {'form': form})

def gastos_por_categoria(request):
    """
    Muestra un resumen de los gastos por categoría.
    """
    gastos_resumen = Gasto.objects.values('categoria').annotate(total=Sum('monto')).order_by('categoria')
    return render(request, 'app/gastos_por_categoria.html', {'gastos_resumen': gastos_resumen})


def confirmacion_accion(request):
    """
    Vista genérica para mostrar un mensaje de confirmación.
    """
    mensaje = request.GET.get('mensaje', 'Acción realizada con éxito.')
    return render(request, 'app/confirmacion_accion.html', {'mensaje': mensaje})
