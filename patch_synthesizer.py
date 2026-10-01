import os

file_path = 'next-frontend/src/app/analytics/synthesizer/page.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('!["pro", "advanced"].includes(userTier)', 'userTier !== "advanced"')
content = content.replace('The Composite Material Synthesizer is a Pro feature.', 'The Composite Material Synthesizer is an Advanced Enterprise feature.')
content = content.replace('>Upgrade Required</h2>', '>Advanced Enterprise Required</h2>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
