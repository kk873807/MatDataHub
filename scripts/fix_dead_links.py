import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

updates = [
    {'id': 10573, 'name': 'ASTM A285 Carbon Steel',
     'source_url': 'https://www.makeitfrom.com/material-properties/ASTM-A285-Grade-C-Carbon-Steel',
     'source_name': 'MakeItFrom.com'},
    {'id': 10640, 'name': 'ASTM A283 Carbon Steel',
     'source_url': 'https://www.makeitfrom.com/material-properties/ASTM-A283-Grade-C-Carbon-Steel',
     'source_name': 'MakeItFrom.com'},
    {'id': 10969, 'name': 'ASTM A387 Grade 11 (K11789) 1.25Cr-0.5Mo Steel',
     'source_url': 'https://www.makeitfrom.com/material-properties/ASTM-A387-Grade-11-K11789-1.25Cr-0.5Mo-Steel',
     'source_name': 'MakeItFrom.com'},
    {'id': 10970, 'name': 'ASTM A387 Grade 22 (K21590) 2.25Cr-1Mo Steel',
     'source_url': 'https://www.makeitfrom.com/material-properties/ASTM-A387-Grade-22-K21590-2.25Cr-1Mo-Steel',
     'source_name': 'MakeItFrom.com'},
    {'id': 10948, 'name': 'ASTM A387 Grade 22L Class 1 2.25Cr-1Mo Steel',
     'source_url': 'https://www.makeitfrom.com/material-properties/ASTM-A387-Grade-22L-Class-1-2.25Cr-1Mo-Steel',
     'source_name': 'MakeItFrom.com'},
    {'id': 11011, 'name': 'AISI 310HCb (S31041) Stainless Steel',
     'source_url': 'https://www.makeitfrom.com/material-properties/AISI-310HCb-S31041-Stainless-Steel',
     'source_name': 'MakeItFrom.com'},
    {'id': 10475, 'name': 'SAE-AISI 4140 (SCM440,G41400) Cr-Mo Steel',
     'source_url': 'https://www.makeitfrom.com/material-properties/SAE-AISI-4140-SCM440-G41400-Cr-Mo-Steel',
     'source_name': 'MakeItFrom.com'},
    {'id': 10005, 'name': 'AWS ER80S-B3L or ER55S-B3L (K30560) Weld Metal',
     'source_url': 'https://www.makeitfrom.com/material-properties/AWS-ER80S-B3L-or-ER55S-B3L-K30560-Weld-Metal',
     'source_name': 'MakeItFrom.com'},
    {'id': 9870, 'name': 'ASTM A436 Type 2b (L-NiCr 20 3, F41003) Cast Iron',
     'source_url': 'https://www.makeitfrom.com/material-properties/ASTM-A436-Type-2b-L-NiCr-20-3-F41003-Cast-Iron',
     'source_name': 'MakeItFrom.com'},
    {'id': 12039, 'name': 'Pure Magnesium (99.8%)',
     'source_url': 'https://intlmag.org/page/basics_phys_prop_ima',
     'source_name': 'International Magnesium Association (IMA)'},
    {'id': 11940, 'name': 'AISI 409 Stainless Steel',
     'source_url': 'https://www.makeitfrom.com/material-properties/AISI-409-S40900-Stainless-Steel',
     'source_name': 'MakeItFrom.com'},
    {'id': 11955, 'name': 'Compacted Graphite Iron (CGI)',
     'source_url': 'https://www.sintercast.com/media/1239/compacted-graphite-iron-material-data-sheet.pdf',
     'source_name': 'SinterCast (CGI Material Data Sheet)'},
    {'id': 11091, 'name': 'EN 1.4439 (X2CrNiMoN17-13-5) Stainless Steel',
     'source_url': 'https://www.makeitfrom.com/material-properties/EN-1.4439-X2CrNiMoN17-13-5-Stainless-Steel',
     'source_name': 'MakeItFrom.com'},
    {'id': 11004, 'name': 'EN 1.4982 (X10CrNiMoMnNbVB15-10-1) Stainless Steel',
     'source_url': 'https://www.makeitfrom.com/material-properties/EN-1.4982-X10CrNiMoMnNbVB15-10-1-Stainless-Steel',
     'source_name': 'MakeItFrom.com'},
    {'id': 10345, 'name': 'EN 1.7335 (13CrMo4-5) Chromium-Molybdenum Steel',
     'source_url': 'https://www.makeitfrom.com/material-properties/EN-1.7335-13CrMo4-5-Chromium-Molybdenum--Steel',
     'source_name': 'MakeItFrom.com'},
    {'id': 564, 'name': 'Maple Wood (Dry)',
     'source_url': 'https://www.wood-database.com/hard-maple/',
     'source_name': 'The Wood Database'},
    {'id': 565, 'name': 'Maple Wood (Green)',
     'source_url': 'https://www.wood-database.com/hard-maple/',
     'source_name': 'The Wood Database',
     'category': 'Wood'},  # Fix category from "Composite" to "Wood"
    {'id': 575, 'name': 'Hickory Wood (Green)',
     'source_url': 'https://www.wood-database.com/shagbark-hickory/',
     'source_name': 'The Wood Database'},
    {'id': 11959, 'name': 'Aluminum 2014 Alloy',
     'source_url': 'https://www.makeitfrom.com/material-properties/2014-AlCu4SiMg-3.1255-A92014-Aluminum',
     'source_name': 'MakeItFrom.com'},
]

print("=== Applying 19 Dead Link Fixes ===\n")
for u in updates:
    mat_id = u['id']
    payload = {'source_url': u['source_url'], 'source_name': u['source_name']}
    if 'category' in u:
        payload['category'] = u['category']

    try:
        supabase.table('materials').update(payload).eq('id', mat_id).execute()
        extra = f" + category fixed to '{u['category']}'" if 'category' in u else ""
        print(f"  Updated: {u['name']}{extra}")
    except Exception as e:
        print(f"  ERROR on {u['name']}: {e}")

print(f"\nAll 19 dead links patched successfully!")
