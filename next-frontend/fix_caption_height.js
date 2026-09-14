const fs = require('fs');

const files = [
  'src/components/demos/SimulatedMaterialsDemo.tsx',
  'src/components/demos/SimulatedCompareDemo.tsx',
  'src/components/demos/SimulatedWorkspaceDemo.tsx'
];

files.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  content = content.replace(/className="mt-6 flex justify-center z-40 relative h-12"/g, 'className="mt-6 flex justify-center z-40 relative min-h-[80px]"');
  content = content.replace(/className="mt-6 flex justify-center z-40 relative h-16"/g, 'className="mt-6 flex justify-center z-40 relative min-h-[80px]"');
  fs.writeFileSync(file, content);
});
console.log('Fixed caption heights');
