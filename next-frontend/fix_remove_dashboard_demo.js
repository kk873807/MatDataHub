const fs = require('fs');

// Remove PageDemo import and dashboard demo from dashboard page
let dashboard = fs.readFileSync('src/app/dashboard/page.tsx', 'utf8');
dashboard = dashboard.replace(/import { PageDemo } from "@\/components\/demos\/PageDemo";\n/, '');
dashboard = dashboard.replace(/import { SimulatedDashboardDemo } from "@\/components\/demos\/SimulatedDashboardDemo";\n/, '');
dashboard = dashboard.replace(/\{\/\* Interactive Demo \*\/\}\n\s*<PageDemo pageKey="dashboard" title="See how your Dashboard works">\n\s*<SimulatedDashboardDemo \/>\n\s*<\/PageDemo>\n\n\s*/g, '');
fs.writeFileSync('src/app/dashboard/page.tsx', dashboard);
console.log('Removed dashboard demo');
