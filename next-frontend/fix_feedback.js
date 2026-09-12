const fs = require('fs');
let code = fs.readFileSync('src/app/feedback/page.tsx', 'utf-8');

code = code.replace(/bg-blue-100 dark:bg-blue-100 dark:bg-blue-900\/20/g, 'bg-blue-100 dark:bg-blue-900/20');
code = code.replace(/text-slate-500 dark:text-slate-400 hover:text-slate-600 dark:text-slate-300 dark:hover:text-slate-600 dark:text-slate-300/g, 'text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200');
code = code.replace(/bg-slate-100 dark:bg-slate-800 hover:bg-slate-700 text-slate-200/g, 'bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300');
code = code.replace(/text-blue-600 dark:text-blue-600 dark:text-blue-400/g, 'text-blue-600 dark:text-blue-400');

fs.writeFileSync('src/app/feedback/page.tsx', code);
console.log('Fixed feedback contrast');
