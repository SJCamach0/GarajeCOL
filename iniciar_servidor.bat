@echo off
REM Inicia el servidor de GarajeCOL abriendo la pagina web en el navegador.
echo Iniciando servidor en http://127.0.0.1:5000
py app.py || python app.py
pause
