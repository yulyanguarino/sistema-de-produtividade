@echo off
cd /d "%~dp0"
echo Abrindo frontend local em http://localhost:5500
echo (o backend precisa estar rodando em http://localhost:8000 - use backend\run_server.bat)
"..\backend\venv\Scripts\python.exe" -m http.server 5500
