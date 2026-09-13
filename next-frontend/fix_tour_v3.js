const fs = require('fs');

let content = fs.readFileSync('src/components/OnboardingTour.tsx', 'utf8');

content = content.replace(
  'import { Joyride, CallBackProps, STATUS } from "react-joyride";',
  'import { Joyride, STATUS } from "react-joyride";'
);

content = content.replace(
  'const handleJoyrideCallback = (data: CallBackProps) => {',
  'const handleJoyrideCallback = (data: any) => {'
);

// Remove styles prop completely
const stylesPropRegex = /styles=\{\{[\s\S]*?\}\}/g;
content = content.replace(stylesPropRegex, '');

fs.writeFileSync('src/components/OnboardingTour.tsx', content);
console.log('Fixed OnboardingTour.tsx v3');
