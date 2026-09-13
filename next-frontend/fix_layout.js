const fs = require('fs');
let content = fs.readFileSync('src/app/layout.tsx', 'utf8');

// Add import
content = content.replace(
  'import { AiChatWidget } from "@/components/AiChatWidget";',
  'import { AiChatWidget } from "@/components/AiChatWidget";\nimport { OnboardingTour } from "@/components/OnboardingTour";'
);

// Add component
content = content.replace(
  '<AiChatWidget />',
  '<AiChatWidget />\n        <OnboardingTour />'
);

fs.writeFileSync('src/app/layout.tsx', content);
console.log('Fixed layout.tsx');
