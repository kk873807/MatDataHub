import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

materials = []
page = 0
page_size = 1000
while True:
    res = supabase.table('materials').select('id, name, source_url').range(page * page_size, (page + 1) * page_size - 1).execute()
    if not res.data:
        break
    materials.extend(res.data)
    if len(res.data) < page_size:
        break
    page += 1

garbage_keywords = [
    '.pdf', '.ashx', 'Technical Datasheets', 'General Information', 'Material Safety',
    '404 -', 'Not Found', '.html', 'Data Sheet'
]

garbage_ids = []
print('Found garbage materials:')
for m in materials:
    name = m['name'].strip()
    is_garbage = False
    
    if any(k.lower() in name.lower() for k in garbage_keywords):
        is_garbage = True
    elif len(name) < 2:
        is_garbage = True
    elif 'error' in name.lower() and 'steel' not in name.lower() and 'alloy' not in name.lower():
        is_garbage = True
        
    if is_garbage:
        print(f"- [{m['id']}] {name} ({m['source_url']})")
        garbage_ids.append(m['id'])

print(f'\\nTotal garbage identified: {len(garbage_ids)}')

# Delete them!
if garbage_ids:
    for i in range(0, len(garbage_ids), 50):
        batch = garbage_ids[i:i+50]
        supabase.table('materials').delete().in_('id', batch).execute()
    print('Deleted successfully.')
