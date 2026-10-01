import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Fetch Kaggle materials
all_kaggle = []
page = 0
page_size = 1000
while True:
    res = supabase.table('materials').select('name, source_url').ilike('source_url', '%kaggle.com%').range(page * page_size, (page + 1) * page_size - 1).execute()
    if not res.data:
        break
    all_kaggle.extend(res.data)
    if len(res.data) < page_size:
        break
    page += 1

# Fetch Wikipedia materials
res_wiki = supabase.table('materials').select('name, source_url').ilike('source_url', '%wikipedia.org%').execute()
wiki_data = res_wiki.data

# Write to markdown file in the artifact directory
out_path = r'C:\Users\KISHAN\.gemini\antigravity\brain\90857fe7-b886-4dbf-9d50-6634bcd34e13\hunting_list_priority2.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('# Manual Source Hunting List: Kaggle & Wikipedia\n\n')
    f.write('This document contains the 1,666 materials that need dedicated property URLs to replace generic Kaggle and Wikipedia links.\n\n')
    
    f.write('## Wikipedia Materials (26)\n')
    f.write('| # | Material | Current URL |\n')
    f.write('|---|---|---|\n')
    for i, r in enumerate(wiki_data, 1):
        f.write(f"| {i} | {r['name']} | {r['source_url']} |\n")
        
    f.write('\n## Kaggle Materials (1,640)\n')
    f.write('*(Currently pointing to the bulk iron alloys dataset)*\n\n')
    
    # Simple grouping for Kaggle (Stainless, Cast, Weld, Other)
    stainless = [r for r in all_kaggle if 'Stainless' in r['name']]
    cast = [r for r in all_kaggle if 'Cast' in r['name']]
    weld = [r for r in all_kaggle if 'Weld' in r['name']]
    other = [r for r in all_kaggle if r not in stainless and r not in cast and r not in weld]
    
    def write_group(title, items, start_idx):
        f.write(f"### {title} ({len(items)})\n")
        f.write("| # | Material |\n")
        f.write("|---|---|\n")
        for i, r in enumerate(items, start_idx):
            f.write(f"| {i} | {r['name']} |\n")
        f.write("\n")
        return start_idx + len(items)
        
    idx = 27
    idx = write_group('Stainless Steels', stainless, idx)
    idx = write_group('Cast Steels', cast, idx)
    idx = write_group('Weld Metals', weld, idx)
    idx = write_group('Other Alloys', other, idx)

print(f'Wrote {len(wiki_data)} wiki and {len(all_kaggle)} kaggle items to {out_path}')
