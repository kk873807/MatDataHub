const fs = require('fs');
let content = fs.readFileSync('src/components/TopNav.tsx', 'utf8');

// Fix the missing closing braces on setShowShortcuts
content = content.replace(
  /onClick=\{\(\) => \{ setAccountMenuOpen\(false\); setShowShortcuts\(false\)\}\>/g,
  `onClick={() => { setAccountMenuOpen(false); setShowShortcuts(false); }}>`
);
content = content.replace(
  /onClick=\{\(\) => \{ setAccountMenuOpen\(false\); setShowShortcuts\(false\)\} className=/g,
  `onClick={() => { setAccountMenuOpen(false); setShowShortcuts(false); }} className=`
);

fs.writeFileSync('src/components/TopNav.tsx', content);
console.log('Fixed second syntax error');
