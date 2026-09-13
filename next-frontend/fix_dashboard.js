const fs = require('fs');

let content = fs.readFileSync('src/app/dashboard/page.tsx', 'utf8');

// Change grid columns
content = content.replace(
  /className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"/,
  'className="grid grid-cols-1 md:grid-cols-3 gap-4"'
);

// Remove the AI Adviser Link block
const aiLinkRegex = /<Link href="\/ai"[\s\S]*?<\/Link>/;
content = content.replace(aiLinkRegex, '');

fs.writeFileSync('src/app/dashboard/page.tsx', content);
console.log('Fixed dashboard page');
