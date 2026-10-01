import os, re
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

targets = ['1045', '1095', '8620', 'A2', 'W1', 'S7', '5160', '4130', '4150', '4320', 'M2', 'P20', '52100', '1060']

page = 0
page_size = 1000
materials = []
while True:
    res = supabase.table('materials').select('id, name, source_url').ilike('source_url', '%makeitfrom%').range(page * page_size, (page + 1) * page_size - 1).execute()
    if not res.data: break
    materials.extend(res.data)
    if len(res.data) < page_size: break
    page += 1

found = {}
for r in materials:
    name = r['name']
    for t in targets:
        if re.search(r'\b' + t + r'\b', name):
            found[t] = found.get(t, []) + [r]

print("Next batch found pointing to MakeItFrom:")
for t in targets:
    if t in found:
        print(f'\n--- {t} ({len(found[t])} variants) ---')
        for item in found[t][:2]:
            print(f"  {item['name']}")
