# Dash Bloquera - Sistema de Gestión

Este proyecto es una aplicación web desarrollada con **Django** diseñada para la gestión integral de un negocio de bloquera y constructora. Permite administrar inventario, ventas (órdenes de compra), recursos humanos (trabajadores, asistencia, salarios) y finanzas (gastos), centralizando la información en un dashboard interactivo.

## Características Principales ✨

* **Dashboard Principal:**
    * Visualización de KPIs clave: Ingresos totales, gastos totales, asistencias del mes.
    * Gráficos interactivos (torta y área) mostrando resumen financiero y tendencias mensuales (Ingresos vs. Gastos).
* **Gestión de Inventario:**
    * CRUD (Crear, Leer, Actualizar, Eliminar) de productos (materiales).
    * Control de stock.
    * API simple para consultar stock de productos (usado en el formulario de ventas).
* **Gestión de Ventas:**
    * Creación de Órdenes de Compra detalladas (cliente, RUT, dirección, productos, cantidades, precios).
    * Validación de stock disponible al crear la orden.
    * Cálculo automático del total de la orden.
    * Listado histórico de órdenes de compra.
    * Visualización detallada de cada orden en formato de ticket/comprobante.
    * Descarga de órdenes en formatos **PDF**, **JPG** y **DOCX**. 📄🖼️📝
* **Gestión de Recursos Humanos:**
    * CRUD de trabajadores (datos personales, cargo, tipo de proyecto, salario por día).
    * Registro manual de asistencia por trabajador, fecha y tipo de proyecto.
    * Cálculo de salarios basado en días trabajados (asistencias) dentro de un rango de fechas y por tipo de proyecto.
    * Registro automático del pago de salario como un Gasto en el módulo de Finanzas.
* **Gestión de Finanzas:**
    * CRUD de gastos (fecha, categoría, descripción, monto, tipo de proyecto).
    * Listado y filtrado de gastos.
* **Autenticación y Usuarios:**
    * Registro de nuevos usuarios.
    * Inicio y cierre de sesión.
    * Configuración de cuenta de usuario (editar perfil, cambiar contraseña).
* **Interfaz de Usuario:**
    * Diseño responsivo basado en Bootstrap 5.
    * Uso de `django-crispy-forms` y `crispy-bootstrap5` para renderizar formularios.
    * Sidebar de navegación persistente.

## Estructura del Proyecto 🏗️

El proyecto está organizado en las siguientes aplicaciones Django:

* `bloquera/`: Configuración principal del proyecto Django (settings, urls globales, wsgi, asgi).
* `core/`: App principal que maneja la autenticación, vistas generales (home/dashboard), plantillas base, archivos estáticos principales y configuración de usuario.
* `inventario/`: Gestiona los modelos, vistas, formularios y URLs relacionados con los productos y el stock.
* `ventas/`: Gestiona todo lo relacionado con las órdenes de compra, sus detalles y la generación de documentos (PDF, JPG, DOCX).
* `recursos_humanos/`: Administra la información de los trabajadores, registros de asistencia y cálculo de salarios.
* `finanzas/`: Se encarga del registro y listado de los gastos operativos y salariales.
* `manage.py`: Script de utilidad de Django.
* `db.sqlite3`: Base de datos SQLite (para desarrollo).
* `requirements.txt`: Lista de dependencias Python.

## Instalación ⚙️

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd dash-bloquera
    ```
2.  **Crear y activar un entorno virtual** (recomendado):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
3.  **Instalar dependencias Python:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Instalar dependencias externas (wkhtmltopdf/wkhtmltoimage):**
    Para la generación de PDF y JPG, necesitas instalar `wkhtmltopdf` (que usualmente incluye `wkhtmltoimage`). Descárgalo desde [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html) y asegúrate de que los ejecutables estén en el PATH de tu sistema o configura la ruta en `settings.py` si usas `python-pdfkit`/`python-imgkit` con configuración explícita (aunque no parece ser el caso en el código actual).
5.  **Realizar las migraciones:**
    ```bash
    python manage.py migrate
    ```
6.  **(Opcional) Crear un superusuario** para acceder al admin de Django:
    ```bash
    python manage.py createsuperuser
    ```
7.  **Ejecutar el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```

## Uso 🚀

1.  Accede a la aplicación en tu navegador: `http://127.0.0.1:8000/`.
2.  Regístrate o inicia sesión con tus credenciales.
3.  Utiliza el menú lateral (sidebar) para navegar entre las diferentes secciones (Dashboard, Ventas, Inventario, Personal, Finanzas).
4.  El panel de administración de Django está disponible en `http://127.0.0.1:8000/admin/` (requiere credenciales de superusuario).

## Dependencias Clave 📦

* Django >= 4.0
* django-crispy-forms
* crispy-bootstrap5
* pdfkit (requiere wkhtmltopdf)
* imgkit (requiere wkhtmltoimage)
* python-docx (usado implícitamente por `docx`)

*(Otras dependencias menores pueden estar incluidas)*

## Contribuciones y Licencia

Las contribuciones son bienvenidas. Este proyecto está bajo la licencia MIT (si aplica, verifica si tienes un archivo LICENSE). 