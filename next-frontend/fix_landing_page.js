const fs = require('fs');

let content = fs.readFileSync('src/app/page.tsx', 'utf8');

// Add import
content = content.replace(
  'import { API } from "@/lib/api";',
  'import { API } from "@/lib/api";\nimport { InteractiveFeatures } from "@/components/InteractiveFeatures";'
);

// Replace section
const oldSectionRegex = /<section id="solution"[\s\S]*?<\/section>/;
content = content.replace(oldSectionRegex, '<InteractiveFeatures />');

fs.writeFileSync('src/app/page.tsx', content);
console.log('Fixed page.tsx');
