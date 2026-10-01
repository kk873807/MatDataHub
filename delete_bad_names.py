
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

offset = 0
bad_ids = []
while True:
    res = supabase.table('materials').select('id, name').range(offset, offset+999).execute()
    if not res.data:
        break
    for m in res.data:
        name = m['name'] or ''
        if len(name) > 30 and ' ' not in name and any(char.isdigit() for char in name):
            bad_ids.append(m['id'])
    offset += 1000

print(f'Deleting {len(bad_ids)} materials...')
batch_size = 50
for i in range(0, len(bad_ids), batch_size):
    batch = bad_ids[i:i+batch_size]
    supabase.table('materials').delete().in_('id', batch).execute()
    print(f'Deleted batch {i//batch_size + 1}')

print('Done!')

