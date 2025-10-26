from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from io import BytesIO
from datetime import date
from django.db.models import Sum, F, Count
from django.db.models.functions import ExtractMonth, ExtractYear
import json
from django.db import transaction
from django.contrib import messages
from django.template.loader import render_to_string
import imgkit
import pdfkit # Añadido
from django.conf import settings
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# --- Vistas Home, Reporte, Lista Ordenes, Crear Orden ---
# (Sin cambios respecto a la versión anterior, puedes mantenerlas como están)
def home(request):
    """
    Renderiza la página de inicio.
    Calcula los datos para los gráficos de ventas y gastos
    y los pasa al contexto.
    """
    hoy = date.today()
    primer_dia_mes = hoy.replace(day=1)

    asistencia_del_mes = Asistencia.objects.filter(fecha__gte=primer_dia_mes).count()
    meses_etiquetas, ventas_mensuales, gastos_mensuales = reporte_graficos_data()

    total_ventas = sum([v.get('total_ventas', 0) for v in ventas_mensuales])
    total_gastos = sum([g.get('total_gastos', 0) for g in gastos_mensuales])

    context = {
        'asistencia_del_mes': asistencia_del_mes,
        'total_ventas': total_ventas,
        'total_gastos': total_gastos,
        'meses_etiquetas_json': json.dumps(meses_etiquetas),
        'datos_ventas_json': json.dumps([float(v.get('total_ventas', 0)) for v in ventas_mensuales]),
        'datos_gastos_json': json.dumps([float(g.get('total_gastos', 0)) for g in gastos_mensuales]),
    }
    return render(request, 'app/home.html', context)

def reporte_graficos_data():
    """
    Genera los datos para los gráficos de ventas y gastos.
    Devuelve: meses_etiquetas, ventas_mensuales, gastos_mensuales
    """
    ventas_qs = OrdenCompra.objects.annotate(
        mes=ExtractMonth('fecha'),
        ano=ExtractYear('fecha')
    ).values('mes', 'ano').annotate(
        total_ventas=Sum('total')
    ).order_by('ano', 'mes')

    gastos_qs = Gasto.objects.annotate(
        mes=ExtractMonth('fecha'),
        ano=ExtractYear('fecha')
    ).values('mes', 'ano').annotate(
        total_gastos=Sum('monto')
    ).order_by('ano', 'mes')

    meses_ventas = {f"{v['ano']}-{str(v['mes']).zfill(2)}" for v in ventas_qs}
    meses_gastos = {f"{g['ano']}-{str(g['mes']).zfill(2)}" for g in gastos_qs}
    meses_etiquetas = sorted(list(meses_ventas.union(meses_gastos)))

    ventas_dict = {f"{v['ano']}-{str(v['mes']).zfill(2)}": v for v in ventas_qs}
    gastos_dict = {f"{g['ano']}-{str(g['mes']).zfill(2)}": g for g in gastos_qs}

    ventas_final = [ventas_dict.get(mes, {'total_ventas': 0}) for mes in meses_etiquetas]
    gastos_final = [gastos_dict.get(mes, {'total_gastos': 0}) for mes in meses_etiquetas]

    return meses_etiquetas, ventas_final, gastos_final

def lista_ordenes(request):
    """
    Muestra una lista de todas las órdenes de compra.
    """
    ordenes = OrdenCompra.objects.prefetch_related('detalles__producto').all().order_by('-fecha')
    return render(request, 'app/lista_ordenes.html', {'ordenes': ordenes})

def crear_orden(request):
    if request.method == 'POST':
        form = OrdenCompraForm(request.POST)
        formset = DetalleOrdenFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    orden = form.save(commit=False)
                    orden.save()

                    detalles = formset.save(commit=False)
                    total_orden = 0
                    productos_a_guardar = []
                    valid_details_count = 0

                    for i, detalle_form in enumerate(formset):
                        if formset.can_delete and formset._should_delete_form(detalle_form):
                            continue
                        if 'producto' in detalle_form.cleaned_data and detalle_form.cleaned_data.get('producto') and detalle_form.cleaned_data.get('cantidad', 0) > 0:
                            valid_details_count += 1
                            detalle = detalle_form.instance
                            producto = detalle.producto
                            if not producto.disminuir_stock(detalle.cantidad):
                                raise Exception(f"No hay suficiente stock para: {producto.nombre}")
                            total_linea = detalle.cantidad * detalle.precio_unitario
                            total_orden += total_linea
                            detalle.orden = orden
                            productos_a_guardar.append(detalle)
                        elif detalle_form.has_changed():
                             pass

                    if valid_details_count == 0:
                        raise Exception("Debes añadir al menos un producto a la orden.")

                    for detalle in productos_a_guardar:
                         detalle.save()

                    orden.total = total_orden
                    orden.save()

                    messages.success(request, f"Orden {orden.numero_venta} creada exitosamente.")
                    return redirect('detalle_orden', orden_id=orden.pk)
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = OrdenCompraForm()
        formset = DetalleOrdenFormSet()

    context = {
        'orden_form': form,
        'detalle_formset': formset
    }
    return render(request, 'app/crear_orden.html', context)

def detalle_orden(request, orden_id):
    """
    Muestra el detalle de una orden de compra específica.
    """
    orden = get_object_or_404(
        OrdenCompra.objects.prefetch_related('detalles__producto'),
        pk=orden_id
    )
    return render(request, 'app/detalle_orden.html', {'orden': orden})

# --- VISTA PDF CORREGIDA ---
def descargar_orden_pdf(request, orden_id):
    """
    Genera un PDF para descargar la orden de compra usando wkhtmltopdf.
    """
    orden = get_object_or_404(OrdenCompra.objects.prefetch_related('detalles__producto'), pk=orden_id)
    html_string = render_to_string('app/detalle_orden_render.html', {'orden': orden, 'request': request})

    try:
        options = {
            'page-size': 'A7',
            'margin-top': '5mm', 'margin-right': '5mm',
            'margin-bottom': '5mm', 'margin-left': '5mm',
            'encoding': "UTF-8",
            'enable-local-file-access': None,
            # 'no-outline': None, <-- Eliminado
            'quiet': ''
        }
        # --- CONFIGURACIÓN DE RUTA (DESCOMENTA Y AJUSTA SI ES NECESARIO) ---
        # Asegúrate que la ruta apunta a wkhtmltopdf.exe
        # path_wkhtmltopdf = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe' # EJEMPLO
        # config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        # pdf_data = pdfkit.from_string(html_string, False, options=options, configuration=config)

        # --- Si está en el PATH ---
        pdf_data = pdfkit.from_string(html_string, False, options=options)
        # Eliminamos la llamada duplicada

        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="orden_{orden.numero_venta or orden.id}.pdf"'
        return response
    except OSError as e:
        error_msg = f"Error al generar PDF: {e}. Asegúrate de que wkhtmltopdf esté instalado y en el PATH."
        print(error_msg)
        return HttpResponse(error_msg, status=500)
    except Exception as e:
        error_msg = f"Error inesperado al generar PDF: {e}"
        print(error_msg)
        return HttpResponse(error_msg, status=500)

# --- VISTA JPG CORREGIDA ---
def descargar_orden_jpg(request, orden_id):
    """
    Genera un JPG para descargar la orden de compra usando wkhtmltoimage.
    """
    orden = get_object_or_404(OrdenCompra.objects.prefetch_related('detalles__producto'), pk=orden_id)
    html_string = render_to_string('app/detalle_orden_render.html', {'orden': orden, 'request': request})

    try:
        options = {
            'format': 'jpg', 'encoding': "UTF-8", 'quality': '90',
            'enable-local-file-access': None,
            # 'no-outline': None, <-- Eliminado
            'quiet': ''
        }
        # --- CONFIGURACIÓN DE RUTA (DESCOMENTA Y AJUSTA SI ES NECESARIO) ---
        # Asegúrate que la ruta apunta a wkhtmltoimage.exe
        # path_wkhtmltoimage = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltoimage.exe' # EJEMPLO
        # config = imgkit.config(wkhtmltoimage=path_wkhtmltoimage)
        # jpg_data = imgkit.from_string(html_string, False, options=options, config=config)

        # --- Si está en el PATH ---
        jpg_data = imgkit.from_string(html_string, False, options=options)
        # Eliminamos la llamada duplicada

        response = HttpResponse(jpg_data, content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="orden_{orden.numero_venta or orden.id}.jpg"'
        return response
    except OSError as e:
        error_msg = f"Error al generar JPG: {e}. Asegúrate de que wkhtmltoimage esté instalado y en el PATH."
        print(error_msg)
        return HttpResponse(error_msg, status=500)
    except Exception as e:
        error_msg = f"Error inesperado al generar JPG: {e}"
        print(error_msg)
        return HttpResponse(error_msg, status=500)


# --- VISTA WORD (Sin cambios necesarios por este error) ---
def descargar_orden_docx(request, orden_id):
    """
    Genera un archivo Word (.docx) para descargar la orden de compra.
    """
    orden = get_object_or_404(OrdenCompra.objects.prefetch_related('detalles__producto'), pk=orden_id)
    document = Document()

    sections = document.sections
    for section in sections:
        section.top_margin = Inches(0.4)
        section.bottom_margin = Inches(0.4)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    p_empresa = document.add_paragraph()
    p_empresa.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    runner = p_empresa.add_run(
        "CONSTRUCCIONES V & G LIZ CASTILLO GARCIA SPA\n"
        "RUT: 77.858.577-4\n"
        "Dirección: Vilaco 301, Toconao\n"
        "Teléfono: +56 9 52341652" # Asegúrate que este sea el número correcto
    )
    runner.font.size = Pt(8)
    runner.bold = True
    p_empresa.paragraph_format.space_after = Pt(0)

    document.add_paragraph("---" * 12).alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_orden_info = document.add_paragraph()
    p_orden_info.add_run(f"Orden de Compra #{orden.numero_venta or orden.id}\n").bold = True
    p_orden_info.add_run(f"Cliente: {orden.cliente}\n")
    p_orden_info.add_run(f"Rut: {orden.rut or 'N/A'}\n")
    p_orden_info.add_run(f"Fecha: {orden.fecha.strftime('%d-%m-%Y %H:%M')}\n")
    p_orden_info.add_run(f"Dirección: {orden.direccion or 'N/A'}")
    for run in p_orden_info.runs:
        run.font.size = Pt(9)
    p_orden_info.paragraph_format.space_after = Pt(6)

    document.add_paragraph("---" * 12).alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_detalle_titulo = document.add_paragraph()
    p_detalle_titulo.add_run("Detalle").bold = True
    p_detalle_titulo.runs[0].font.size = Pt(10)
    p_detalle_titulo.paragraph_format.space_after = Pt(3)

    table = document.add_table(rows=1, cols=4)
    table.style = 'Table Grid'
    table.autofit = False

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Producto'
    hdr_cells[1].text = 'Cant'
    hdr_cells[2].text = 'P. Unit.'
    hdr_cells[3].text = 'Total'
    for cell in hdr_cells:
         cell.paragraphs[0].runs[0].font.bold = True
         cell.paragraphs[0].runs[0].font.size = Pt(9)
         cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    for detalle in orden.detalles.all():
        row_cells = table.add_row().cells
        precio_unit_str = f"${detalle.precio_unitario:,.0f}".replace(",",".")
        total_linea_str = f"${detalle.total_linea:,.0f}".replace(",",".")
        row_cells[0].text = detalle.producto.nombre
        row_cells[1].text = str(detalle.cantidad)
        row_cells[2].text = precio_unit_str
        row_cells[3].text = total_linea_str
        for i, cell in enumerate(row_cells):
             cell.paragraphs[0].runs[0].font.size = Pt(9)
             if i > 0:
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    table.columns[0].width = Inches(2.8)
    table.columns[1].width = Inches(0.5)
    table.columns[2].width = Inches(0.9)
    table.columns[3].width = Inches(1.0)

    document.add_paragraph("---" * 12).alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_total = document.add_paragraph()
    p_total.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    total_str = f"${orden.total:,.0f}".replace(",",".")
    runner_total = p_total.add_run(f"Total a Pagar: {total_str}")
    runner_total.bold = True
    runner_total.font.size = Pt(11)
    p_total.paragraph_format.space_after = Pt(0)

    document.add_paragraph("---" * 12).alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_gracias = document.add_paragraph(
        "¡Gracias por su compra!\nEsperamos atenderle pronto."
    )
    p_gracias.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_gracias.runs[0].font.size = Pt(8)

    f = BytesIO()
    document.save(f)
    f.seek(0)
    response = HttpResponse(
        f.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="orden_{orden.numero_venta or orden.id}.docx"'
    f.close()
    return response

# --- Vistas restantes (sin cambios) ---
def lista_trabajadores(request):
    trabajadores = Trabajador.objects.all()
    return render(request, 'app/lista_trabajadores.html', {'trabajadores': trabajadores})

def crear_trabajador(request):
    if request.method == 'POST':
        form = TrabajadorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Trabajador creado exitosamente.")
            return redirect('lista_trabajadores')
    else:
        form = TrabajadorForm()
    return render(request, 'app/crear_trabajador.html', {'form': form})

def asistencia_manual(request):
    if request.method == 'POST':
        form = AsistenciaManualForm(request.POST)
        if form.is_valid():
            trabajador = form.cleaned_data['trabajador']
            fecha = form.cleaned_data['fecha']
            tipo_proyecto = form.cleaned_data['tipo_proyecto']
            if not Asistencia.objects.filter(trabajador=trabajador, fecha=fecha, tipo_proyecto=tipo_proyecto).exists():
                Asistencia.objects.create(
                    trabajador=trabajador, fecha=fecha, tipo_proyecto=tipo_proyecto
                )
                messages.success(request, "Asistencia registrada exitosamente.")
                return redirect('asistencia_confirmacion')
            else:
                messages.error(request, "Esta asistencia ya fue registrada.")
    else:
        form = AsistenciaManualForm()
    return render(request, 'app/asistencia_manual.html', {'form': form})

def asistencia_confirmacion(request):
    return render(request, 'app/asistencia_confirmacion.html')

def inventario(request):
    productos = Producto.objects.all().order_by('nombre')
    return render(request, 'app/inventario.html', {'productos': productos})

def crear_producto(request):
    titulo = "Agregar Nuevo Producto"
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado exitosamente.")
            return redirect('inventario')
    else:
        form = ProductoForm()
    return render(request, 'app/crear_producto.html', {'form': form, 'titulo': titulo})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    titulo = f"Editar Producto: {producto.nombre}"
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado exitosamente.")
            return redirect('inventario')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'app/editar_producto.html', {'form': form, 'producto': producto, 'titulo': titulo})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f"Producto '{nombre_producto}' eliminado exitosamente.")
        return redirect('inventario')
    messages.warning(request, "Acción no permitida.")
    return redirect('inventario')

def lista_gastos(request):
    gastos = Gasto.objects.all().order_by('-fecha')
    return render(request, 'app/lista_gastos.html', {'gastos': gastos})

def registrar_gasto(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Gasto registrado exitosamente.")
            return redirect('lista_gastos')
    else:
        form = GastoForm()
    return render(request, 'app/registrar_gasto.html', {'form': form})