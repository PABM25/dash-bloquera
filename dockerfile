# Usa una imagen oficial de Python como base
FROM python:3.11-slim

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crea y define el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema (para Pillow y psycopg2)
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev libjpeg-dev zlib1g-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instala Gunicorn (servidor WSGI) y psycopg2-binary (driver de Postgres)
# Estos no estaban en tu requirements.txt pero son necesarios para producción
RUN pip install gunicorn psycopg2-binary

# Copia tu archivo de requerimientos e instálalos
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia todo el código de tu proyecto al contenedor
COPY . .

# Ejecuta collectstatic para agrupar todos los archivos estáticos
# Esto usará la variable STATIC_ROOT ('staticfiles_collected') de tu settings.py
RUN python manage.py collectstatic --noinput

# Expone el puerto 8000 (donde Gunicorn se ejecutará)
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["gunicorn", "bloquera.wsgi:application", "--bind", "0.0.0.0:8000"]