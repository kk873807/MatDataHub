const fs = require('fs');
let code = fs.readFileSync('src/lib/blogs.ts', 'utf-8');
const images = [
  'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=800',
  'https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&q=80&w=800',
  'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=800',
  'https://images.unsplash.com/photo-1616423640778-28d1b53229bd?auto=format&fit=crop&q=80&w=800',
  'https://images.unsplash.com/photo-1580983592398-44fb780281b3?auto=format&fit=crop&q=80&w=800'
];

let i = 0;
code = code.replace(/\{(\s+)title:/g, (match, p1) => {
  const replacement = '{' + p1 + 'image: "' + images[i % images.length] + '",' + p1 + 'title:';
  i++;
  return replacement;
});

fs.writeFileSync('src/lib/blogs.ts', code);
