import os
import re
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

res = supabase.table('materials').select('name').or_('subcategory.ilike.%alumin%,name.ilike.%alumin%').execute()

db_names = [m['name'] for m in res.data]
# Extract the 4 digit codes
db_codes = set()
for name in db_names:
    match = re.search(r'\b[1-8]\d{3}[A-Z]?\b', name)
    if match:
        db_codes.add(match.group(0))

standard_alloys = {
    '1000 Series (Pure Aluminum)': ['1050', '1060', '1070', '1100', '1145', '1199', '1200', '1350'],
    '2000 Series (Copper)': ['2011', '2014', '2017', '2024', '2090', '2099', '2124', '2219', '2324'],
    '3000 Series (Manganese)': ['3003', '3004', '3005', '3103', '3105'],
    '4000 Series (Silicon)': ['4032', '4043', '4047', '4145', '4643'],
    '5000 Series (Magnesium)': ['5005', '5052', '5059', '5083', '5086', '5154', '5182', '5251', '5356', '5454', '5456', '5754'],
    '6000 Series (Magnesium & Silicon)': ['6005', '6005A', '6013', '6026', '6060', '6061', '6063', '6082', '6101', '6262', '6463'],
    '7000 Series (Zinc)': ['7005', '7020', '7039', '7049', '7050', '7068', '7075', '7150', '7175', '7475'],
    '8000 Series (Other Elements)': ['8006', '8011', '8090']
}

missing_alloys = {}
for series, alloys in standard_alloys.items():
    missing = [a for a in alloys if a not in db_codes and a + 'A' not in db_codes and a.replace('A','') not in db_codes]
    if missing:
        missing_alloys[series] = missing

md_path = r'C:\Users\KISHAN\.gemini\antigravity\brain\eff86858-6371-4a19-a4ad-4c179410bba2\missing_aluminum.md'
with open(md_path, 'w') as f:
    f.write('---\nsummary: "A list of common standard Aluminum alloys that are currently missing from the database."\nuser_facing: true\nrequest_feedback: false\n---\n')
    f.write('# Missing Aluminum Alloys\n\n')
    f.write('The Aluminum Association has registered over a thousand distinct wrought alloys, but many are obscure, highly specific, or obsolete. Below is a list of the **most common and widely-used standard commercial grades** across the 1000-8000 series that are currently **missing** from your database (Note: the 9000 series is currently unassigned/unused by the Aluminum Association).\n\n')
    
    for series, missing in missing_alloys.items():
        f.write(f'### {series}\n')
        for alloy in missing:
            f.write(f'- {alloy}\n')
        f.write('\n')

print('Missing alloys calculated!')
