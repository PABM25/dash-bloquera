# bloquera/settings.py (Modificado para no tener secretos por defecto)
"""
Archivo de configuración principal del proyecto Django "bloquera".
"""

import os
from pathlib import Path

# --- Definición de Rutas Base ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Configuración de Seguridad y Despliegue ---

# Lee la clave secreta OBLIGATORIAMENTE desde el entorno.
# Si no está definida, usa una clave "dummy" temporal SOLO para el 'build'.
# La clave real de .env la sobrescribirá en 'run'.
# LÍNEA CORREGIDA:
SECRET_KEY = 'django-insecure-^5o5g+pxuhyryu*fk*sma3s6=28%j3&t^&$l_9jk*%70y$t$ru'
# Lee el modo DEBUG desde el entorno. Si no está, asume 'False' (seguro).
DEBUG = True

# Lee los hosts permitidos desde el entorno. Si no está, usa una lista vacía.
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    # Mis Apps
    'core.apps.CoreConfig',
    'inventario.apps.InventarioConfig',
    'recursos_humanos.apps.RecursosHumanosConfig',
    'ventas.apps.VentasConfig',
    'finanzas.apps.FinanzasConfig',
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third Party Apps
    'crispy_forms',
    'crispy_bootstrap5',
    'django.contrib.humanize'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bloquera.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bloquera.wsgi.application'


# --- Configuración de Base de Datos ---
# Lee OBLIGATORIAMENTE la configuración de la BD desde el entorno.
# Usamos .get() con valores 'dummy' para que el 'collectstatic'
# (que se ejecuta durante el 'build') no falle, ya que necesita
# leer este archivo de settings para funcionar.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'constructora',
        'USER': 'postgres',
        'PASSWORD': 'Pabm261996!*',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
     BASE_DIR / "core" / "static",
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Autenticación
LOGIN_URL = 'core:login'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'core:login'
