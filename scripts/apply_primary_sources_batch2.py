import os
from supabase import create_client
from dotenv import load_dotenv
import re

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Dictionary of primary datasheet URLs for the remaining 9 grades
primary_sources = {
    '17-4': ('https://www.carpentertechnology.com/hubfs/7407324/Material%20Saftey%20Data%20Sheets/Custom%20630%20(17-4%20PH).pdf', 'Carpenter Technology (Custom 630 / 17-4 PH)'),
    '4340': ('https://www.azom.com/article.aspx?ArticleID=6772', 'AZoM (AISI 4340)'),
    '1018': ('https://www.azom.com/article.aspx?ArticleID=9138', 'AZoM (AISI 1018)'),
    '1020': ('https://www.voestalpine.com/highperformancemetals/australia/app/uploads/sites/265/2024/08/Datasheet-1020-2026-v2.pdf', 'voestalpine (1020)'),
    'D2': ('https://www.bohler-edelstahl.com/app/uploads/sites/248/productdb/api/k110_en_gb.pdf', 'Bohler-Uddeholm (K110 / D2)'),
    'O1': ('https://uddeholm.com/app/uploads/sites/240/2024/05/Tech-Uddeholm-Arne-EN.pdf', 'Uddeholm (Arne / O1)'),
    'H13': ('https://www.uddeholm.com/app/uploads/sites/41/2023/05/Tech-Uddeholm-Orvar-Supreme-EN.pdf', 'Uddeholm (Orvar Supreme / H13)'),
    '2205': ('https://otke-cdn.outokumpu.com/-/media/files/products/forta/outokumpu-forta-range-datasheet.pdf?revision=0f5520ea-c3f6-47e5-9b4f-2edc78c9b6a0', 'Outokumpu (Forta DX 2205)'),
    '904L': ('https://swisssteel-group.com/content-media/documents/Data-Sheets/Stainless-Steel/1.4539_en.pdf', 'Swiss Steel Group (1.4539 / 904L)')
}

target_keys = ['17-4', '4340', '1018', '1020', 'D2', 'O1', 'H13', '2205', '904L']

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
    # (Since the Kaggle ones were mapped to MakeItFrom, this covers them too)
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

print("Primary source upgrade complete.")
