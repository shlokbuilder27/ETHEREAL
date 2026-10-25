const { app, BrowserWindow, shell, powerSaveBlocker } = require('electron');
const path = require('path');

// Keep animations, timers, and audio running at full speed in the background
app.commandLine.appendSwitch('disable-background-timer-throttling');
app.commandLine.appendSwitch('disable-renderer-backgrounding');

let mainWindow;
let powerSaveBlockerId = null;

// Prevent display dimming / sleeping and prevent laptop suspension
function enableAlwaysOn() {
  if (powerSaveBlockerId === null || !powerSaveBlocker.isStarted(powerSaveBlockerId)) {
    powerSaveBlockerId = powerSaveBlocker.start('prevent-display-sleep');
    console.log(`[ETHEREAL] PowerSaveBlocker active (ID: ${powerSaveBlockerId}) - Laptop display and system will always stay ON!`);
  }
}

function disableAlwaysOn() {
  if (powerSaveBlockerId !== null && powerSaveBlocker.isStarted(powerSaveBlockerId)) {
    powerSaveBlocker.stop(powerSaveBlockerId);
    console.log(`[ETHEREAL] PowerSaveBlocker stopped (ID: ${powerSaveBlockerId})`);
    powerSaveBlockerId = null;
  }
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1440,
    height: 920,
    minWidth: 1024,
    minHeight: 700,
    title: 'ETHEREAL // Sleeper Build Protocol',
    icon: path.join(__dirname, 'build', 'icon.ico'),
    backgroundColor: '#000000',
    autoHideMenuBar: true,
    show: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: false,
      allowRunningInsecureContent: true,
      backgroundThrottling: false
    }
  });

  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Handle external link clicks
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith('http:') || url.startsWith('https:')) {
      shell.openExternal(url);
      return { action: 'deny' };
    }
    return { action: 'allow' };
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  // Always stay on: laptop display and system will never sleep or turn off while ETHEREAL is running
  enableAlwaysOn();

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  disableAlwaysOn();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('will-quit', () => {
  disableAlwaysOn();
});
