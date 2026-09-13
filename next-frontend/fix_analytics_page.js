const fs = require('fs');
let content = fs.readFileSync('src/app/analytics/page.tsx', 'utf8');

// Add import
content = content.replace(
  'import { motion } from "framer-motion";',
  'import { motion } from "framer-motion";\nimport { SimulatedCompareDemo } from "@/components/demos/SimulatedCompareDemo";'
);

// Insert demo before the grid
const gridStart = '<div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">';
content = content.replace(
  gridStart,
  `<div className="mb-12">\n            <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-6 flex items-center gap-2"><Scale className="w-6 h-6 text-indigo-500" /> See it in action</h2>\n            <SimulatedCompareDemo />\n          </div>\n          ` + gridStart
);

fs.writeFileSync('src/app/analytics/page.tsx', content);
console.log('Fixed analytics page');
