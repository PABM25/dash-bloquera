# ventas/views.py
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, JsonResponse # JsonResponse no se usa aquí pero podría ser útil
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import OrdenCompra, DetalleOrden, Producto # Importar Producto
from .forms import OrdenCompraForm, DetalleOrdenFormSet
from io import BytesIO
from django.template.loader import render_to_string
import pdfkit
import imgkit
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

@login_required
def lista_ordenes(request):
    ordenes = OrdenCompra.objects.prefetch_related('detalles__producto').all().order_by('-fecha')
    return render(request, 'ventas/lista_ordenes.html', {'ordenes': ordenes}) # Ajustado

@login_required
@transaction.atomic # Asegura que la creación de orden y detalles sea atómica
def crear_orden(request):
    if request.method == 'POST':
        orden_form = OrdenCompraForm(request.POST)
        detalle_formset = DetalleOrdenFormSet(request.POST, prefix='detalles') # Añadir prefix

        if orden_form.is_valid() and detalle_formset.is_valid():
            try:
                orden = orden_form.save(commit=False)
                # No guardamos aún, necesitamos el total
                # orden.save() # <-- Quitar esto temporalmente

                detalles_instancias = detalle_formset.save(commit=False)
                total_orden = 0
                productos_a_actualizar = [] # Para actualizar stock al final
                detalles_a_guardar = []
                valid_details_count = 0

                for form in detalle_formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        producto = form.cleaned_data.get('producto')
                        cantidad = form.cleaned_data.get('cantidad')
                        precio = form.cleaned_data.get('precio_unitario')

                        if producto and cantidad and cantidad > 0 and precio is not None:
                            valid_details_count += 1
                            detalle = form.instance # Usar instancia del formset
                            # Verificar stock ANTES de proceder
                            producto_db = Producto.objects.get(pk=producto.pk) # Obtener estado actual
                            if producto_db.stock < cantidad:
                                raise Exception(f"No hay suficiente stock para: {producto.nombre} (disponible: {producto_db.stock})")

                            total_linea = cantidad * precio
                            total_orden += total_linea
                            # Añadir a listas para guardar/actualizar después
                            detalles_a_guardar.append(detalle)
                            productos_a_actualizar.append({'producto': producto_db, 'cantidad': cantidad}) # Guardar obj de DB y cantidad

                if valid_details_count == 0:
                    raise Exception("Debes añadir al menos un producto válido a la orden.")

                # Ahora sí guardamos la orden y asignamos el total
                orden.total = total_orden
                orden.save() # Ahora la orden tiene ID y total

                # Asociar detalles y guardar
                for detalle in detalles_a_guardar:
                    detalle.orden = orden # Asignar la orden guardada
                    detalle.save()

                # Actualizar stock
                for item in productos_a_actualizar:
                    item['producto'].disminuir_stock(item['cantidad']) # Usar método del modelo

                # Guardar relaciones ManyToMany del formset (si las hubiera)
                detalle_formset.save_m2m()

                messages.success(request, f"Orden {orden.numero_venta} creada exitosamente.")
                return redirect('ventas:detalle_orden', orden_id=orden.pk) # Ajustado

            except Exception as e:
                messages.error(request, f"Error al crear la orden: {e}")
                # No es necesario volver a renderizar aquí si usamos transaction.atomic
                # La transacción se revierte automáticamente en caso de excepción

    else: # Método GET
        orden_form = OrdenCompraForm()
        detalle_formset = DetalleOrdenFormSet(prefix='detalles') # Añadir prefix

    context = {
        'orden_form': orden_form,
        'detalle_formset': detalle_formset
    }
    return render(request, 'ventas/crear_orden.html', context) # Ajustado


@login_required
def detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra.objects.prefetch_related('detalles__producto'), pk=orden_id)
    return render(request, 'ventas/detalle_orden.html', {'orden': orden}) # Ajustado

# --- Vistas de Descarga ---
# (Mantenidas aquí ya que dependen directamente de OrdenCompra)

@login_required
def descargar_orden_pdf(request, orden_id):
    orden = get_object_or_404(OrdenCompra.objects.prefetch_related('detalles__producto'), pk=orden_id)
    # Usa la plantilla renderizada desde la app 'ventas'
    html_string = render_to_string('ventas/detalle_orden_render.html', {'orden': orden, 'request': request}) # Ajustado
    try:
        # Opciones para pdfkit (asegúrate que wkhtmltopdf esté instalado y en el PATH)
        options = {
            'page-size': 'A7', # Tamaño ticket pequeño
            'margin-top': '5mm',
            'margin-right': '5mm',
            'margin-bottom': '5mm',
            'margin-left': '5mm',
            'encoding': "UTF-8",
            'enable-local-file-access': None, # Necesario para cargar CSS/imágenes locales si usas rutas absolutas
            'quiet': '' # Suprime salida en consola
        }
        pdf_data = pdfkit.from_string(html_string, False, options=options)
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="orden_{orden.numero_venta or orden.id}.pdf"'
        return response
    except Exception as e:
        print(f"Error al generar PDF: {e}")
        messages.error(request, f"Error al generar PDF: {e}. Asegúrate que wkhtmltopdf esté instalado.")
        return redirect('ventas:detalle_orden', orden_id=orden.pk) # Ajustado


@login_required
def descargar_orden_jpg(request, orden_id):
    orden = get_object_or_404(OrdenCompra.objects.prefetch_related('detalles__producto'), pk=orden_id)
    # Usa la plantilla renderizada desde la app 'ventas'
    html_string = render_to_string('ventas/detalle_orden_render.html', {'orden': orden, 'request': request}) # Ajustado
    try:
         # Opciones para imgkit (asegúrate que wkhtmltoimage esté instalado y en el PATH)
        options = {
            'format': 'jpg',
            'encoding': "UTF-8",
            'quality': '90',
             'width': 302, # Ancho aproximado de 80mm en 96dpi
            'enable-local-file-access': None,
            'quiet': ''
        }
        jpg_data = imgkit.from_string(html_string, False, options=options)
        response = HttpResponse(jpg_data, content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="orden_{orden.numero_venta or orden.id}.jpg"'
        return response
    except Exception as e:
        print(f"Error al generar JPG: {e}")
        messages.error(request, f"Error al generar JPG: {e}. Asegúrate que wkhtmltoimage esté instalado.")
        return redirect('ventas:detalle_orden', orden_id=orden.pk) # Ajustado


@login_required
def descargar_orden_docx(request, orden_id):
    orden = get_object_or_404(OrdenCompra.objects.prefetch_related('detalles__producto'), pk=orden_id)
    try:
        document = Document()
        # Ajustar márgenes (ejemplo)
        sections = document.sections
        for section in sections:
            section.top_margin = Inches(0.4)
            section.bottom_margin = Inches(0.4)
            section.left_margin = Inches(0.5)
            section.right_margin = Inches(0.5)

        # Encabezado Empresa (Alineado a la derecha)
        p_empresa = document.add_paragraph()
        p_empresa.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        runner = p_empresa.add_run(
            "CONSTRUCCIONES V & G LIZ CASTILLO GARCIA SPA\n"
            "RUT: 77.858.577-4\n"
            "Dirección: Vilaco 301, Toconao\n"
            "Teléfono: +56 9 52341652"
        )
        runner.font.size = Pt(8)
        runner.bold = True
        p_empresa.paragraph_format.space_after = Pt(0)

        document.add_paragraph("---" * 12).alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Info Orden
        p_orden_info = document.add_paragraph()
        p_orden_info.add_run(f"Orden de Compra #{orden.numero_venta or orden.id}\n").bold = True
        p_orden_info.add_run(f"Cliente: {orden.cliente}\n")
        p_orden_info.add_run(f"Rut: {orden.rut or 'N/A'}\n")
        p_orden_info.add_run(f"Fecha: {orden.fecha.strftime('%d-%m-%Y %H:%M')}\n") # Formato fecha
        p_orden_info.add_run(f"Dirección: {orden.direccion or 'N/A'}")
        for run in p_orden_info.runs:
            run.font.size = Pt(9) # Tamaño fuente info
        p_orden_info.paragraph_format.space_after = Pt(6)

        document.add_paragraph("---" * 12).alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Título Detalle
        p_detalle_titulo = document.add_paragraph()
        p_detalle_titulo.add_run("Detalle").bold = True
        p_detalle_titulo.runs[0].font.size = Pt(10)
        p_detalle_titulo.paragraph_format.space_after = Pt(3)

        # Tabla de Productos
        table = document.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        table.autofit = False # Controlar anchos manualmente

        # Encabezados tabla
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Producto'
        hdr_cells[1].text = 'Cant'
        hdr_cells[2].text = 'P. Unit.'
        hdr_cells[3].text = 'Total'
        for cell in hdr_cells:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].runs[0].font.size = Pt(9)
            if cell != hdr_cells[0]: # Centrar excepto producto
                 cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER


        # Filas de detalles
        for detalle in orden.detalles.all():
            row_cells = table.add_row().cells
            # Formatear números
            precio_unit_str = f"${detalle.precio_unitario:,.0f}".replace(",", ".")
            total_linea_str = f"${detalle.total_linea:,.0f}".replace(",", ".")

            row_cells[0].text = detalle.producto.nombre
            row_cells[1].text = str(detalle.cantidad)
            row_cells[2].text = precio_unit_str
            row_cells[3].text = total_linea_str

            for i, cell in enumerate(row_cells):
                cell.paragraphs[0].runs[0].font.size = Pt(9)
                if i > 0: # Centrar cantidad, precios
                    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Ajustar anchos de columna (ejemplo)
        table.columns[0].width = Inches(2.8)
        table.columns[1].width = Inches(0.5)
        table.columns[2].width = Inches(0.9)
        table.columns[3].width = Inches(1.0)

        document.add_paragraph("---" * 12).alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Total
        p_total = document.add_paragraph()
        p_total.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        total_str = f"${orden.total:,.0f}".replace(",", ".")
        runner_total = p_total.add_run(f"Total a Pagar: {total_str}")
        runner_total.bold = True
        runner_total.font.size = Pt(11)
        p_total.paragraph_format.space_after = Pt(0)

        document.add_paragraph("---" * 12).alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Mensaje final
        p_gracias = document.add_paragraph(
            "¡Gracias por su compra!\nEsperamos atenderle pronto."
        )
        p_gracias.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_gracias.runs[0].font.size = Pt(8)

        # Guardar en memoria
        f = BytesIO()
        document.save(f)
        f.seek(0)

        # Crear respuesta HTTP
        response = HttpResponse(
            f.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = f'attachment; filename="orden_{orden.numero_venta or orden.id}.docx"'
        f.close()
        return response

    except Exception as e:
        print(f"Error al generar DOCX: {e}")
        messages.error(request, f"Error al generar DOCX: {e}.")
        return redirect('ventas:detalle_orden', orden_id=orden.pk) # Ajustado