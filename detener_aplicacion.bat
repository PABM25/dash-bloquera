@echo off
echo Deteniendo la aplicación V&G SPA...

:: Cambia al directorio donde se encuentra este script
cd /d "%~dp0"

:: Ejecuta docker-compose para detener y eliminar los contenedores
docker-compose down

echo.
echo ¡Aplicación detenida! Puede cerrar esta ventana.

:: Pausa para que el usuario pueda leer el mensaje (opcional)
:: timeout /t 5 /nobreak > nul
pause