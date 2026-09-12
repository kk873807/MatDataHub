const fs = require('fs');

let content = fs.readFileSync('src/components/AccountModals.tsx', 'utf8');

// Replace first paragraph
content = content.replace(
  /As an Advanced tier member, you are eligible for programmatic REST API access\./g,
  'As an Advanced tier member, you are eligible for programmatic REST API access to query our materials database. API credentials are provisioned securely by our team upon request.'
);

// Replace second paragraph
content = content.replace(
  /Your API credentials have been provisioned\./g,
  'Your API credentials have been provisioned. Contact support at support@matdatahub.com to receive your keys securely.'
);

// Specifically replace the strong tag inside the second paragraph if they wanted bold (the original had <strong>support@matdatahub.com</strong>)
content = content.replace(
  /Contact support at support@matdatahub.com to receive your keys securely\./g,
  'Contact support at <strong>support@matdatahub.com</strong> to receive your keys securely.'
);

fs.writeFileSync('src/components/AccountModals.tsx', content);
console.log('Fixed API texts');
