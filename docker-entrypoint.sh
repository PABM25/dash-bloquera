#!/bin/bash
# docker-entrypoint.sh

# Nombre del host de la base de datos (definido en docker-compose.yml)
DB_HOST="db" 
# Puerto de la base de datos
DB_PORT="5432" 

echo "Esperando que la base de datos esté lista en $DB_HOST:$DB_PORT..."

# Bucle que espera a que netcat (nc) pueda conectarse al host y puerto
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.5 
done

echo "¡Base de datos lista! Ejecutando el comando de inicio de la aplicación."

# Ejecutar el comando original de Gunicorn
exec gunicorn bloquera.wsgi:application --bind 0.0.0.0:8000