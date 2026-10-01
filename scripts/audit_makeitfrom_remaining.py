"""Audit: How many MakeItFrom materials remain, grouped by category."""
import os, re
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

print("Fetching all MakeItFrom-sourced materials...")
materials = []
page = 0
page_size = 1000
while True:
    res = supabase.table('materials').select('id, name, source_url, source_name').ilike('source_url', '%makeitfrom%').range(page * page_size, (page + 1) * page_size - 1).execute()
    if not res.data: break
    materials.extend(res.data)
    if len(res.data) < page_size: break
    page += 1

print(f"Total materials still pointing to MakeItFrom: {len(materials)}\n")

# Categorise
categories = {
    'Stainless Steel': [],
    'Carbon Steel': [],
    'Alloy Steel': [],
    'Tool Steel': [],
    'Cast Iron': [],
    'Cast Steel': [],
    'Weld Metal': [],
    'Aluminum': [],
    'Copper/Brass/Bronze': [],
    'Nickel Alloy': [],
    'Titanium': [],
    'Other': []
}

for m in materials:
    name = m['name']
    if 'Stainless' in name:
        categories['Stainless Steel'].append(m)
    elif 'Carbon Steel' in name:
        categories['Carbon Steel'].append(m)
    elif 'Tool Steel' in name or any(t in name for t in ['Cold-Work', 'Hot-Work', 'High-Speed', 'Shock-Resisting', 'Water-Hardening', 'Oil-Hardening', 'Mould Steel']):
        categories['Tool Steel'].append(m)
    elif 'Alloy Steel' in name or 'Cr-Mo' in name or 'Ni-Cr' in name or 'Boron' in name or 'Chromium Steel' in name or 'Nickel Steel' in name or 'Spring Steel' in name:
        categories['Alloy Steel'].append(m)
    elif 'Cast Iron' in name or 'Grey Cast' in name or 'Ductile' in name:
        categories['Cast Iron'].append(m)
    elif 'Cast' in name and 'Steel' in name:
        categories['Cast Steel'].append(m)
    elif 'Weld' in name or 'Filler' in name:
        categories['Weld Metal'].append(m)
    elif 'Aluminum' in name or 'Aluminium' in name:
        categories['Aluminum'].append(m)
    elif any(t in name for t in ['Copper', 'Brass', 'Bronze', 'CuNi', 'CuSn']):
        categories['Copper/Brass/Bronze'].append(m)
    elif any(t in name for t in ['Inconel', 'Monel', 'Hastelloy', 'Waspaloy', 'Nimonic']):
        categories['Nickel Alloy'].append(m)
    elif 'Titanium' in name:
        categories['Titanium'].append(m)
    else:
        categories['Other'].append(m)

for cat, items in sorted(categories.items(), key=lambda x: -len(x[1])):
    if items:
        print(f"  {cat}: {len(items)}")
        # Show 3 example names
        for item in items[:3]:
            print(f"    - {item['name']}")

# List the most "popular" remaining grades (ones with multiple variants)
print(f"\n{'='*60}")
print("Grades with the most variants still on MakeItFrom:")
print("(These are the next candidates for primary source replacement)")
print(f"{'='*60}")

# Extract base grade from name
grade_counts = {}
for m in materials:
    name = m['name']
    # Try to extract the base grade number
    match = re.search(r'\b(\d{4,5})\b', name)
    if match:
        grade = match.group(1)
        grade_counts[grade] = grade_counts.get(grade, 0) + 1

for grade, count in sorted(grade_counts.items(), key=lambda x: -x[1])[:25]:
    print(f"  {grade}: {count} variants")
