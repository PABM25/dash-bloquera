#!/usr/bin/env python
"""
Utilidad de línea de comandos de Django para tareas administrativas.
"""
import os
import sys

def main():
    """Ejecuta tareas administrativas."""
    # Establece la variable de entorno para apuntar al archivo settings.py
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloquera.settings')
    try:
        # Intenta importar el ejecutor de comandos
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Lanza un error claro si Django no está instalado o el PYTHONPATH es incorrecto
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Pasa los argumentos de la línea de comandos (ej. 'runserver') a Django
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()