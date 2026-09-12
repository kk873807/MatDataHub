const fs = require('fs');

let listPage = fs.readFileSync('src/app/materials/page.tsx', 'utf-8');

// The line is: s.category}{s.grade ?     : ""}
// Let's replace the whole block exactly:
listPage = listPage.replace(/s\.grade \? \[^\]*\$\{s\.grade\}\ : ""/g, 's.grade ?  •  : ""');

if (!listPage.includes('ArrowLeft')) {
  listPage = listPage.replace('import { LayoutGrid, List, Search', 'import { LayoutGrid, List, Search, ArrowLeft');
}

const backHtml = '<Link href="/" className="inline-flex items-center gap-2 text-sm font-medium text-slate-500 hover:text-emerald-600 dark:text-slate-400 dark:hover:text-emerald-400 transition-colors w-fit mb-2"><ArrowLeft className="w-4 h-4" /> Back to Home</Link>';
if (!listPage.includes('Back to Home')) {
  listPage = listPage.replace('<div className="w-full max-w-7xl mx-auto flex flex-col gap-6">', '<div className="w-full max-w-7xl mx-auto flex flex-col gap-6">\n        ' + backHtml);
}
fs.writeFileSync('src/app/materials/page.tsx', listPage, 'utf-8');

let detailPage = fs.readFileSync('src/app/materials/[id]/page.tsx', 'utf-8');
detailPage = detailPage.replace(/\{material\.category\} \? \{material\.subcategory\}/g, '{material.category} • {material.subcategory}');
detailPage = detailPage.replace(/\{material\.category\} â€¢ \{material\.subcategory\}/g, '{material.category} • {material.subcategory}');
fs.writeFileSync('src/app/materials/[id]/page.tsx', detailPage, 'utf-8');
console.log('Fixed pages successfully!');
