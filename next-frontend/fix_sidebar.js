const fs = require('fs');
let content = fs.readFileSync('src/app/projects/[id]/page.tsx', 'utf8');

// Fix Cost Optimizer button active text color
content = content.replace(/text-green-400 border/g, 'text-green-700 dark:text-green-400 border');

// Fix hover text color on all sidebar buttons
content = content.replace(/hover:text-white border border-transparent/g, 'hover:text-slate-900 dark:hover:text-white border border-transparent');

fs.writeFileSync('src/app/projects/[id]/page.tsx', content);
console.log('Fixed sidebar buttons');
