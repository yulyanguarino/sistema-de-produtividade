@echo off
rem Sobe backend (8003) + frontend (5500) e abre o navegador. Duplo clique para usar.
cd /d "%~dp0"
start "Backend 8003" /min cmd /c "backend\run_server.bat"
start "Frontend 5500" /min cmd /c "frontend\run_frontend.bat"
timeout /t 6 /nobreak >nul
start http://localhost:5500
echo Servidores iniciados. Para encerrar, feche as janelas "Backend 8003" e "Frontend 5500".
timeout /t 5 >nul
