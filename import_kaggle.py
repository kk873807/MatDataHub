
import os, csv
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

materials = []
with open('steel_strength.csv', 'r') as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader):
        try:
            yield_str = float(row['yield strength']) if row['yield strength'] else None
        except: yield_str = None
        
        try:
            tensile_str = float(row['tensile strength']) if row['tensile strength'] else None
        except: tensile_str = None
        
        try:
            elongation = float(row['elongation']) if row['elongation'] else None
        except: elongation = None

        formula = row['formula']
        
        # Build a readable composition string from the percentages
        comp_parts = []
        for el in ['c', 'mn', 'si', 'cr', 'ni', 'mo', 'v', 'n', 'nb', 'co', 'w', 'al', 'ti']:
            val = float(row[el]) if row[el] else 0
            if val > 0:
                comp_parts.append(f'{el.capitalize()} {val}%')
        composition_str = ', '.join(comp_parts)

        mat = {
            'name': f'Experimental Steel Grade {idx+1}',
            'category': 'Metal',
            'subcategory': 'Computational Steel',
            'yield_strength_min': yield_str,
            'tensile_strength_min': tensile_str,
            'elongation': elongation,
            'composition': composition_str,
            'description': f'Computational formula: {formula}',
            'source_name': 'Kaggle (ritwikbasu)',
            'source_url': 'https://www.kaggle.com/datasets/ritwikbasu/steel-properties-and-composition',
            'extraction_method': 'CSV Import (Kaggle Dataset)'
        }
        materials.append(mat)

print(f'Parsed {len(materials)} materials. Inserting...')

# Insert in batches of 50
batch_size = 50
for i in range(0, len(materials), batch_size):
    batch = materials[i:i+batch_size]
    supabase.table('materials').insert(batch).execute()
    print(f'Inserted batch {i//batch_size + 1}')

print('Done!')

