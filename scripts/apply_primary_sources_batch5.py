import os
from supabase import create_client
from dotenv import load_dotenv
import re

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Primary datasheet URLs for Non-Ferrous Metals (Batch 5)
primary_sources = {
    # Aluminum
    '1050': ('https://matweb.com/search/QuickText.aspx?SearchText=Aluminum%201050', 'MatWeb (Aluminum 1050)'),
    '6061': ('https://matweb.com/search/QuickText.aspx?SearchText=Aluminum%206061', 'MatWeb (Aluminum 6061)'),
    '6101': ('https://matweb.com/search/QuickText.aspx?SearchText=Aluminum%206101', 'MatWeb (Aluminum 6101)'),
    
    # Copper Alloys (CDA - Copper Development Association standard PDFs)
    'C26000': ('https://www.copper.org/resources/properties/db/pdf/c26000.pdf', 'Copper Development Association (C26000 Cartridge Brass)'),
    'C51000': ('https://www.copper.org/resources/properties/db/pdf/c51000.pdf', 'Copper Development Association (C51000 Phosphor Bronze)'),
    
    # Titanium (TIMET primary mill PDFs)
    'Grade 2': ('https://www.timet.com/wp-content/uploads/2021/04/TIMET-CP-Titanium-Grade-2.pdf', 'TIMET (Titanium Grade 2)'),
    'Grade 5': ('https://www.timet.com/wp-content/uploads/2021/04/TIMETAL-6-4.pdf', 'TIMET (Titanium Grade 5 / Ti-6Al-4V)'),
    'Grade 23': ('https://www.timet.com/wp-content/uploads/2021/04/TIMETAL-6-4-ELI.pdf', 'TIMET (Titanium Grade 23 / Ti-6Al-4V ELI)')
}

# Be careful with 'Grade 2' matching generic things, so we will strictly match Titanium + Grade 2
target_keys = ['1050', '6061', '6101', 'C26000', 'C51000', 'Grade 2', 'Grade 5', 'Grade 23']

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
    
    url_check = r['source_url'] or ''
    if 'makeitfrom' not in url_check and 'wikipedia' not in url_check and 'kaggle' not in url_check:
        continue
        
    for key in target_keys:
        # Extra safety for Titanium grades to avoid matching "Grade 2" of some random steel
        if 'Grade' in key and 'Titanium' not in name and 'Ti-' not in name:
            continue
            
        if re.search(r'\b' + key + r'\b', name):
            url, source_name = primary_sources[key]
            updates.append({
                'id': r['id'],
                'source_url': url,
                'source_name': source_name
            })
            break

print(f"Found {len(updates)} records to update with Non-Ferrous primary datasheets.")

batch_size = 50
updated_count = 0
for i in range(0, len(updates), batch_size):
    batch = updates[i:i+batch_size]
    for item in batch:
        supabase.table('materials').update(item).eq('id', item['id']).execute()
    updated_count += len(batch)
    print(f"Updated {updated_count}/{len(updates)} records")

print("Primary source upgrade (Batch 5 - Non-Ferrous) complete.")
