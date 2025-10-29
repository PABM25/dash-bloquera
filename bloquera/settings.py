# bloquera/settings.py
"""
Archivo de configuración principal del proyecto Django "bloquera".

Define las aplicaciones instaladas, middleware, bases de datos,
configuraciones de internacionalización, archivos estáticos y
otras configuraciones a nivel de proyecto.
"""

import os
from pathlib import Path

# --- Definición de Rutas Base ---
# Construye rutas dentro del proyecto como: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# --- Configuración de Seguridad y Despliegue ---

# ADVERTENCIA DE SEGURIDAD: ¡mantén la clave secreta usada en producción en secreto!
# Se usa os.environ.get para leerla desde variables de entorno, con un valor por defecto
# (inseguro) solo para desarrollo.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-^5o5g+pxuhyryu*fk*sma3s6=28%j3&t^&$l_9jk*%70y$t$ru')

# ADVERTENCIA DE SEGURIDAD: ¡no ejecutes con debug activado en producción!
# Lee la variable de entorno 'DJANGO_DEBUG'. Si no existe, usa 'True' por defecto.
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# Hosts permitidos. Lee desde variables de entorno, separando por comas.
# Es vital para producción.
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')


# --- Definición de Aplicaciones ---
# Aquí se registran todas las apps de Django y de terceros que usa el proyecto.

INSTALLED_APPS = [
    # Mis Apps (usando la configuración explícita de AppConfig)
    'core.apps.CoreConfig', # App principal (dashboard, auth)
    'inventario.apps.InventarioConfig',
    'recursos_humanos.apps.RecursosHumanosConfig',
    'ventas.apps.VentasConfig',
    'finanzas.apps.FinanzasConfig',

    # Apps nativas de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps de Terceros
    'crispy_forms', # Para renderizar formularios con Bootstrap
    'crispy_bootstrap5', # Plantillas de Crispy para Bootstrap 5
    'django.contrib.humanize' # Para formatear números (ej. 1,000,000)
]


# --- Configuración de Middleware ---
# El middleware procesa las peticiones y respuestas globalmente.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Maneja sesiones
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', # Protección CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Asocia usuarios a peticiones
    'django.contrib.messages.middleware.MessageMiddleware', # Maneja mensajes flash
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- Configuración de URLs ---
# Define el archivo de URLs raíz del proyecto.
ROOT_URLCONF = 'bloquera.urls'

# --- Configuración de Plantillas (Templates) ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # DIRS le dice a Django dónde buscar plantillas a nivel de proyecto.
        'DIRS': [BASE_DIR / 'templates'], # Busca en una carpeta 'templates' en la raíz
        # APP_DIRS=True hace que Django busque en carpetas 'templates' dentro de cada app.
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Estos procesadores añaden variables útiles al contexto de todas las plantillas.
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # Añade la variable 'request'
                'django.contrib.auth.context_processors.auth', # Añade 'user' y 'perms'
                'django.contrib.messages.context_processors.messages', # Añade 'messages'
            ],
        },
    },
]

# --- Configuración de WSGI ---
# Define la aplicación WSGI para servidores web.
WSGI_APPLICATION = 'bloquera.wsgi.application'


# --- Configuración de Base de Datos ---
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# Configurado para leer desde variables de entorno para producción (Docker).
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'constructora'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASS', 'Pabm261996!*'),
        'HOST': os.environ.get('DB_HOST', 'localhost'), # Docker Compose cambiará esto a 'db'
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
# NOTA: En desarrollo, si no usas Docker, puedes cambiar 'HOST' a 'localhost'
# o usar el 'db.sqlite3' original:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# --- Validación de Contraseñas ---
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# --- Internacionalización (i18n) ---
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es-cl' # Español - Chile
TIME_ZONE = 'America/Santiago' # Zona horaria de Chile
USE_I18N = True # Activar traducción
USE_TZ = True # Activar soporte para zonas horarias


# --- Configuración de Archivos Estáticos (CSS, JS, Imágenes) ---
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# URL pública para los archivos estáticos.
STATIC_URL = '/static/'

# Directorio donde `collectstatic` reunirá todos los archivos estáticos
# para servirlos en producción (ej. Nginx).
STATIC_ROOT = BASE_DIR / 'staticfiles_collected'

# Directorios adicionales donde Django buscará archivos estáticos.
# Aquí se define que busque en la carpeta 'static' de la app 'core'.
STATICFILES_DIRS = [
     BASE_DIR / "core" / "static",
]


# --- Configuración de Clave Primaria por Defecto ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Configuración de Crispy Forms ---
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5" # Usar Bootstrap 5

# --- Configuración de Autenticación ---
# Define las URLs para el flujo de login/logout.
LOGIN_URL = 'core:login' # Nombre de la URL para iniciar sesión
LOGIN_REDIRECT_URL = 'core:home' # A dónde ir después de un login exitoso
LOGOUT_REDIRECT_URL = 'core:login' # A dónde ir después de cerrar sesión