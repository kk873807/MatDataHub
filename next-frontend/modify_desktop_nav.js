const fs = require('fs');
let code = fs.readFileSync('src/components/TopNav.tsx', 'utf-8');

const oldMap = \{appNavItems.map((item) => {
                  const isActive = pathname === item.href || (item.href !== "/" && pathname?.startsWith(item.href));
                  return (
                    <Link
                      key={item.name}
                      href={item.href}
                      className={\\\lex items-center gap-2 px-3 py-2 rounded-full text-sm font-medium transition-all \\\\}
                    >
                      <item.icon className="w-4 h-4" />
                      {item.name}
                    </Link>
                  );
                })}\;

const newMap = \{appNavItems.map((item) => {
                  if (item.subItems) {
                    return (
                      <div key={item.name} className="relative group">
                        <button className="flex items-center gap-1.5 px-3 py-2 rounded-full text-sm font-medium transition-all text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-white">
                          <item.icon className="w-4 h-4" />
                          {item.name}
                          <ChevronDown className="w-3 h-3 ml-0.5 opacity-50" />
                        </button>
                        <div className="absolute top-full left-0 mt-2 w-48 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all flex flex-col p-2 z-50">
                          {item.subItems.map(sub => (
                            <Link key={sub.name} href={sub.href} className="px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors">
                              {sub.name}
                            </Link>
                          ))}
                        </div>
                      </div>
                    );
                  }

                  const isActive = item.href && (pathname === item.href || (item.href !== "/" && pathname?.startsWith(item.href)));
                  return (
                    <Link
                      key={item.name}
                      href={item.href!}
                      className={\\\lex items-center gap-2 px-3 py-2 rounded-full text-sm font-medium transition-all \\\\}
                    >
                      <item.icon className="w-4 h-4" />
                      {item.name}
                    </Link>
                  );
                })}\;

code = code.replace(oldMap, newMap);
fs.writeFileSync('src/components/TopNav.tsx', code);
console.log('Fixed desktop map');
