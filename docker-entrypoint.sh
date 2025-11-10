#!/bin/bash
# docker-entrypoint.sh

DB_HOST="db" 
DB_PORT="5432" 

echo "Esperando que la base de datos esté lista en $DB_HOST:$DB_PORT..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.5 
done

echo "¡Base de datos lista! Aplicando migraciones y recolectando estáticos."

# 1. Aplicar Migraciones
python manage.py migrate --noinput

# 2. Recolectar Estáticos
# Ahora usando la ruta consistente /app/static
python manage.py collectstatic --noinput --settings=bloquera.settings

echo "¡Base de datos configurada! Iniciando servidor Gunicorn."

# 3. Iniciar Gunicorn (el comando final)
exec gunicorn bloquera.wsgi:application --bind 0.0.0.0:8000