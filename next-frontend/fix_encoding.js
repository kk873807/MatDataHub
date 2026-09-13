const fs = require('fs');

let content = fs.readFileSync('src/components/InteractiveFeatures.tsx', 'utf8');

// Replace the corrupted character with a standard HTML entity or just a 3
content = content.replace(/g\/cm./g, 'g/cm³');

fs.writeFileSync('src/components/InteractiveFeatures.tsx', content);
console.log('Fixed encoding bug');
