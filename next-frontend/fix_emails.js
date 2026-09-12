const fs = require('fs');
const files = [
  'src/app/account/page.tsx',
  'src/app/contact/page.tsx',
  'src/components/AccountModals.tsx'
];

files.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  content = content.replace(/support@matdatahub\.com/g, 'matdatahub.support@gmail.com');
  content = content.replace(/billing@matdatahub\.com/g, 'matdatahub.support@gmail.com');
  fs.writeFileSync(file, content);
});
console.log('Fixed emails in all files');
