# Usa una imagen oficial de Python ligera como base
FROM python:3.11-slim

# Establece variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE 1 # No crear archivos .pyc
ENV PYTHONUNBUFFERED 1      # Enviar logs directo a la consola (vital para Docker)

# Crea y define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema operativo (para Postgres, Pillow y netcat)
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev libjpeg-dev zlib1g-dev netcat-openbsd \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instala Gunicorn (servidor WSGI) y psycopg2 (driver de Postgres)
# Estos son necesarios para producción, incluso si no están en requirements.txt
RUN pip install gunicorn psycopg2-binary

# Copia solo el archivo de requerimientos primero
COPY requirements.txt .
# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Copiar el script de entrada y darle permisos
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Copia TODO el código del proyecto al directorio /app
COPY . .

# Ejecuta 'collectstatic' de Django
RUN python manage.py collectstatic --noinput

# Expone el puerto 8000 (donde Gunicorn se ejecutará DENTRO del contenedor)
EXPOSE 8000

# Cambiar el CMD para usar el script
CMD ["docker-entrypoint.sh"]