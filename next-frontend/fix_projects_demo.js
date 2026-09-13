const fs = require('fs');
let content = fs.readFileSync('src/app/projects/page.tsx', 'utf8');

// Remove the incorrectly placed demo
content = content.replace(
  `          <PageDemo pageKey="workspaces" title="See how Engineering Workspaces work">
            <SimulatedWorkspaceDemo />
          </PageDemo>\n\n`,
  ''
);

// Now insert it in the right place - after the heading/description section, before the conditional blocks
// Find the search bar section
content = content.replace(
  `<p className="text-slate-600 dark:text-slate-300 mt-2">Manage your multi-part assemblies and interactive blueprints.</p>`,
  `<p className="text-slate-600 dark:text-slate-300 mt-2">Manage your multi-part assemblies and interactive blueprints.</p>
          </div>
          <PageDemo pageKey="workspaces" title="See how Engineering Workspaces work">
            <SimulatedWorkspaceDemo />
          </PageDemo>
          <div>`
);

fs.writeFileSync('src/app/projects/page.tsx', content);
console.log('Fixed projects page');
