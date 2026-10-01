import os
from supabase import create_client
from dotenv import load_dotenv
import re

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Primary datasheet URLs for the 12 heavy-hitters
primary_sources = {
    '4130': ('https://www.dacooper.co.uk/wp-content/uploads/2020/11/AISI-SAE-4130-Product-Datasheet-D.A.Cooper-Sons-.pdf', 'D.A. Cooper & Sons (4130)'),
    '1045': ('https://www.mwcomponents.com/uploads/Resource-Center/Elgin-Material-Sheets/Carbon-Steel-Grade-1045-Fact-Sheet_Elgin-Website.pdf', 'MW Components / Elgin (1045)'),
    '1095': ('https://dl.asminternational.org/alloy-digest/article-pdf/33/1/CS-99/366293/ad_v33_01_cs-99.pdf', 'ASM International Alloy Digest CS-99 (1095)'),
    '8620': ('https://www.mwcomponents.com/uploads/Resource-Center/Elgin-Material-Sheets/Alloy-Steel-Grade-8620-Fact-Sheet_Elgin-Website.pdf', 'MW Components / Elgin (8620)'),
    '5160': ('https://otaisteel.com/wp-content/uploads/2016/06/5160-Spring-Steel.pdf', 'Otai Special Steel (5160)'),
    '52100': ('https://carpentertechnology.com/hubfs/7407324/Material%20Saftey%20Data%20Sheets/52100.pdf', 'Carpenter Technology (52100)'),
    'A2': ('https://www.carpentertechnology.com/hubfs/7407324/Material%20Saftey%20Data%20Sheets/A2.pdf', 'Carpenter Technology (A2 Tool Steel)'),
    'W1': ('https://www.onlinemetals.com/en/product-guide/alloy/W1', 'Online Metals (W1 Tool Steel)'),
    'S7': ('https://www.carpentertechnology.com/hubfs/7407324/Material%20Saftey%20Data%20Sheets/S7.pdf', 'Carpenter Technology (S7 Tool Steel)'),
    'M2': ('https://www.carpentertechnology.com/hubfs/7407324/Material%20Saftey%20Data%20Sheets/M2%20.pdf', 'Carpenter Technology (M2 High-Speed Steel)'),
    'P20': ('https://uddeholm.com/app/uploads/sites/230/2024/05/Tech-Uddeholm-Impax-Supreme-EN.pdf.pdf', 'Uddeholm (Impax Supreme / P20 Mold Steel)'),
    '4320': ('https://www.mwcomponents.com/uploads/Resource-Center/Elgin-Material-Sheets/Alloy-Steel-Grade-4320-Fact-Sheet_Elgin-Website.pdf', 'MW Components / Elgin (4320)')
}

target_keys = ['4130', '1045', '1095', '8620', '5160', '52100', 'A2', 'W1', 'S7', 'M2', 'P20', '4320']

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
    
    # We only want to replace MakeItFrom or generic Kaggle/Wikipedia sources
    url_check = r['source_url'] or ''
    if 'makeitfrom' not in url_check and 'wikipedia' not in url_check and 'kaggle' not in url_check:
        continue
        
    for key in target_keys:
        if re.search(r'\b' + key + r'\b', name):
            url, source_name = primary_sources[key]
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

print("Primary source upgrade (Batch 3) complete.")
