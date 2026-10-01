import os
import re
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

targets = ['304', '316', '316L', '410', '420', '440C', '17-4', '15-5', '4140', '4340', '1018', '1020', 'A36', 'D2', 'O1', 'H13', '2205', '904L', '8620']

res = supabase.table('materials').select('id, name, source_url').ilike('source_url', '%makeitfrom%').execute()

found = {}
for r in res.data:
    name = r['name']
    for t in targets:
        if re.search(r'\b' + t + r'\b', name):
            found[t] = found.get(t, []) + [r]

print("Top grades found pointing to MakeItFrom:")
for t in targets:
    if t in found:
        print(f'\n--- {t} ---')
        for item in found[t][:5]:
            print(f"  {item['name']}")
