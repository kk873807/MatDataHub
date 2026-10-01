import os
from supabase import create_client
from dotenv import load_dotenv
import re

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Primary datasheet URLs for the Carbon Steels (Batch 4)
# Since AZoM and MatWeb have dedicated articles/results for these, we link directly to their specific searches/articles
primary_sources = {
    '1050': ('https://matweb.com/search/QuickText.aspx?SearchText=AISI%201050', 'MatWeb (AISI 1050 Carbon Steel)'),
    '1060': ('https://matweb.com/search/QuickText.aspx?SearchText=AISI%201060', 'MatWeb (AISI 1060 Carbon Steel)'),
    '1080': ('https://matweb.com/search/QuickText.aspx?SearchText=AISI%201080', 'MatWeb (AISI 1080 Carbon Steel)'),
    '1040': ('https://matweb.com/search/QuickText.aspx?SearchText=AISI%201040', 'MatWeb (AISI 1040 Carbon Steel)'),
    '1030': ('https://matweb.com/search/QuickText.aspx?SearchText=AISI%201030', 'MatWeb (AISI 1030 Carbon Steel)'),
    '1025': ('https://matweb.com/search/QuickText.aspx?SearchText=AISI%201025', 'MatWeb (AISI 1025 Carbon Steel)'),
    '1035': ('https://www.mwcomponents.com/uploads/Resource-Center/Elgin-Material-Sheets/Carbon-Steel-Grade-1035-Fact-Sheet_Elgin-Website.pdf', 'MW Components / Elgin (1035)'),
    '1015': ('https://matweb.com/search/QuickText.aspx?SearchText=AISI%201015', 'MatWeb (AISI 1015 Carbon Steel)'),
    '1010': ('https://matweb.com/search/QuickText.aspx?SearchText=AISI%201010', 'MatWeb (AISI 1010 Carbon Steel)'),
    '1055': ('https://matweb.com/search/QuickText.aspx?SearchText=AISI%201055', 'MatWeb (AISI 1055 Carbon Steel)'),
    '1070': ('https://matweb.com/search/QuickText.aspx?SearchText=AISI%201070', 'MatWeb (AISI 1070 Carbon Steel)'),
}

target_keys = ['1050', '1060', '1080', '1040', '1030', '1025', '1035', '1015', '1010', '1055', '1070']

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
        if re.search(r'\b' + key + r'\b', name):
            url, source_name = primary_sources[key]
            updates.append({
                'id': r['id'],
                'source_url': url,
                'source_name': source_name
            })
            break

print(f"Found {len(updates)} records to update with MatWeb/Elgin datasheets.")

batch_size = 50
updated_count = 0
for i in range(0, len(updates), batch_size):
    batch = updates[i:i+batch_size]
    for item in batch:
        supabase.table('materials').update(item).eq('id', item['id']).execute()
    updated_count += len(batch)
    print(f"Updated {updated_count}/{len(updates)} records")

print("Primary source upgrade (Batch 4) complete.")
