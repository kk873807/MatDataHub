const fs = require('fs');
let code = fs.readFileSync('src/lib/blogs.ts', 'utf-8');

const features = [
  { name: 'Explore Materials Database', link: '/materials' },
  { name: 'Try Compare Tool', link: '/analytics/compare' },
  { name: 'Try CBAM Calculator', link: '/analytics/cbam' },
  { name: 'Try Composite Synthesizer', link: '/analytics/synthesizer' },
  { name: 'Try AI Material Advisor', link: '/dashboard' },
  { name: 'Try AI Substitution', link: '/analytics/substitution' },
  { name: 'Try CBAM Calculator', link: '/analytics/cbam' },
  { name: 'Explore Workspaces', link: '/projects' }
];

let i = 0;
code = code.replace(/featured:\s*(true|false),/g, (match) => {
  const replacement = match + '\n      featureName: "' + features[i].name + '", featureLink: "' + features[i].link + '",';
  i++;
  return replacement;
});

fs.writeFileSync('src/lib/blogs.ts', code);
