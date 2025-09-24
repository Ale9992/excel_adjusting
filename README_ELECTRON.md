# Excel Adjuster - App Desktop con Electron

Questa guida ti spiega come creare un'app desktop installabile per Windows, macOS e Linux usando Electron.

## 🚀 **Caratteristiche dell'App Desktop**

- ✅ **Cross-platform**: Windows, macOS, Linux
- ✅ **Installabile**: File .exe, .dmg, .deb
- ✅ **System Tray**: Funziona in background
- ✅ **Auto-avvio**: Server Python integrato
- ✅ **Interfaccia nativa**: Menu e scorciatoie
- ✅ **Portable**: Versione senza installazione

## 📋 **Prerequisiti**

### **1. Node.js**
Installa Node.js (versione 18 o superiore):
- **Windows**: [nodejs.org](https://nodejs.org)
- **macOS**: `brew install node`
- **Linux**: `sudo apt install nodejs npm`

### **2. Python**
Assicurati che Python sia installato e accessibile:
- **Windows**: Python 3.11+ nel PATH
- **macOS**: `python3` disponibile
- **Linux**: `python3` disponibile

## 🛠️ **Installazione e Setup**

### **1. Installa le dipendenze**
```bash
npm install
```

### **2. Testa l'app in modalità sviluppo**
```bash
npm run electron-dev
```

### **3. Crea l'app per la distribuzione**
```bash
# Per Windows
npm run build:win

# Per macOS
npm run build:mac

# Per Linux
npm run build:linux

# Per tutte le piattaforme
npm run build
```

## 📁 **Struttura del Progetto**

```
excel-adjuster/
├── electron/
│   ├── main.js          # Processo principale Electron
│   └── preload.js       # Script di preload sicuro
├── assets/
│   ├── icon.ico         # Icona Windows
│   ├── icon.icns        # Icona macOS
│   └── icon.png         # Icona Linux
├── dist/                # File compilati
├── index.html           # Frontend HTML
├── app.js               # Frontend JavaScript
├── app.py               # Backend Python
├── solver_semplice.py   # Algoritmo
├── package.json         # Configurazione Node.js
└── electron-builder.json # Configurazione build
```

## 🎯 **Funzionalità dell'App**

### **Interfaccia Desktop**
- **Finestra principale**: Interfaccia web integrata
- **Menu nativo**: File, Modifica, Visualizza, Aiuto
- **Scorciatoie**: Ctrl+N (nuovo file), Ctrl+Q (esci)
- **System Tray**: Icona nella barra delle applicazioni

### **Gestione Server**
- **Auto-avvio**: Server Python si avvia automaticamente
- **Background**: Continua a funzionare anche se chiusa
- **Riavvio automatico**: Se il server si blocca
- **Gestione errori**: Notifiche per problemi

### **Distribuzione**
- **Windows**: Installer NSIS + versione portable
- **macOS**: File .dmg con drag & drop
- **Linux**: AppImage + pacchetto .deb

## 🔧 **Configurazione Avanzata**

### **Personalizzare l'Icona**
1. Crea le icone in formato:
   - **Windows**: `assets/icon.ico` (256x256)
   - **macOS**: `assets/icon.icns` (512x512)
   - **Linux**: `assets/icon.png` (512x512)

2. Aggiorna `electron-builder.json` se necessario

### **Modificare il Comportamento**
Edita `electron/main.js` per:
- Cambiare dimensioni finestra
- Modificare menu
- Aggiungere funzionalità
- Personalizzare system tray

### **Configurare il Build**
Modifica `electron-builder.json` per:
- Cambiare nome app
- Modificare installer
- Aggiungere certificati
- Personalizzare distribuzione

## 📦 **Distribuzione**

### **File Generati**
Dopo il build, troverai in `dist/`:

**Windows:**
- `Excel Adjuster-1.0.0-x64.exe` (installer)
- `Excel Adjuster-1.0.0-x64-portable.exe` (portable)

**macOS:**
- `Excel Adjuster-1.0.0-x64.dmg` (installer)
- `Excel Adjuster-1.0.0-arm64.dmg` (Apple Silicon)

**Linux:**
- `Excel Adjuster-1.0.0-x64.AppImage` (portable)
- `Excel Adjuster-1.0.0-x64.deb` (installer)

### **Test dell'App**
1. **Installa** l'app su una macchina pulita
2. **Verifica** che si avvii correttamente
3. **Testa** tutte le funzionalità
4. **Controlla** che il server Python funzioni

## 🐛 **Troubleshooting**

### **App non si avvia**
- Verifica che Python sia installato
- Controlla i log in DevTools (F12)
- Assicurati che `app.py` sia presente

### **Server Python non funziona**
- Verifica il percorso di Python
- Controlla le dipendenze in `requirements.txt`
- Testa manualmente: `python app.py`

### **Build fallisce**
- Verifica Node.js e npm
- Controlla `package.json`
- Assicurati che tutti i file siano presenti

### **Icone non appaiono**
- Verifica formato e dimensioni
- Controlla percorsi in `electron-builder.json`
- Usa tool online per convertire formati

## 🚀 **Deploy e Distribuzione**

### **Distribuzione Manuale**
1. Crea i file con `npm run build`
2. Carica su Google Drive/Dropbox
3. Condividi i link di download

### **Distribuzione Automatica**
Configura GitHub Actions per:
- Build automatico su push
- Upload su GitHub Releases
- Notifiche automatiche

### **Store Distribution**
- **Microsoft Store**: Windows Package Manager
- **Mac App Store**: Richiede certificati Apple
- **Snap Store**: Per distribuzione Linux

## 📝 **Note di Sviluppo**

### **Sicurezza**
- `contextIsolation: true`
- `nodeIntegration: false`
- Script di preload sicuro

### **Performance**
- Lazy loading delle risorse
- Gestione memoria ottimizzata
- Chiusura pulita dei processi

### **Compatibilità**
- Windows 10+
- macOS 10.14+
- Linux (Ubuntu 18.04+)

---

**Congratulazioni!** Hai creato un'app desktop professionale per Excel Adjuster! 🎉

L'app è ora pronta per essere distribuita e installata su qualsiasi computer Windows, macOS o Linux.
