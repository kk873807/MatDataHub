const fs = require('fs');
let layout = fs.readFileSync('src/app/layout.tsx', 'utf-8');
if (!layout.includes('AiChatWidget')) {
  layout = layout.replace('import { ThemeProvider } from "@/components/ThemeProvider";', 'import { ThemeProvider } from "@/components/ThemeProvider";\nimport { AiChatWidget } from "@/components/AiChatWidget";');
  layout = layout.replace('</body>', '  <AiChatWidget />\n      </body>');
  fs.writeFileSync('src/app/layout.tsx', layout, 'utf-8');
  console.log('Added AiChatWidget to layout.tsx');
}
