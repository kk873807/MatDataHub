const fs = require('fs');
let code = fs.readFileSync('src/app/materials/page.tsx', 'utf-8');

const regex = /<div className="flex bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-1">[\s\S]*?<List className="w-5 h-5" \/>\s*<\/button>\s*<\/div>/;

if (regex.test(code)) {
    code = code.replace(regex, '');
    fs.writeFileSync('src/app/materials/page.tsx', code);
    console.log('Successfully removed viewMode toggle');
} else {
    console.log('Regex did not match');
}
