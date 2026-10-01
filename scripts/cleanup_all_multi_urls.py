import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

print("Fetching all records with comma-separated URLs...")
all_ids = []
updates = []
page = 0
page_size = 1000

while True:
    res = supabase.table('materials').select('id, source_url').ilike('source_url', '%,%').range(page * page_size, (page + 1) * page_size - 1).execute()
    data = res.data
    if not data:
        break
    for row in data:
        # Split by comma and take the first URL
        first_url = row['source_url'].split(',')[0].strip()
        updates.append({'id': row['id'], 'source_url': first_url})
        
    if len(data) < page_size:
        break
    page += 1

print(f"Found {len(updates)} records that need their multi-URLs cleaned up.")

# Batch update them
batch_size = 100
updated = 0
for i in range(0, len(updates), batch_size):
    batch = updates[i:i+batch_size]
    # We can't use in_ for different values, so we update one by one or use upsert if we select everything.
    # Updating one by one in a batch using a loop
    for item in batch:
        supabase.table('materials').update({'source_url': item['source_url']}).eq('id', item['id']).execute()
    updated += len(batch)
    print(f"Updated {updated}/{len(updates)} records")

print("Finished cleaning up all multi-URLs across the database!")
