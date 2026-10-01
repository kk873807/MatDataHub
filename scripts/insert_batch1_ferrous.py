import os
import csv
from io import StringIO
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

csv_data = """category,subcategory,name,density,tensile_strength_min,yield_strength_min,elongation,hardness,elastic_modulus,thermal_conductivity,specific_heat,melting_point_min,composition,description,source_url
Steel,Free Machining Steel,AISI 1215 Free Machining Steel,7.87,540,415,10,167 HB,200,,,,"C <=0.09%, Mn 0.75-1.05%, P 0.04-0.09%, S 0.26-0.35%, Fe balance","Cold drawn (19-38 mm round) condition; resulfurized/rephosphorized free-machining low-carbon screw stock steel. UNS G12150; ASTM A29/A108.",https://www.matweb.com/search/datasheet.aspx?matguid=1df1e9e661684d75bf2fa0cc303e5fd7
Steel,HSLA Steel,Hy-100 High-Yield Steel,7.83,792,690,"18 (L) / 16 (T)",230-290 HB,200,25,460,1450,"C 0.10-0.20, Mn 0.10-0.40, Si 0.15-0.35, Cr 1.35-1.80, Ni 2.75-3.50, Mo 0.30-0.60, P <=0.015, S <=0.004, Fe balance","Quenched & tempered Ni-Cr-Mo low-alloy steel per MIL-S-21952 / T9074-BD-GIB-010/0300; min. 100 ksi yield; submarine pressure hulls, pressure vessels, naval construction. Tensile/yield shown are minimums of the specified range (792-930 / 690-897 MPa).",https://www.wieland-diversified.com/hy-80-100-steels/hy-100-steel/
Steel,HSLA Steel,Hy-80 High-Yield Steel,7.83,690,552,"20 (L) / 18 (T)",230-290 HB,200,25,460,1450,"Fe 93.1-96.4, Ni 2.0-3.25, Cr 1.0-1.80, Mo 0.20-0.60, Si 0.15-0.35, C 0.12-0.18, Mn 0.10-0.40, Cu <=0.25, P <=0.025, S <=0.025","Quenched & tempered Ni-Cr-Mo martensitic steel per MIL-S-16216 / MIL-S-21952; min. 80 ksi yield; developed for US Navy submarine pressure hulls. Tensile/yield shown are minimums of the specified range (690-827 / 552-686 MPa). Composition per AZoM (see second source).",https://www.wieland-diversified.com/hy-80-100-steels/hy-80-steel/ | composition: https://www.azom.com/article.aspx?ArticleID=6720
Steel,Maraging Steel,Maraging Steel 250,8.02,1758,1724,6,>=48 HRC,193,25.5,450,1413,"Ni 17.0-19.0, Co 7.0-8.5, Mo 4.6-5.2, Ti 0.3-0.5, Al 0.05-0.15, Mn <=0.10, Si <=0.10, C <=0.03, Fe balance","Age-hardened (maraged) 18% Ni-Co-Mo ultra-high-strength steel per AMS 6512 / MIL-S-46850 / UNS K92890; missile & ejector systems, slat tracks, drive shafts. Density from Alloys International datasheet (secondary source).",https://www.aircraftmaterials.com/data/nickel/C250.html
Steel,Maraging Steel,Maraging Steel 300,8.02,1999,1931,8,52 HRC,190,21,450,1413,"C <=0.03, Co 8.0-9.5, Ni 18.0-19.0, Mo 4.6-5.2, Ti 0.55-0.80, Al 0.05-0.15, Mn <=0.10, Si <=0.10, Fe balance","Age-hardened 18% Ni-Co-Mo maraging steel per AMS 6514/6521, MIL-S-46850 / UNS K93120; tooling, transmission shafts, motorsport components, landing gear. Values shown are for the solution-annealed + aged (900F/482C) condition.",https://www.aircraftmaterials.com/data/nickel/C300.html
Steel,Maraging Steel,Maraging Steel 350,8.08,2413,2275,8,60 HRC,200,21,450,1413,"Ni 18.50, Co 12.0, Mo 4.8, Ti 1.40, Al 0.10, Mn <=0.10, Si <=0.10, C <=0.03, B 0.003, P <=0.01, S <=0.01, Zr 0.01, Fe balance","Cobalt-strengthened 18% Ni maraging steel per AMS 6515 / MIL-S-46850 / UNS K93160; missile & rocket motor cases, landing gear components, high-performance shafting and fasteners.",https://www.aircraftmaterials.com/data/nickel/C350.html
Steel,Low Expansion Alloy,Invar 36 (Fe-Ni Alloy),8.05,490,240,42,,141-148,10.5,515,1427,"Ni 35-38%, C <=0.10, Mn <=0.06, P <=0.025, S <=0.025, Si <=0.35, Cr <=0.50, Mo <=0.50, Co <=1.0, Fe balance","36% Ni-Fe low-expansion alloy; CTE approx. 1.2x10^-6/C near room temperature. Precision instruments, optical/laser systems, aerospace tooling, cryogenic tanks & piping. Mechanical properties (annealed) from Aircraft Materials; physical/thermal properties from High Temp Metals (second source).",https://www.aircraftmaterials.com/data/nickel/al36.html | physical/thermal: https://www.hightempmetals.com/techdata/hitempInvar36data.php
Steel,Controlled Expansion Alloy,Kovar (Fe-Ni-Co Alloy),8.36,518,276,30,80 HRB,207,17,460,1449,"Fe balance, Ni 29%, Co 17%, C 0.02%, Cr 0.2%, Si 0.2%","Fe-Ni-Co (29/17) controlled-expansion glass-sealing alloy per ASTM F15; CTE matched to borosilicate glass & alumina ceramics; used for glass-to-metal hermetic seals, transistor/IC lead frames, vacuum tube leads.",https://www.hightempmetals.com/techdata/hitempKovardata.php
"""

import re
def sanitize_float(val):
    if not val: return None
    try:
        if isinstance(val, str):
            m = re.search(r'^-?\d+\.?\d*', val)
            if m: return float(m.group())
        return float(val)
    except:
        return None

reader = csv.DictReader(StringIO(csv_data.strip()))

for row in reader:
    name = row['name'].strip()
    
    # Process numeric fields
    payload = {
        'category': row['category'],
        'subcategory': row['subcategory'],
        'name': name,
        'description': row['description'],
        'composition': row['composition'],
        'source_url': row['source_url'].split(' | ')[0].strip(), # Use primary URL
        'source_name': "Verified Source",
        'is_verified': True
    }
    
    for f in ['density', 'tensile_strength_min', 'yield_strength_min', 'elastic_modulus', 'thermal_conductivity', 'specific_heat', 'melting_point_min', 'elongation']:
        if row.get(f):
            sanitized = sanitize_float(row[f])
            if sanitized is not None:
                payload[f] = sanitized
                
    if row.get('hardness'): payload['hardness'] = row['hardness']
    
    # Check if exists
    res = supabase.table('materials').select('id').eq('name', name).execute()
    if res.data:
        # Update
        tid = res.data[0]['id']
        supabase.table('materials').update(payload).eq('id', tid).execute()
        print(f"Updated existing: {name}")
    else:
        # Insert
        supabase.table('materials').insert(payload).execute()
        print(f"Inserted new: {name}")

print("Batch 1 processing complete.")
