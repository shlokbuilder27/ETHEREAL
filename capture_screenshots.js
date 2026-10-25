const { app, BrowserWindow } = require('electron');
const path = require('path');
const fs = require('fs');

const outputDir = path.join(__dirname, 'assets', 'screenshots');
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

const tabsToCapture = [
  { tab: 'tracker', name: '01_hero_dashboard.png' },
  { tab: 'radar', name: '02_radar_biometrics.png' },
  { tab: 'focus', name: '03_focus_protocol.png' },
  { tab: 'calendar', name: '04_calendar_schedule.png' },
  { tab: 'nutrition', name: '05_nutrition_matrix.png' },
  { tab: 'ai', name: '06_ai_coach.png' },
  { tab: 'profile', name: '07_profile_biometrics.png' }
];

app.whenReady().then(async () => {
  const win = new BrowserWindow({
    width: 1920,
    height: 1080,
    show: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: false
    }
  });

  await win.loadFile(path.join(__dirname, 'index.html'));

  // Wait for initial Tailwind & font load
  await new Promise(r => setTimeout(r, 2500));

  // Dismiss splash screen if visible
  await win.webContents.executeJavaScript(`
    if (typeof dismissSplash === 'function') dismissSplash();
    const splash = document.getElementById('landing-splash-overlay');
    if (splash) splash.style.display = 'none';
  `);

  await new Promise(r => setTimeout(r, 1000));

  for (const item of tabsToCapture) {
    console.log(`Capturing ${item.tab} -> ${item.name}...`);
    await win.webContents.executeJavaScript(`
      if (typeof switchTab === 'function') {
        switchTab('${item.tab}');
      }
    `);
    // Allow backdrop crossfade & chart transitions to render
    await new Promise(r => setTimeout(r, 1800));

    const image = await win.webContents.capturePage();
    const filePath = path.join(outputDir, item.name);
    fs.writeFileSync(filePath, image.toPNG());
    console.log(`Saved ${filePath} (${image.getSize().width}x${image.getSize().height})`);
  }

  console.log('All screenshots captured successfully!');
  app.quit();
});
