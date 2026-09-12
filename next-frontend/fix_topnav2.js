const fs = require('fs');

let content = fs.readFileSync('src/components/TopNav.tsx', 'utf8');

// 1. Add import
if (!content.includes('AccountModals')) {
    content = content.replace(/import \{ LoginModal \} from "\.\/LoginModal";/, 'import { LoginModal } from "./LoginModal";\nimport { AccountModals } from "./AccountModals";');
}

// 2. Add state
if (!content.includes('activeAccountModal')) {
    content = content.replace(
        /const \[showShortcuts, setShowShortcuts\] = useState\(false\);/,
        `const [showShortcuts, setShowShortcuts] = useState(false);\n  const [activeAccountModal, setActiveAccountModal] = useState<string | null>(null);`
    );
}

// 3. Replace Account Management Link
content = content.replace(
    /<Link href="\/account" className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors">\s*<Settings className="w-4 h-4" \/> Account Management\s*<\/Link>/g,
    `<button onClick={() => setActiveAccountModal('account')} className="w-full text-left flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors">
                            <Settings className="w-4 h-4" /> Account Management
                          </button>`
);

// 4. Replace Transactions & Billing Link
content = content.replace(
    /<Link href="\/account\?tab=billing" className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors">\s*<CreditCard className="w-4 h-4" \/> Transactions & Billing\s*<\/Link>/g,
    `<button onClick={() => setActiveAccountModal('billing')} className="w-full text-left flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors">
                            <CreditCard className="w-4 h-4" /> Transactions & Billing
                          </button>`
);

// 5. Replace Help Centre & Legal Link
content = content.replace(
    /<Link href="\/contact" className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors">\s*<LifeBuoy className="w-4 h-4" \/> Help Centre & Legal\s*<\/Link>/g,
    `<button onClick={() => setActiveAccountModal('help')} className="w-full text-left flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors">
                            <LifeBuoy className="w-4 h-4" /> Help Centre & Legal
                          </button>`
);

// 6. Add modal rendering
if (!content.includes('<AccountModals')) {
    content = content.replace(
        /<LoginModal isOpen=\{showLoginModal\} onClose=\{\(\) => setShowLoginModal\(false\)\} \/>/,
        `<AccountModals activeModal={activeAccountModal} setActiveModal={setActiveAccountModal} userInfo={userInfo} />\n      <LoginModal isOpen={showLoginModal} onClose={() => setShowLoginModal(false)} />`
    );
}

fs.writeFileSync('src/components/TopNav.tsx', content);
console.log('Fixed TopNav dropdown items');
