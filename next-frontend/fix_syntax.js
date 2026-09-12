const fs = require('fs');

let content = fs.readFileSync('src/components/TopNav.tsx', 'utf8');

// Fix the missing closing braces
content = content.replace(
  /onClick=\{\(\) => \{ setAccountMenuOpen\(false\); setActiveAccountModal\('account'\)\} className=/g,
  `onClick={() => { setAccountMenuOpen(false); setActiveAccountModal('account'); }} className=`
);
content = content.replace(
  /onClick=\{\(\) => \{ setAccountMenuOpen\(false\); setActiveAccountModal\('billing'\)\} className=/g,
  `onClick={() => { setAccountMenuOpen(false); setActiveAccountModal('billing'); }} className=`
);
content = content.replace(
  /onClick=\{\(\) => \{ setAccountMenuOpen\(false\); setActiveAccountModal\('help'\)\} className=/g,
  `onClick={() => { setAccountMenuOpen(false); setActiveAccountModal('help'); }} className=`
);
content = content.replace(
  /onClick=\{\(\) => \{ setAccountMenuOpen\(false\); setShowShortcuts\(true\)\} className=/g,
  `onClick={() => { setAccountMenuOpen(false); setShowShortcuts(true); }} className=`
);

// If the above didn't match because of the missing }, let's do a more generic replace
content = content.replace(
  /onClick=\{\(\) => \{ setAccountMenuOpen\(false\); setActiveAccountModal\('([^']+)'\)\} className=/g,
  `onClick={() => { setAccountMenuOpen(false); setActiveAccountModal('$1'); }} className=`
);

fs.writeFileSync('src/components/TopNav.tsx', content);
console.log('Fixed syntax in TopNav');
