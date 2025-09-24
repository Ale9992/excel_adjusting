const fs = require('fs');
const path = require('path');

// Script per creare icone placeholder
// In produzione, sostituisci con icone reali

const createPlaceholderIcon = (size, format) => {
  // Crea un'icona SVG semplice
  const svg = `
<svg width="${size}" height="${size}" xmlns="http://www.w3.org/2000/svg">
  <rect width="${size}" height="${size}" fill="#3B82F6" rx="${size/8}"/>
  <text x="50%" y="50%" text-anchor="middle" dy=".3em" 
        font-family="Arial, sans-serif" font-size="${size/4}" 
        font-weight="bold" fill="white">EA</text>
</svg>`;
  
  return svg;
};

// Crea directory assets se non esiste
const assetsDir = path.join(__dirname, 'assets');
if (!fs.existsSync(assetsDir)) {
  fs.mkdirSync(assetsDir);
}

// Crea icona PNG per Linux
const pngIcon = createPlaceholderIcon(512, 'png');
fs.writeFileSync(path.join(assetsDir, 'icon.png'), pngIcon);

console.log('✅ Icone placeholder create in assets/');
console.log('📝 Sostituisci con icone reali prima del build finale');
console.log('🎨 Formati necessari:');
console.log('   - assets/icon.png (512x512) per Linux');
console.log('   - assets/icon.ico (256x256) per Windows');
console.log('   - assets/icon.icns (512x512) per macOS');
