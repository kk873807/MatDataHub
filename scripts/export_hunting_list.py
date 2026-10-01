import os
import csv
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

print("Fetching remaining MakeItFrom materials...")
materials = []
page = 0
page_size = 1000
while True:
    res = supabase.table('materials').select('id, name, source_url').ilike('source_url', '%makeitfrom%').range(page * page_size, (page + 1) * page_size - 1).execute()
    if not res.data:
        break
    materials.extend(res.data)
    if len(res.data) < page_size:
        break
    page += 1

csv_path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\remaining_makeitfrom_targets.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Material Name', 'Current MakeItFrom URL', 'New Primary Source URL (To be filled)', 'New Source Name (To be filled)'])
    
    # Sort alphabetically by name for easier hunting
    materials.sort(key=lambda x: x['name'])
    
    for m in materials:
        writer.writerow([
            m['id'],
            m['name'],
            m['source_url'] or '',
            '',
            ''
        ])

print(f"Exported {len(materials)} materials to {csv_path}")
