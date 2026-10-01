import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

key_props = ['density', 'yield_strength_min', 'thermal_conductivity', 'hardness',
             'elastic_modulus', 'tensile_strength_min', 'melting_point_min']

print("Scanning for sparse materials with valid source URLs...")
all_sparse = []
page = 0
page_size = 1000
while True:
    res = supabase.table('materials').select(
        'id, name, source_name, source_url, density, yield_strength_min, '
        'thermal_conductivity, hardness, elastic_modulus, tensile_strength_min, '
        'melting_point_min, extraction_method'
    ).range(page * page_size, (page + 1) * page_size - 1).execute()
    if not res.data:
        break
    for mat in res.data:
        url = mat.get('source_url') or ''
        source = mat.get('source_name') or ''
        
        # Skip Materials Project (DFT computed), Kaggle placeholders, and Experimental Steels
        if 'Materials Project' in source or 'Kaggle' in source:
            continue
        if 'Experimental' in (mat.get('name') or ''):
            continue
        if not url.startswith('http'):
            continue
            
        missing = sum(1 for k in key_props if mat.get(k) is None)
        if missing >= 4:  # missing at least 4 out of 7 key properties
            all_sparse.append(mat)
    if len(res.data) < page_size:
        break
    page += 1

print(f"\nFound {len(all_sparse)} materials still sparse (missing 4+ key properties).\n")

# Group by extraction method
by_method = {}
for m in all_sparse:
    method = m.get('extraction_method') or 'Unknown'
    by_method[method] = by_method.get(method, 0) + 1

print("Breakdown by extraction method:")
for method, count in sorted(by_method.items(), key=lambda x: -x[1]):
    print(f"  {method}: {count}")

# Show first 20
print(f"\nFirst 20 sparse materials:")
for m in all_sparse[:20]:
    missing = sum(1 for k in key_props if m.get(k) is None)
    print(f"  [{missing}/7 missing] {m['name']} ({m.get('extraction_method','?')}) -> {m['source_url'][:80]}")
