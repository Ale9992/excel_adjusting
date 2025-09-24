const { contextBridge, ipcRenderer } = require('electron');

// Espone API sicure al renderer
contextBridge.exposeInMainWorld('electronAPI', {
  // Funzioni per comunicare con il main process
  onNewFile: (callback) => {
    ipcRenderer.on('new-file', callback);
  },
  
  // Funzioni per il sistema
  platform: process.platform,
  
  // Funzioni per le notifiche
  showNotification: (title, body) => {
    ipcRenderer.invoke('show-notification', { title, body });
  }
});
