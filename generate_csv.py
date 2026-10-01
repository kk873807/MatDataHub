
import os
import csv
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

res = supabase.table('materials').select('name, category, subcategory, yield_strength_min, tensile_strength_min').or_('subcategory.ilike.%alumin%,name.ilike.%alumin%').order('name').execute()

os.makedirs(r'C:\Users\KISHAN\.gemini\antigravity\brain\eff86858-6371-4a19-a4ad-4c179410bba2\scratch', exist_ok=True)
csv_path = r'C:\Users\KISHAN\.gemini\antigravity\brain\eff86858-6371-4a19-a4ad-4c179410bba2\scratch\aluminum_materials.csv'

with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Category', 'Subcategory', 'Yield Strength (MPa)', 'Tensile Strength (MPa)'])
    for row in res.data:
        writer.writerow([
            row['name'],
            row['category'] or '',
            row['subcategory'] or '',
            row['yield_strength_min'] or '',
            row['tensile_strength_min'] or ''
        ])

print('CSV Generated!')

