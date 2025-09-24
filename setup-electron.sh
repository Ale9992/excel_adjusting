#!/bin/bash

echo "========================================"
echo "    Excel Adjuster - Setup Electron"
echo "========================================"
echo

echo "[1/4] Verifico Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js non trovato!"
    echo "   Installa Node.js da: https://nodejs.org"
    exit 1
fi
echo "✅ Node.js trovato"

echo
echo "[2/4] Verifico Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non trovato!"
    echo "   Installa Python3: sudo apt install python3"
    exit 1
fi
echo "✅ Python3 trovato"

echo
echo "[3/4] Installo dipendenze Node.js..."
npm install
if [ $? -ne 0 ]; then
    echo "❌ Errore installazione dipendenze"
    exit 1
fi
echo "✅ Dipendenze installate"

echo
echo "[4/4] Installo dipendenze Python..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Errore installazione dipendenze Python"
    exit 1
fi
echo "✅ Dipendenze Python installate"

echo
echo "========================================"
echo "    Setup completato con successo!"
echo "========================================"
echo
echo "Comandi disponibili:"
echo "  npm run electron-dev    - Testa l'app"
echo "  npm run build:win       - Crea installer Windows"
echo "  npm run build:mac       - Crea installer macOS"
echo "  npm run build:linux     - Crea installer Linux"
echo "  npm run build           - Crea app per tutte le piattaforme"
echo
