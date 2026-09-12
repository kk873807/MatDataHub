const fs = require('fs');
const path = require('path');

const dir = 'src/components';
const files = ['SafetyFactor.tsx', 'ThermalExpansion.tsx', 'FatigueLife.tsx', 'BeamDeflection.tsx', 'CostOptimizer.tsx', 'ThermalShock.tsx'];

files.forEach(file => {
  const filePath = path.join(dir, file);
  if (!fs.existsSync(filePath)) return;
  
  let content = fs.readFileSync(filePath, 'utf8');
  
  // Fix text-slate-200 to text-slate-700 dark:text-slate-200
  content = content.replace(/className="([^"]*)text-slate-200([^"]*)"/g, 'className="$1text-slate-700 dark:text-slate-200$2"');
  
  // Fix FatigueLife specific colors
  if (file === 'FatigueLife.tsx') {
    content = content.replace(/bg-cyan-900\/20/g, 'bg-cyan-100 dark:bg-cyan-900/20');
    content = content.replace(/border-cyan-900\/50/g, 'border-cyan-200 dark:border-cyan-900/50');
    content = content.replace(/text-cyan-400/g, 'text-cyan-700 dark:text-cyan-400');
    content = content.replace(/text-cyan-300/g, 'text-cyan-600 dark:text-cyan-300');
  }
  
  fs.writeFileSync(filePath, content);
});

console.log('Fixed styles.');
