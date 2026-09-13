const fs = require('fs');

let content = fs.readFileSync('src/components/TopNav.tsx', 'utf8');

// Add tourClass to type NavItem
content = content.replace(
  /subItems\?: \{ name: string; href: string \}\[\];/g,
  'subItems?: { name: string; href: string }[];\n  tourClass?: string;'
);

// Add tour classes to appNavItems
content = content.replace(
  /\{ name: "Dashboard", href: "\/dashboard", icon: Home \},/g,
  '{ name: "Dashboard", href: "/dashboard", icon: Home, tourClass: "tour-dashboard" },'
);
content = content.replace(
  /\{ name: "Materials", href: "\/materials", icon: Database \},/g,
  '{ name: "Materials", href: "/materials", icon: Database, tourClass: "tour-materials" },'
);
content = content.replace(
  /\{ name: "Analytics", href: "\/analytics", icon: BarChart3 \},/g,
  '{ name: "Analytics", href: "/analytics", icon: BarChart3, tourClass: "tour-analytics" },'
);
content = content.replace(
  /\{ name: "Workspaces", href: "\/projects", icon: Workflow \},/g,
  '{ name: "Workspaces", href: "/projects", icon: Workflow, tourClass: "tour-projects" },'
);

// Apply to rendering
const oldLink = `                      <Link
                        key={item.name}
                        href={item.href!}
                        className={\`flex items-center gap-2 px-3 py-2 rounded-full text-sm font-medium transition-all \${
                          isActive 
                            ? "bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-white" 
                            : "text-slate-600 hover:bg-slate-50 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-800/50 dark:hover:text-white"
                        }\`}`;

const newLink = `                      <Link
                        key={item.name}
                        href={item.href!}
                        className={\`\${item.tourClass || ''} flex items-center gap-2 px-3 py-2 rounded-full text-sm font-medium transition-all \${
                          isActive 
                            ? "bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-white" 
                            : "text-slate-600 hover:bg-slate-50 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-800/50 dark:hover:text-white"
                        }\`}`;

content = content.replace(oldLink, newLink);

// And for the account menu toggle button
content = content.replace(
  /<button\s+onClick=\{\(\) => setAccountMenuOpen\(!accountMenuOpen\)\}\s+className="flex items-center gap-2 p-1\.5 pr-3 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"/g,
  '<button onClick={() => setAccountMenuOpen(!accountMenuOpen)} className="tour-account flex items-center gap-2 p-1.5 pr-3 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"'
);

fs.writeFileSync('src/components/TopNav.tsx', content);
console.log('Fixed TopNav tour classes');
