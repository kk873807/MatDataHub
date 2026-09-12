const fs = require('fs');

const files = [
    'src/components/SafetyFactor.tsx',
    'src/components/ThermalExpansion.tsx',
    'src/components/FatigueLife.tsx',
    'src/components/BeamDeflection.tsx',
    'src/components/ThermalShock.tsx'
];

for (const filepath of files) {
    let content = fs.readFileSync(filepath, 'utf8');
    // Replace newline + 'esult' back to 'result'
    content = content.replace(/\{\r?esult/g, '{result');
    fs.writeFileSync(filepath, content);
}
console.log("Fixed carriage returns");
