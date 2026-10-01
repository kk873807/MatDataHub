import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

updates = [
    {
        'name': 'Gold Bonding Wire (99.99% Au)',
        'data': {
            'density': 19.3, 'melting_point_min': 1064.4, 'thermal_conductivity': 318,
            'tensile_strength_min': 130, 'yield_strength_min': 205, 'elastic_modulus': 78.5,
            'hardness': '20-60 HV', 
            'source_url': 'https://www.goodfellow.com/gold-wire',
            'source_name': 'Goodfellow / Inseto',
            'description': '99.99% purity bonding wire. Tensile properties vary significantly between soft (annealed) and hard states. Electrical resistivity 2.20 µΩ·cm.'
        }
    },
    {
        'name': '10K Gold Alloy (41.7% Au)',
        'data': {
            'density': 11.42, 'hardness': '133 HV', 'melting_point_min': 945, # 1733 F -> 945 C
            'composition': 'Au 41.7%, Cu, Ag, Zn (Standard Yellow Alloy 231)',
            'source_url': 'https://www.unitedpmr.com/wp-content/uploads/2021/07/231.pdf',
            'source_name': 'United Precious Metal Refining',
            'description': '10K standard yellow gold casting alloy. As-cast Vickers hardness 133. Density varies slightly depending on exact color tint formulation.'
        }
    },
    {
        'name': 'Dental Gold Alloy Type III',
        'data': {
            'source_url': 'https://medicaljournalssweden.se/actaodontologica/article/download/38078/43236/95886',
            'source_name': 'Acta Odontologica Scandinavica (NIOM)',
            'description': 'ADA Specification No. 5 Type 3. Medium-hard dental casting alloy for crowns, bridges, and inlays. Primary properties derived from independent peer-reviewed NIOM measurements.'
        }
    },
    {
        'name': 'Gold-Copper Alloy (Au-Cu)',
        'data': {
            'density': 18.0, 'tensile_strength_min': 450, 'elongation': 4.3, 'melting_point_min': 930, 'elastic_modulus': 100,
            'composition': 'Au 89-91%, Cu 9-11%',
            'source_url': 'https://store.astm.org/b0596-89r17.html',
            'source_name': 'ASTM B596-21',
            'description': 'Official ASTM B596 electrical contact material. Specifies UTS/elongation/hardness as temper criteria. Used for high-reliability slip rings and precision connectors.'
        }
    }
]

print("=== Applying Fixes for Flagged Gold Items ===")
for u in updates:
    res = supabase.table('materials').select('id').eq('name', u['name']).execute()
    if res.data:
        supabase.table('materials').update(u['data']).eq('id', res.data[0]['id']).execute()
        print(f"Updated: {u['name']} with {len(u['data'])} refined fields")
    else:
        print(f"NOT FOUND: {u['name']}")

print("\nGold fixes applied successfully!")
