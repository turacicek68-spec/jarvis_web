@echo off
REM Jarvis Web Sunucusunu Başlat

REM 1. Bu bat dosyasının bulunduğu klasöre git
cd /d "%~dp0"

REM 2. Flask sunucusunu başlat
echo Flask sunucusu başlatılıyor...
start "" cmd /k "python app.py"

REM 3. 2 saniye bekle ve tarayıcıyı aç
timeout /t 2 /nobreak >nul
start "" http://127.0.0.1:5000/

pause
