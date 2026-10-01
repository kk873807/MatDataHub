import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

def makeitfrom_url(name):
    slug = name.replace(' ', '-').replace('(', '').replace(')', '').replace(',', '-')
    while '--' in slug:
        slug = slug.replace('--', '-')
    return 'https://www.makeitfrom.com/material-properties/' + slug

print("Cleaning up invalid Kaggle row...")
supabase.table('materials').delete().eq('name', 'Tempering data for carbon and low alloy steels').execute()

print("Fetching Kaggle materials...")
all_kaggle = []
page = 0
page_size = 1000
while True:
    res = supabase.table('materials').select('id, name, source_url').ilike('source_url', '%kaggle.com%').range(page * page_size, (page + 1) * page_size - 1).execute()
    if not res.data:
        break
    all_kaggle.extend(res.data)
    if len(res.data) < page_size:
        break
    page += 1

print(f"Processing {len(all_kaggle)} Kaggle materials...")

updates = []
for r in all_kaggle:
    name = r['name']
    if name.startswith('Experimental Steel Grade'):
        updates.append({
            'id': r['id'],
            'source_name': 'Kaggle Dataset (Experimental - No Public Datasheet)'
        })
    else:
        new_url = makeitfrom_url(name)
        updates.append({
            'id': r['id'],
            'source_url': new_url,
            'source_name': 'MakeItFrom (Auto-Mapped)'
        })

# Batch update
batch_size = 100
updated_count = 0
for i in range(0, len(updates), batch_size):
    batch = updates[i:i+batch_size]
    for item in batch:
        supabase.table('materials').update(item).eq('id', item['id']).execute()
    updated_count += len(batch)
    print(f"Updated {updated_count}/{len(updates)} records")

print("Done with Kaggle batch.")
