@echo off
echo Iniciando la aplicación V&G SPA... Espere un momento...

:: Cambia al directorio donde se encuentra este script
cd /d "%~dp0"

:: Ejecuta docker-compose para iniciar los servicios en segundo plano (-d)
docker-compose up -d

echo.
echo ¡Listo! La aplicación debería estar accesible en http://localhost
echo Puede cerrar esta ventana.

:: Pausa para que el usuario pueda leer el mensaje (opcional)
:: timeout /t 10 /nobreak > nul
pause