# Bloquera

Este proyecto es una aplicación web desarrollada con Django para la gestión de una bloquera. Permite administrar trabajadores, asistencias, gastos, inventario y órdenes de compra.

## Características principales
- Registro y gestión de trabajadores
- Control de asistencias manuales y confirmación
- Administración de gastos
- Inventario de productos
- Creación y seguimiento de órdenes de compra
- Panel de administración de Django

## Estructura del proyecto
- `app/`: Lógica principal de la aplicación (modelos, vistas, formularios, urls)
- `bloquera/`: Configuración principal de Django (settings, urls, wsgi, asgi)
- `templates/app/`: Plantillas HTML para la interfaz de usuario
- `static/app/`: Archivos estáticos (CSS, JS, imágenes)
- `db.sqlite3`: Base de datos SQLite
- `manage.py`: Script de gestión de Django

## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/bloquera.git
   cd bloquera
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Realiza las migraciones:
   ```bash
   python manage.py migrate
   ```
4. Ejecuta el servidor:
   ```bash
   python manage.py runserver
   ```

## Uso
Accede a la aplicación en `http://localhost:8000/` y utiliza las diferentes funcionalidades desde la interfaz web.

## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

## Licencia
Este proyecto está bajo la licencia MIT.
