const fs = require('fs');
let nav = fs.readFileSync('src/components/TopNav.tsx', 'utf-8');
nav = nav.replace(/{\s*name:\s*["']AI Adviser["'],\s*href:\s*["']\/ai["'],\s*icon:\s*Bot\s*},?\s*/g, '');
fs.writeFileSync('src/components/TopNav.tsx', nav);
console.log('Fixed TopNav');
