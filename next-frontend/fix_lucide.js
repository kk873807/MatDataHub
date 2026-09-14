const fs = require('fs');
const file = 'src/components/demos/SimulatedWorkspaceDemo.tsx';
let content = fs.readFileSync(file, 'utf8');
content = content.replace(/Component, /g, 'Box, ');
content = content.replace(/<Component className/g, '<Box className');
fs.writeFileSync(file, content);
console.log('Fixed Lucide Component import');
