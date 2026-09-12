const fs = require('fs');

// 1. Fix the AccountModals overlapping Zap icon
let modalsContent = fs.readFileSync('src/components/AccountModals.tsx', 'utf8');
modalsContent = modalsContent.replace(
  /<div className="absolute top-0 right-0 p-4 opacity-10"><Zap className="w-32 h-32"\/><\/div>/g,
  '<div className="absolute top-0 right-0 p-4 opacity-10 pointer-events-none"><Zap className="w-32 h-32"/></div>'
);
fs.writeFileSync('src/components/AccountModals.tsx', modalsContent);
console.log('Fixed overlapping Zap icon in AccountModals');

// 2. Fix TopNav account button not working on mobile/Vercel
let topnavContent = fs.readFileSync('src/components/TopNav.tsx', 'utf8');

if (!topnavContent.includes('const [accountMenuOpen, setAccountMenuOpen]')) {
  topnavContent = topnavContent.replace(
    /const \[activeAccountModal, setActiveAccountModal\] = useState<string \| null>\(null\);/,
    `const [activeAccountModal, setActiveAccountModal] = useState<string | null>(null);\n  const [accountMenuOpen, setAccountMenuOpen] = useState(false);`
  );
}

// Modify the button to toggle state and handle clicks outside
topnavContent = topnavContent.replace(
  /<button className="flex items-center gap-2 pl-2 pr-3 py-1.5 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">/g,
  `<button onClick={() => setAccountMenuOpen(!accountMenuOpen)} className="flex items-center gap-2 pl-2 pr-3 py-1.5 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">`
);

// Modify the dropdown container to use state and group-hover
topnavContent = topnavContent.replace(
  /className="absolute top-full right-0 mt-2 w-56 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all flex flex-col p-2 z-50"/g,
  `className={\`absolute top-full right-0 mt-2 w-56 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl transition-all flex flex-col p-2 z-50 \${accountMenuOpen ? 'opacity-100 visible' : 'opacity-0 invisible lg:group-hover:opacity-100 lg:group-hover:visible'}\`}`
);

// Also need to wrap the whole component or add a global click handler to close the menu when clicking outside.
// Actually, using onMouseLeave on the container is easier for desktop, but for mobile, clicking outside is needed.
// For now, let's just make it toggleable, and if they click an option inside, it closes.
topnavContent = topnavContent.replace(
  /onClick=\{\(\) => setActiveAccountModal/g,
  `onClick={() => { setAccountMenuOpen(false); setActiveAccountModal`
);
topnavContent = topnavContent.replace(
  /onClick=\{\(\) => setShowShortcuts/g,
  `onClick={() => { setAccountMenuOpen(false); setShowShortcuts`
);
topnavContent = topnavContent.replace(
  /onClick=\{handleLogout\}/g,
  `onClick={() => { setAccountMenuOpen(false); handleLogout(); }}`
);

// Close menu if they click outside (a simple trick is to add an invisible overlay when open)
const overlayStr = `
                      {accountMenuOpen && (
                        <div className="fixed inset-0 z-40 lg:hidden" onClick={() => setAccountMenuOpen(false)}></div>
                      )}
                      <div className="absolute top-full
`;
topnavContent = topnavContent.replace(
  /<div className=\{`absolute top-full/g,
  `{accountMenuOpen && (<div className="fixed inset-0 z-40 lg:hidden" onClick={() => setAccountMenuOpen(false)}></div>)}\n                        <div className={\`absolute top-full`
);

fs.writeFileSync('src/components/TopNav.tsx', topnavContent);
console.log('Fixed TopNav toggle menu');

