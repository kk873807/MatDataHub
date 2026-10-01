import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

res = supabase.table('materials').select('name, subcategory, yield_strength_min, tensile_strength_min').or_('subcategory.ilike.%alumin%,name.ilike.%alumin%').order('name').execute()

md_path = r'C:\Users\KISHAN\.gemini\antigravity\brain\eff86858-6371-4a19-a4ad-4c179410bba2\aluminum_materials.md'

with open(md_path, 'w', encoding='utf-8') as f:
    f.write('---\nsummary: "A complete list of all 122 Aluminum materials and alloys currently stored in the database."\nuser_facing: true\nrequest_feedback: false\n---\n')
    f.write('# Aluminum Materials in Database\n\n')
    f.write('Here is the complete list of all 122 Aluminum materials and alloys currently stored in your database.\n\n')
    f.write('| Material Name | Subcategory | Yield Strength (MPa) | Tensile Strength (MPa) |\n')
    f.write('|---|---|---|---|\n')
    for row in res.data:
        ys = row['yield_strength_min'] if row['yield_strength_min'] is not None else '-'
        ts = row['tensile_strength_min'] if row['tensile_strength_min'] is not None else '-'
        f.write(f"| {row['name']} | {row['subcategory'] or '-'} | {ys} | {ts} |\n")

print('Markdown Generated!')
