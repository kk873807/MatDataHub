const fs = require('fs');
let content = fs.readFileSync('src/components/InteractiveFeatures.tsx', 'utf8');
content = content.replace(/g\/cm./g, 'g/cm3');
fs.writeFileSync('src/components/InteractiveFeatures.tsx', content);
