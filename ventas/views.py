# ventas/views.py
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import OrdenCompra, DetalleOrden
from inventario.models import Producto
from .forms import OrdenCompraForm, DetalleOrdenFormSet
from io import BytesIO
from django.template.loader import render_to_string
from django.contrib.humanize.templatetags.humanize import intcomma
import os
from django.contrib.staticfiles import finders


# --- IMPORTACIONES PARA PDF (ReportLab) ---
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter # O un tamaño personalizado
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image, Frame, BaseDocTemplate, PageTemplate
from reportlab.platypus.flowables import HRFlowable # Importar HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


# --- IMPORTACIONES PARA DOCX (Sin cambios) ---
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# --- VISTAS EXISTENTES (sin cambios en lógica principal) ---
@login_required
def lista_ordenes(request):
    ordenes = OrdenCompra.objects.prefetch_related('detalles__producto').all().order_by('-fecha')
    return render(request, 'ventas/lista_ordenes.html', {'ordenes': ordenes})

@login_required
@transaction.atomic
def crear_orden(request):
    if request.method == 'POST':
        orden_form = OrdenCompraForm(request.POST)
        detalle_formset = DetalleOrdenFormSet(request.POST, prefix='detalles')

        if orden_form.is_valid() and detalle_formset.is_valid():
            try:
                orden = orden_form.save(commit=False)
                detalles_instancias = detalle_formset.save(commit=False)
                total_orden = 0
                productos_a_actualizar = []
                detalles_a_guardar = []
                valid_details_count = 0

                for form in detalle_formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        producto = form.cleaned_data.get('producto')
                        cantidad = form.cleaned_data.get('cantidad')
                        precio = form.cleaned_data.get('precio_unitario')

                        if producto and cantidad and cantidad > 0 and precio is not None:
                            valid_details_count += 1
                            detalle = form.instance
                            producto_db = Producto.objects.select_for_update().get(pk=producto.pk) # Bloquear producto
                            if producto_db.stock < cantidad:
                                raise Exception(f"No hay suficiente stock para: {producto.nombre} (disponible: {producto_db.stock})")

                            total_linea = cantidad * precio
                            total_orden += total_linea
                            detalles_a_guardar.append(detalle)
                            productos_a_actualizar.append({'producto': producto_db, 'cantidad': cantidad})

                if valid_details_count == 0:
                    raise Exception("Debes añadir al menos un producto válido a la orden.")

                orden.total = total_orden
                orden.save() # Guardar orden principal

                for detalle in detalles_a_guardar:
                    detalle.orden = orden # Asignar la orden guardada
                    detalle.save()

                for item in productos_a_actualizar:
                    item['producto'].disminuir_stock(item['cantidad'])

                detalle_formset.save_m2m()

                messages.success(request, f"Orden {orden.numero_venta} creada exitosamente.")
                return redirect('ventas:detalle_orden', orden_id=orden.pk)

            except Exception as e:
                messages.error(request, f"Error al crear la orden: {e}")

    else: # GET
        orden_form = OrdenCompraForm()
        detalle_formset = DetalleOrdenFormSet(prefix='detalles')

    context = {
        'orden_form': orden_form,
        'detalle_formset': detalle_formset
    }
    return render(request, 'ventas/crear_orden.html', context)


@login_required
def detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenCompra.objects.prefetch_related('detalles__producto'), pk=orden_id)
    return render(request, 'ventas/detalle_orden.html', {'orden': orden})

# --- VISTA DE DESCARGA PDF CON REPORTLAB (MEJORADA) ---
@login_required
def descargar_orden_pdf(request, orden_id):
    orden = get_object_or_404(OrdenCompra.objects.prefetch_related('detalles__producto'), pk=orden_id)

    buffer = BytesIO()

    # --- Configuración del Documento ---
    ticket_width = 80 * mm
    # Incrementamos la altura estimada para dar más espacio
    ticket_height = 200 * mm # Ajusta esta altura si es necesario
    pagesize = (ticket_width, ticket_height)
    margin = 5 * mm
    effective_width = ticket_width - 2 * margin

    doc = BaseDocTemplate(buffer, pagesize=pagesize,
                          leftMargin=margin, rightMargin=margin,
                          topMargin=margin, bottomMargin=margin)

    # --- Estilos ---
    styles = getSampleStyleSheet()
    # Estilo base más pequeño
    style_base = ParagraphStyle(name='Base', parent=styles['Normal'], fontSize=8, leading=10)
    # Estilos derivados
    style_normal = ParagraphStyle(name='Normal', parent=style_base, alignment=TA_LEFT)
    style_bold = ParagraphStyle(name='Bold', parent=style_base, fontName='Helvetica-Bold')
    style_header_info = ParagraphStyle(name='HeaderInfo', parent=style_base, fontSize=7, leading=8.5, alignment=TA_LEFT) # Más pequeño para info empresa
    style_header_name = ParagraphStyle(name='HeaderName', parent=style_header_info, fontName='Helvetica-Bold')
    style_order_title = ParagraphStyle(name='OrderTitle', parent=style_bold, fontSize=9, leading=11, alignment=TA_LEFT)
    style_center = ParagraphStyle(name='Center', parent=style_base, alignment=TA_CENTER)
    style_center_bold = ParagraphStyle(name='CenterBold', parent=style_bold, alignment=TA_CENTER)
    style_right = ParagraphStyle(name='Right', parent=style_base, alignment=TA_RIGHT)
    style_right_bold = ParagraphStyle(name='RightBold', parent=style_bold, alignment=TA_RIGHT)
    style_total_label = ParagraphStyle(name='TotalLabel', parent=style_right_bold, fontSize=10, leading = 12)
    style_total_value = ParagraphStyle(name='TotalValue', parent=style_total_label) # Mismo estilo para el valor
    style_gracias = ParagraphStyle(name='Gracias', parent=style_center, fontSize=8, leading=10)
    style_table_header = ParagraphStyle(name='TableHeader', parent=style_bold, fontSize=7, alignment=TA_CENTER)
    style_table_cell = ParagraphStyle(name='TableCell', parent=style_base, fontSize=7)
    style_table_cell_right = ParagraphStyle(name='TableCellRight', parent=style_table_cell, alignment=TA_RIGHT)
    style_table_product = ParagraphStyle(name='TableProduct', parent=style_table_cell, alignment=TA_LEFT)


    # --- Contenido (Story) ---
    story = []

    # --- Encabezado con Logo ---
    logo_path_relative = 'app/img/logo.png' # Ruta relativa dentro de static
    # Encontrar la ruta absoluta del archivo estático
    logo_path_absolute = finders.find(logo_path_relative)

    if logo_path_absolute and os.path.exists(logo_path_absolute):
        # Redimensionar imagen si es necesario (ej: a 20mm de alto, manteniendo proporción)
        img = Image(logo_path_absolute, height=15*mm, width=15*mm) # Ajusta tamaño según tu logo
        img.hAlign = 'LEFT' # Alinear imagen dentro de su celda (si es necesario)

        header_data = [
            [img, Paragraph("<b>CONSTRUCCIONES V & G<br/>LIZ CASTILLO GARCIA SPA</b><br/>"
                           "RUT: 77.858.577-4<br/>"
                           "Dirección: Vilaco 301, Toconao<br/>"
                           "Teléfono: +56 9 52341652", style_header_info)]
        ]
        header_table = Table(header_data, colWidths=[20*mm, effective_width - 20*mm]) # Anchos de columna
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0), # Sin padding extra
            ('BOTTOMPADDING', (0,0), (-1,-1), 1*mm),
        ]))
        story.append(header_table)
    else:
        # Fallback si no se encuentra el logo
        story.append(Paragraph("CONSTRUCCIONES V & G LIZ CASTILLO GARCIA SPA", style_center_bold))
        # ... (añadir resto de info como párrafos separados) ...
        messages.warning(request, f"No se encontró el archivo del logo en: {logo_path_relative}")

    story.append(Spacer(1, 1 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.black, spaceBefore=1*mm, spaceAfter=1*mm))

    # --- Info Orden ---
    story.append(Paragraph(f"Orden de Compra #{orden.numero_venta or orden.id}", style_order_title))
    story.append(Paragraph(f"Cliente: {orden.cliente}", style_normal))
    if orden.rut:
        story.append(Paragraph(f"RUT: {orden.rut}", style_normal))
    story.append(Paragraph(f"Fecha: {orden.fecha.strftime('%d-%m-%Y %H:%M')}", style_normal))
    if orden.direccion:
        story.append(Paragraph(f"Dirección: {orden.direccion}", style_normal))
    story.append(Spacer(1, 3 * mm))

    # --- Detalle Título ---
    story.append(Paragraph("Detalle", style_bold)) # Podría ser centrado si prefieres
    story.append(Spacer(1, 1 * mm))

    # --- Tabla de Productos ---
    # Encabezados como Paragraphs para usar estilos
    headers = [
        Paragraph('Producto', style_table_header),
        Paragraph('Cant', style_table_header),
        Paragraph('P. Unitario', style_table_header),
        Paragraph('Total', style_table_header)
    ]
    data = [headers]
    detalles = orden.detalles.all()

    table_style_commands = [
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        # ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey), # Quitar fondo gris si no lo quieres
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # Alineaciones específicas por columna (0-indexado)
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),    # Columna Producto (0) a la izquierda
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),  # Columna Cant (1) al centro
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),  # Columnas P.Unit (2) y Total (3) a la derecha
        ('LEFTPADDING', (0, 0), (-1, -1), 1.5*mm), # Añadir un poco de padding
        ('RIGHTPADDING', (0, 0), (-1, -1), 1.5*mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1*mm),
        ('TOPPADDING', (0, 0), (-1, -1), 1*mm),
    ]

    if detalles:
        for detalle in detalles:
            # Usar estilos de celda definidos
            data.append([
                Paragraph(detalle.producto.nombre, style_table_product),
                Paragraph(str(detalle.cantidad), style_table_cell), # Cantidad centrada por estilo de tabla
                Paragraph(f"${intcomma(int(detalle.precio_unitario))}", style_table_cell_right),
                Paragraph(f"${intcomma(int(detalle.total_linea))}", style_table_cell_right)
            ])
    else:
        # Fila para orden sin productos
        data.append([Paragraph('Sin productos', style_table_cell), '', '', ''])
        # Ajustar GRID si se añade esta fila
        table_style_commands[0] = ('GRID', (0, 0), (-1, -2), 0.5, colors.black)


    col_widths = [effective_width * 0.40, effective_width * 0.15, effective_width * 0.22, effective_width * 0.23] # Ajustar anchos
    tabla = Table(data, colWidths=col_widths)
    tabla.setStyle(TableStyle(table_style_commands))
    story.append(tabla)
    story.append(Spacer(1, 3 * mm))

    # --- Total ---
    # Usamos una tabla pequeña para alinear "Total a Pagar:" y el valor
    total_str = f"${intcomma(int(orden.total))}"
    total_data = [[Paragraph('Total a Pagar:', style_total_label), Paragraph(total_str, style_total_value)]]
    total_table = Table(total_data, colWidths=[effective_width * 0.6, effective_width * 0.4])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(total_table)
    story.append(Spacer(1, 1 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.black, spaceBefore=1*mm, spaceAfter=1*mm))


    # --- Mensaje final ---
    story.append(Paragraph("¡Gracias por su compra!", style_gracias))
    story.append(Paragraph("Esperamos atenderle pronto.", style_gracias))

    # --- Construir el PDF ---
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal',
                  leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0) # Padding del frame a 0
    template = PageTemplate(id='main', frames=[frame])
    doc.addPageTemplates([template])

    try:
        doc.build(story)
    except Exception as e:
        print(f"Error al construir PDF con ReportLab: {e}")
        messages.error(request, f"Error al generar PDF: {e}")
        return redirect('ventas:detalle_orden', orden_id=orden.pk)

    # --- Crear Respuesta ---
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="orden_{orden.numero_venta or orden.id}.pdf"'
    return response

# --- VISTA DE DESCARGA DOCX (Sin cambios relevantes aquí) ---
@login_required
def descargar_orden_docx(request, orden_id):
    orden = get_object_or_404(OrdenCompra.objects.prefetch_related('detalles__producto'), pk=orden_id)
    try:
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
            "Teléfono: +56 9 52341652"
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
            if cell != hdr_cells[0]:
                 cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        for detalle in orden.detalles.all():
            row_cells = table.add_row().cells
            # Formatear números estilo CLP
            precio_unit_str = f"${intcomma(int(detalle.precio_unitario))}" # Usar intcomma
            total_linea_str = f"${intcomma(int(detalle.total_linea))}" # Usar intcomma

            row_cells[0].text = detalle.producto.nombre
            row_cells[1].text = str(detalle.cantidad)
            row_cells[2].text = precio_unit_str
            row_cells[3].text = total_linea_str

            for i, cell in enumerate(row_cells):
                cell.paragraphs[0].runs[0].font.size = Pt(9)
                if i > 0:
                    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        table.columns[0].width = Inches(2.8)
        table.columns[1].width = Inches(0.5)
        table.columns[2].width = Inches(0.9)
        table.columns[3].width = Inches(1.0)

        document.add_paragraph("---" * 12).alignment = WD_ALIGN_PARAGRAPH.CENTER

        p_total = document.add_paragraph()
        p_total.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        total_str = f"${intcomma(int(orden.total))}" # Usar intcomma
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

    except Exception as e:
        print(f"Error al generar DOCX: {e}")
        messages.error(request, f"Error al generar DOCX: {e}.")
        return redirect('ventas:detalle_orden', orden_id=orden.pk)