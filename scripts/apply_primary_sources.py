import os
from supabase import create_client
from dotenv import load_dotenv
import re

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Dictionary of primary datasheet URLs for the top grades
primary_sources = {
    '304': ('https://www.upmet.com/sites/default/files/datasheets/304-304l.pdf', 'United Performance Metals (304/304L Datasheet)'),
    '316': ('https://www.upmet.com/sites/default/files/datasheets/316-316l.pdf', 'United Performance Metals (316/316L Datasheet)'),
    '410': ('https://www.upmet.com/sites/default/files/datasheets/410.pdf', 'United Performance Metals (410 Datasheet)'),
    '440C': ('https://www.upmet.com/sites/default/files/datasheets/440c.pdf', 'United Performance Metals (440C Datasheet)'),
    'A36': ('https://www.ssab.com/-/media/files/en/ssab-steel/ssab-a36-steel-plate.pdf', 'SSAB (A36 Structural Carbon Steel Datasheet)'),
    '4140': ('https://www.asminternational.org/documents/10192/1849770/02141G_Chapter_1.pdf', 'ASM International (4140 Alloy Steel Profile)')
}

# Mapping specific keywords to their target key
target_keys = ['304', '316', '316L', '410', '440C', '4140', 'A36']

print("Fetching all materials...")
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

updates = []
for r in materials:
    name = r['name']
    
    # We only want to replace MakeItFrom or generic Wikipedia sources, not specific good sources
    if 'makeitfrom' not in (r['source_url'] or '') and 'wikipedia' not in (r['source_url'] or ''):
        continue
        
    for key in target_keys:
        if re.search(r'\b' + key + r'\b', name):
            # Special case mapping 316L to 316
            lookup_key = '316' if key == '316L' else key
            
            if lookup_key in primary_sources:
                url, source_name = primary_sources[lookup_key]
                updates.append({
                    'id': r['id'],
                    'source_url': url,
                    'source_name': source_name
                })
            break # only map the first found key

print(f"Found {len(updates)} records to update with primary mill datasheets.")

batch_size = 50
updated_count = 0
for i in range(0, len(updates), batch_size):
    batch = updates[i:i+batch_size]
    for item in batch:
        supabase.table('materials').update(item).eq('id', item['id']).execute()
    updated_count += len(batch)
    print(f"Updated {updated_count}/{len(updates)} records")

print("Primary source upgrade complete.")
