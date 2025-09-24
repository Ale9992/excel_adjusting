const { app, BrowserWindow, Menu, Tray, nativeImage, shell, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

// Variabili globali
let mainWindow;
let tray;
let pythonProcess;
let isQuitting = false;

// Configurazione
const PYTHON_PORT = 8000;
const APP_NAME = 'Excel Adjuster';

// Funzione per creare la finestra principale
function createWindow() {
  // Crea la finestra del browser
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      webSecurity: true
    },
    icon: getAppIcon(),
    title: APP_NAME,
    show: false, // Non mostrare finché non è pronto
    titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'default'
  });

  // Carica l'app
  mainWindow.loadFile('index.html');

  // Mostra la finestra quando è pronta
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    
    // Avvia il server Python
    startPythonServer();
  });

  // Gestisci la chiusura della finestra
  mainWindow.on('close', (event) => {
    if (!isQuitting) {
      event.preventDefault();
      mainWindow.hide();
      
      // Mostra notifica se è la prima volta
      if (tray) {
        tray.displayBalloon({
          title: APP_NAME,
          content: 'L\'applicazione continua a funzionare in background. Clicca sull\'icona per riaprirla.',
          icon: getAppIcon()
        });
      }
    }
  });

  // Gestisci i link esterni
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });

  // Apri DevTools in modalità sviluppo
  if (process.argv.includes('--dev')) {
    mainWindow.webContents.openDevTools();
  }
}

// Funzione per avviare il server Python
function startPythonServer() {
  const pythonPath = getPythonPath();
  const scriptPath = path.join(__dirname, '..', 'app.py');
  
  console.log('Avvio server Python...');
  console.log('Python path:', pythonPath);
  console.log('Script path:', scriptPath);

  // Verifica che il file Python esista
  if (!fs.existsSync(scriptPath)) {
    dialog.showErrorBox('Errore', 'File app.py non trovato!');
    return;
  }

  // Avvia il processo Python
  pythonProcess = spawn(pythonPath, [scriptPath], {
    cwd: path.join(__dirname, '..'),
    stdio: ['pipe', 'pipe', 'pipe']
  });

  // Gestisci l'output del server
  pythonProcess.stdout.on('data', (data) => {
    console.log('Python stdout:', data.toString());
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error('Python stderr:', data.toString());
  });

  pythonProcess.on('close', (code) => {
    console.log(`Server Python chiuso con codice: ${code}`);
    if (!isQuitting) {
      // Riavvia il server se non stiamo chiudendo l'app
      setTimeout(() => {
        startPythonServer();
      }, 2000);
    }
  });

  pythonProcess.on('error', (error) => {
    console.error('Errore avvio server Python:', error);
    dialog.showErrorBox('Errore Server', `Impossibile avviare il server Python: ${error.message}`);
  });
}

// Funzione per ottenere il percorso di Python
function getPythonPath() {
  if (process.platform === 'win32') {
    return 'python.exe';
  } else if (process.platform === 'darwin') {
    return 'python3';
  } else {
    return 'python3';
  }
}

// Funzione per ottenere l'icona dell'app
function getAppIcon() {
  const iconPath = path.join(__dirname, '..', 'assets', 'icon.png');
  if (fs.existsSync(iconPath)) {
    return nativeImage.createFromPath(iconPath);
  }
  return null;
}

// Funzione per creare il menu
function createMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Nuovo File Excel',
          accelerator: 'CmdOrCtrl+N',
          click: () => {
            mainWindow.webContents.send('new-file');
          }
        },
        { type: 'separator' },
        {
          label: 'Esci',
          accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
          click: () => {
            isQuitting = true;
            app.quit();
          }
        }
      ]
    },
    {
      label: 'Modifica',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' }
      ]
    },
    {
      label: 'Visualizza',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' }
      ]
    },
    {
      label: 'Aiuto',
      submenu: [
        {
          label: 'Informazioni',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'Informazioni',
              message: APP_NAME,
              detail: 'Versione 1.0.0\nCreato da Alessio Baronti\nper Puff Store Pisa\n\nLicenza gratuita'
            });
          }
        }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// Funzione per creare la system tray
function createTray() {
  const icon = getAppIcon();
  if (icon) {
    tray = new Tray(icon);
    
    const contextMenu = Menu.buildFromTemplate([
      {
        label: 'Mostra App',
        click: () => {
          mainWindow.show();
        }
      },
      {
        label: 'Nascondi App',
        click: () => {
          mainWindow.hide();
        }
      },
      { type: 'separator' },
      {
        label: 'Esci',
        click: () => {
          isQuitting = true;
          app.quit();
        }
      }
    ]);

    tray.setToolTip(APP_NAME);
    tray.setContextMenu(contextMenu);
    
    tray.on('click', () => {
      if (mainWindow.isVisible()) {
        mainWindow.hide();
      } else {
        mainWindow.show();
      }
    });
  }
}

// Eventi dell'app
app.whenReady().then(() => {
  createWindow();
  createMenu();
  createTray();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    isQuitting = true;
    app.quit();
  }
});

app.on('before-quit', () => {
  isQuitting = true;
  
  // Termina il processo Python
  if (pythonProcess) {
    pythonProcess.kill();
  }
});

// Gestisci il protocollo personalizzato (opzionale)
app.setAsDefaultProtocolClient('excel-adjuster');

// Prevenire l'avvio di più istanze
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });
}
