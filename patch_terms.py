import os

file_path = 'next-frontend/src/app/terms/page.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

ip_clause = """        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">2. Intellectual Property & Anti-Scraping</h2>
          <p>
            All content, database schemas, material datasets, proprietary algorithms (including the Rule of Mixtures and CBAM equations), and user interfaces on MatDataHub are the exclusive intellectual property of MatDataHub and are protected by international copyright laws. 
          </p>
          <ul className="list-disc pl-6 mt-3 space-y-2">
            <li><strong>No Data Scraping:</strong> Automated scraping, crawling, or mass-downloading of our material database is strictly prohibited. Violators will face immediate permanent IP bans and legal action.</li>
            <li><strong>No Derivative Works:</strong> You may not copy, reverse-engineer, or resell our datasets, calculators, or platform features to build a competing product.</li>
            <li><strong>Watermarking:</strong> Data exports and generated PDF reports contain cryptographic and visual watermarks to track unauthorized redistribution of our proprietary data.</li>
          </ul>
        </section>
"""

if 'Anti-Scraping' not in content:
    # Find the second section to insert this as section 2
    content = content.replace('<section>', '<section>', 1) # dummy
    parts = content.split('</section>')
    if len(parts) > 1:
        parts[0] = parts[0] + '</section>\n' + ip_clause
        content = "".join(parts)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
