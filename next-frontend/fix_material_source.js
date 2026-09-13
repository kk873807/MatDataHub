const fs = require('fs');

let content = fs.readFileSync('src/app/materials/[id]/page.tsx', 'utf8');

const oldSource = `<div className="pt-2 border-t border-slate-200 dark:border-slate-800">
                  <span className="text-slate-600 dark:text-slate-300 block text-xs">
                    Data Source
                  </span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-medium">
                    {material.data_source || "Verified Internal Database"}
                  </span>
                </div>`;

const newSource = `<div className="pt-2 border-t border-slate-200 dark:border-slate-800 relative group cursor-pointer">
                  <span className="text-slate-600 dark:text-slate-300 block text-xs flex items-center gap-1">
                    Data Source <Info className="w-3 h-3 text-slate-400" />
                  </span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-medium border-b border-dashed border-emerald-400/50">
                    {material.data_source || "Verified Internal Database"}
                  </span>
                  <div className="absolute bottom-full left-0 mb-2 w-72 bg-slate-900 dark:bg-slate-800 text-white text-xs rounded-xl p-3 shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
                    All material properties, supply chain math, economics, and ESG/CBAM emission factors are rigorously sourced from verified industry standards (ASTM, ISO, DIN), reputable global commodities indices, and validated scientific databases (e.g., ICE DB University of Bath).
                    <div className="absolute top-full left-4 -mt-1 border-4 border-transparent border-t-slate-900 dark:border-t-slate-800"></div>
                  </div>
                </div>`;

content = content.replace(oldSource, newSource);
fs.writeFileSync('src/app/materials/[id]/page.tsx', content);
console.log('Fixed Data Source tooltip');
