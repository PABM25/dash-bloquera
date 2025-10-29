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
    * ... (etc.)
* **Autenticación y Usuarios:**
    * Registro de nuevos usuarios.
    * Inicio y cierre de sesión.
    * Configuración de cuenta de usuario (editar perfil, cambiar contraseña).

## Estructura del Proyecto 🏗️

El proyecto está organizado en las siguientes aplicaciones Django:

* `bloquera/`: Configuración principal del proyecto Django (settings, urls globales, wsgi, asgi).
* `core/`: App principal que maneja la autenticación, vistas generales (home/dashboard), plantillas base, etc.
* `inventario/`: Gestiona los productos y el stock.
* `ventas/`: Gestiona las órdenes de compra y la generación de documentos.
* `recursos_humanos/`: Administra trabajadores, asistencia y salarios.
* `finanzas/`: Se encarga del registro de gastos.
* `manage.py`: Script de utilidad de Django.
* `requirements.txt`: Lista de dependencias Python.
* `dockerfile` / `docker-compose.yml`: (Deberían añadirse aquí) Archivos para despliegue con Docker.

## Instalación ⚙️

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd dash-bloquera
    ```
2.  **Crear y activar un entorno virtual** (recomendado):
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
3.  **Instalar dependencias Python:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Realizar las migraciones:**
    ```bash
    python manage.py migrate
    ```
5.  **Crear un superusuario** (para acceder a /admin/):
    ```bash
    python manage.py createsuperuser
    ```
6.  **Ejecutar el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```
## Dependencias Clave 📦

* Django >= 4.0
* django-crispy-forms
* crispy-bootstrap5
* reportlab (en lugar de pdfkit/imgkit)
* python-docx