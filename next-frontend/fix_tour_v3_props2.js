const fs = require('fs');

let content = fs.readFileSync('src/components/OnboardingTour.tsx', 'utf8');

// Remove showSkipButton
content = content.replace(
  /showSkipButton/g,
  ''
);

fs.writeFileSync('src/components/OnboardingTour.tsx', content);
console.log('Fixed OnboardingTour.tsx v3 props 2');
