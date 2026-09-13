const fs = require('fs');
let content = fs.readFileSync('src/components/AiChatWidget.tsx', 'utf8');

content = content.replace(
  /className="fixed bottom-12 left-6 lg:left-8 z-50/g,
  'className="tour-ai-widget fixed bottom-12 left-6 lg:left-8 z-50'
);

fs.writeFileSync('src/components/AiChatWidget.tsx', content);
console.log('Fixed AiChatWidget.tsx');
