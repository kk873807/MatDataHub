import os, json
from supabase import create_client
from dotenv import load_dotenv
load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

names = [
    'ACI-ASTM CA15M (J91151) Cast Stainless Steel',
    'UNS S82122 Stainless Steel',
    'AISI 304 (S30400) Stainless Steel'
]
fields = 'name, density, yield_strength_min, yield_strength_max, tensile_strength_min, tensile_strength_max, elastic_modulus, thermal_conductivity, elongation, fatigue_strength, poissons_ratio, shear_modulus, melting_point_min, melting_point_max, max_service_temp, specific_heat, embodied_carbon, hardness, composition, thermal_expansion_coefficient'

for name in names:
    res = supabase.table('materials').select(fields).eq('name', name).execute()
    if res.data:
        d = res.data[0]
        print("--- " + d["name"] + " ---")
        for k, v in d.items():
            if k != 'name' and v is not None:
                print("  " + k + ": " + str(v)[:100])
        print()
