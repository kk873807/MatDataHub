const fs = require('fs');

let content = fs.readFileSync('src/components/AccountModals.tsx', 'utf8');

// Replace the Manage Plan button
const oldManage = `<button onClick={() => alert("Billing portal integration coming soon.")} className="px-4 py-1.5 bg-white text-slate-900 rounded-lg hover:bg-slate-200 transition-colors font-bold">Manage Plan</button>`;
const newManage = `<a href="mailto:billing@matdatahub.com?subject=Manage%20Subscription%20Plan" className="px-4 py-1.5 bg-white text-slate-900 rounded-lg hover:bg-slate-200 transition-colors font-bold inline-block">Manage Plan</a>`;
content = content.replace(oldManage, newManage);

fs.writeFileSync('src/components/AccountModals.tsx', content);
console.log('Fixed Manage Plan button');
