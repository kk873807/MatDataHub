const fs = require('fs');
let topNav = fs.readFileSync('src/components/TopNav.tsx', 'utf-8');
topNav = topNav.replace('{ name: "AI Adviser", href: "/ai", icon: Bot },\n  ', '');
fs.writeFileSync('src/components/TopNav.tsx', topNav, 'utf-8');
console.log('Removed AI Adviser from TopNav.tsx');
