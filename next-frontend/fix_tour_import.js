const fs = require('fs');

let content = fs.readFileSync('src/components/OnboardingTour.tsx', 'utf8');

content = content.replace(
  'import Joyride, { CallBackProps, STATUS } from "react-joyride";',
  'import { Joyride, CallBackProps, STATUS } from "react-joyride";'
);

fs.writeFileSync('src/components/OnboardingTour.tsx', content);
console.log('Fixed OnboardingTour.tsx');
