import csv
from collections import Counter

csv_path = 'Genuinely_Dead_Links.csv'
names = []
cats = Counter()
elements = {'iron', 'copper', 'aluminum', 'aluminium', 'titanium', 'gold', 'silver', 'platinum', 'magnesium', 'beryllium', 'zinc', 'lead', 'nickel', 'cobalt', 'tungsten', 'molybdenum', 'chromium', 'vanadium', 'zirconium'}

single_elements = []

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        cats[row.get('category', '')] += 1
        name = row['name']
        names.append(name)
        
        # Check if it's a single element (either exactly the element name, or starts with 'pure ')
        name_lower = name.lower().strip()
        if name_lower in elements or name_lower.startswith('pure '):
            single_elements.append(name)
            
        if i < 15:
            print(f"{name} | {row.get('category','')} | {row.get('error_status','')}")

print('\n=== Top Categories in Dead Links ===')
for c, count in cats.most_common(10):
    print(f'{count:4d} : {c}')

print(f'\nFound {len(single_elements)} strictly pure single-element names (e.g. "Iron", "Pure Gold").')
if single_elements:
    print(f"Examples: {single_elements[:5]}")
