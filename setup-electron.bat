@echo off
echo ========================================
echo    Excel Adjuster - Setup Electron
echo ========================================
echo.

echo [1/4] Verifico Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js non trovato!
    echo    Installa Node.js da: https://nodejs.org
    pause
    exit /b 1
)
echo ✅ Node.js trovato

echo.
echo [2/4] Verifico Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python non trovato!
    echo    Installa Python da: https://python.org
    pause
    exit /b 1
)
echo ✅ Python trovato

echo.
echo [3/4] Installo dipendenze Node.js...
npm install
if %errorlevel% neq 0 (
    echo ❌ Errore installazione dipendenze
    pause
    exit /b 1
)
echo ✅ Dipendenze installate

echo.
echo [4/4] Installo dipendenze Python...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Errore installazione dipendenze Python
    pause
    exit /b 1
)
echo ✅ Dipendenze Python installate

echo.
echo ========================================
echo    Setup completato con successo!
echo ========================================
echo.
echo Comandi disponibili:
echo   npm run electron-dev    - Testa l'app
echo   npm run build:win       - Crea installer Windows
echo   npm run build           - Crea app per tutte le piattaforme
echo.
pause
