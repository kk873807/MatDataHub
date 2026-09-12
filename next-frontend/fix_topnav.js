const fs = require('fs');

let content = fs.readFileSync('src/components/TopNav.tsx', 'utf8');

// 1. Add showShortcuts state
content = content.replace(
    /const \[showLoginModal, setShowLoginModal\] = useState\(false\);/,
    `const [showLoginModal, setShowLoginModal] = useState(false);\n  const [showShortcuts, setShowShortcuts] = useState(false);`
);

// 2. Add X import if missing
if (!content.includes(' X ')) {
    content = content.replace(/import \{ (.*?) \} from "lucide-react";/, 'import { $1, X } from "lucide-react";');
}

// 3. Replace alert() with setShowShortcuts(true)
content = content.replace(
    /onClick=\{\(\) => alert\('Keyboard shortcuts:\\nCtrl\+K: Search\\nCtrl\+\/: Shortcuts'\)\}/,
    `onClick={() => setShowShortcuts(true)}`
);

// 4. Add the modal before <LoginModal
const modalJSX = `
      {showShortcuts && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-sm" onClick={() => setShowShortcuts(false)}>
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl w-full max-w-sm p-6 animate-in zoom-in-95" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-slate-900 dark:text-white flex items-center gap-2"><Keyboard className="w-5 h-5"/> Keyboard Shortcuts</h3>
              <button onClick={() => setShowShortcuts(false)} className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"><X className="w-5 h-5"/></button>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-slate-50 dark:bg-slate-800/50 rounded-xl">
                <span className="text-sm font-medium text-slate-700 dark:text-slate-300">Global Search</span>
                <kbd className="px-2 py-1 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded shadow-sm text-xs font-mono text-slate-500 dark:text-slate-400">Ctrl + K</kbd>
              </div>
              <div className="flex justify-between items-center p-3 bg-slate-50 dark:bg-slate-800/50 rounded-xl">
                <span className="text-sm font-medium text-slate-700 dark:text-slate-300">Open Shortcuts</span>
                <kbd className="px-2 py-1 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded shadow-sm text-xs font-mono text-slate-500 dark:text-slate-400">Ctrl + /</kbd>
              </div>
              <div className="flex justify-between items-center p-3 bg-slate-50 dark:bg-slate-800/50 rounded-xl">
                <span className="text-sm font-medium text-slate-700 dark:text-slate-300">AI Advisor</span>
                <kbd className="px-2 py-1 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded shadow-sm text-xs font-mono text-slate-500 dark:text-slate-400">Ctrl + J</kbd>
              </div>
            </div>
            <button onClick={() => setShowShortcuts(false)} className="w-full mt-6 py-2.5 bg-slate-900 dark:bg-white hover:bg-slate-800 dark:hover:bg-slate-100 text-white dark:text-slate-900 rounded-xl font-bold text-sm transition-colors">
              Got it
            </button>
          </div>
        </div>
      )}
`;

content = content.replace(/<LoginModal isOpen=\{showLoginModal\}/, modalJSX + '\n      <LoginModal isOpen={showLoginModal}');

fs.writeFileSync('src/components/TopNav.tsx', content);
console.log('Fixed TopNav shortcuts modal');
