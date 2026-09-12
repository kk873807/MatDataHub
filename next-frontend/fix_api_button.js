const fs = require('fs');

let content = fs.readFileSync('src/components/AccountModals.tsx', 'utf8');

// 1. Add pointer-events-none to the decorative blur div
content = content.replace(
  /<div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500\/10 rounded-full blur-3xl"><\/div>/g,
  '<div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>'
);

// 2. Make the generate API keys button have relative z-10 and prevent bubbling
content = content.replace(
  /<button onClick=\{generateApiKeys\} className="px-6 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl transition-colors flex items-center gap-2">/g,
  '<button onClick={(e) => { e.preventDefault(); e.stopPropagation(); generateApiKeys(); }} className="px-6 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl transition-colors flex items-center gap-2 relative z-10 cursor-pointer">'
);

// 3. Improve the alert error message so we know if it's an API failure
content = content.replace(
  /alert\("Failed to generate API credentials."\);/g,
  `const errData = await res.json().catch(() => ({})); alert("Failed to generate API credentials: " + (errData.detail || "Server Error"));`
);

fs.writeFileSync('src/components/AccountModals.tsx', content);
console.log('Fixed API button');
