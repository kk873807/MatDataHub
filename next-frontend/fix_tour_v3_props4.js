const fs = require('fs');

let content = fs.readFileSync('src/components/OnboardingTour.tsx', 'utf8');

content = content.replace(/callback=/g, 'onEvent=');

fs.writeFileSync('src/components/OnboardingTour.tsx', content);
console.log('Fixed OnboardingTour.tsx v3 props 4');
