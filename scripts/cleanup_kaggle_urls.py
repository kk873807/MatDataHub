import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

KAGGLE_URL = 'https://www.kaggle.com/datasets/nikitamanaenkov/iron-alloys-dataset'

print("Fetching Kaggle records...")
# Use pagination since there are 1327 records and the limit is 1000
all_ids = []
page = 0
page_size = 1000

while True:
    res = supabase.table('materials').select('id, source_url').eq('source_name', 'Kaggle: Iron alloys mechanical properties').range(page * page_size, (page + 1) * page_size - 1).execute()
    data = res.data
    if not data:
        break
    for row in data:
        # Check if it needs updating (i.e. contains commas or is just wrong)
        if row['source_url'] != KAGGLE_URL:
            all_ids.append(row['id'])
    if len(data) < page_size:
        break
    page += 1

print(f"Found {len(all_ids)} Kaggle records that need their URL cleaned up.")

# Batch update them
batch_size = 100
updated = 0
for i in range(0, len(all_ids), batch_size):
    batch_ids = all_ids[i:i+batch_size]
    # Supabase in() filter
    supabase.table('materials').update({'source_url': KAGGLE_URL}).in_('id', batch_ids).execute()
    updated += len(batch_ids)
    print(f"Updated {updated}/{len(all_ids)} records")

print("Finished cleaning up Kaggle URLs!")
