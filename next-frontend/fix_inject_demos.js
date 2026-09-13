const fs = require('fs');

// === 1. DASHBOARD ===
let dashboard = fs.readFileSync('src/app/dashboard/page.tsx', 'utf8');

// Add imports
dashboard = dashboard.replace(
  'import { API } from "@/lib/api";',
  'import { API } from "@/lib/api";\nimport { PageDemo } from "@/components/demos/PageDemo";\nimport { SimulatedDashboardDemo } from "@/components/demos/SimulatedDashboardDemo";'
);

// Insert demo after "Here is what's happening..." paragraph
dashboard = dashboard.replace(
  '{/* Quick Actions Grid */}',
  `{/* Interactive Demo */}\n        <PageDemo pageKey="dashboard" title="See how your Dashboard works">\n          <SimulatedDashboardDemo />\n        </PageDemo>\n\n        {/* Quick Actions Grid */}`
);

fs.writeFileSync('src/app/dashboard/page.tsx', dashboard);
console.log('Injected demo into dashboard');

// === 2. MATERIALS ===
let materials = fs.readFileSync('src/app/materials/page.tsx', 'utf8');

materials = materials.replace(
  'import { API } from "@/lib/api";',
  'import { API } from "@/lib/api";\nimport { PageDemo } from "@/components/demos/PageDemo";\nimport { SimulatedMaterialsDemo } from "@/components/demos/SimulatedMaterialsDemo";'
);

// Insert after the heading section
materials = materials.replace(
  '{/* Search & Top Filters */}',
  `{/* Interactive Demo */}\n        <PageDemo pageKey="materials" title="See how Material Search works">\n          <SimulatedMaterialsDemo />\n        </PageDemo>\n\n        {/* Search & Top Filters */}`
);

fs.writeFileSync('src/app/materials/page.tsx', materials);
console.log('Injected demo into materials');

// === 3. ANALYTICS ===
let analytics = fs.readFileSync('src/app/analytics/page.tsx', 'utf8');

// Remove the old hardcoded demo section
analytics = analytics.replace(
  /import { SimulatedCompareDemo } from "@\/components\/demos\/SimulatedCompareDemo";/g,
  'import { PageDemo } from "@/components/demos/PageDemo";\nimport { SimulatedCompareDemo } from "@/components/demos/SimulatedCompareDemo";'
);

// Replace the old hardcoded demo div with PageDemo wrapper
analytics = analytics.replace(
  /<div className="mb-12">\n\s*<h2[^>]*>.*?<\/h2>\n\s*<SimulatedCompareDemo \/>\n\s*<\/div>/s,
  '<PageDemo pageKey="analytics" title="See how Compare & Analytics works">\n          <SimulatedCompareDemo />\n        </PageDemo>'
);

fs.writeFileSync('src/app/analytics/page.tsx', analytics);
console.log('Injected demo into analytics');

// === 4. WORKSPACES (projects page) ===
let projects = fs.readFileSync('src/app/projects/page.tsx', 'utf8');

projects = projects.replace(
  'import { API } from "@/lib/api";',
  'import { API } from "@/lib/api";\nimport { PageDemo } from "@/components/demos/PageDemo";\nimport { SimulatedWorkspaceDemo } from "@/components/demos/SimulatedWorkspaceDemo";'
);

// Insert after "Manage your multi-part assemblies" paragraph
projects = projects.replace(
  '<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">',
  '<PageDemo pageKey="workspaces" title="See how Engineering Workspaces work">\n            <SimulatedWorkspaceDemo />\n          </PageDemo>\n\n          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">'
);

fs.writeFileSync('src/app/projects/page.tsx', projects);
console.log('Injected demo into projects');

console.log('\nAll demos injected!');
