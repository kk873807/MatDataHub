import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

batch_4 = [
    # ALUMINUM
    {
        'category': 'Aluminum', 'subcategory': 'Pure Aluminum', 'name': 'Aluminum 1199 Alloy',
        'density': 2.70, 'tensile_strength_min': 45, 'yield_strength_min': 15, 'elongation': 45, 'hardness': '15 HB', 'elastic_modulus': 70, 'thermal_conductivity': 236, 'specific_heat': 900, 'melting_point_min': 657,
        'source_url': 'https://www.matweb.com/search/DataSheet.aspx?bassnum=MA1199O', 'source_name': 'MatWeb', 'is_verified': True,
        'description': 'Ultra-high purity aluminum (99.99%+ Al). Excellent corrosion resistance and electrical/thermal conductivity. Typical values for O (annealed) temper.'
    },
    {
        'category': 'Aluminum', 'subcategory': 'Aluminum-Copper', 'name': 'Aluminum 2014 Alloy',
        'density': 2.80, 'tensile_strength_min': 483, 'yield_strength_min': 414, 'elongation': 13, 'hardness': '135 HB', 'elastic_modulus': 72, 'thermal_conductivity': 155, 'specific_heat': 875, 'melting_point_min': 507,
        'source_url': 'https://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MA2014T6', 'source_name': 'ASM Material Data Sheet', 'is_verified': True,
        'description': 'High-strength aerospace alloy (Al-Cu). Values shown are for T6 temper. Very susceptible to corrosion compared to other aluminum grades.'
    },
    {
        'category': 'Aluminum', 'subcategory': 'Cast Aluminum', 'name': 'Aluminum 319.0 Cast Alloy',
        'density': 2.79, 'tensile_strength_min': 234, 'yield_strength_min': 124, 'elongation': 2, 'hardness': '70 HB', 'elastic_modulus': 74, 'thermal_conductivity': 109, 'specific_heat': 963, 'melting_point_min': 515,
        'source_url': 'https://www.matweb.com/search/datasheettext.aspx?matid=9863', 'source_name': 'MatWeb', 'is_verified': True,
        'description': 'Al-Si-Cu general purpose casting alloy. Values for sand cast T6 condition.'
    },
    {
        'category': 'Aluminum', 'subcategory': 'Cast Aluminum', 'name': 'Aluminum 380.0 Cast Alloy',
        'density': 2.71, 'tensile_strength_min': 317, 'yield_strength_min': 159, 'elongation': 3.5, 'hardness': '80 HB', 'elastic_modulus': 71, 'thermal_conductivity': 96, 'specific_heat': 963, 'melting_point_min': 540,
        'source_url': 'https://www.matweb.com/search/datasheet.aspx?matguid=568dd76f95094ab2ad63726be36ce1dd', 'source_name': 'MatWeb', 'is_verified': True,
        'description': 'Most commonly used aluminum die casting alloy (Al-Si-Cu). Good balance of properties and castability. Values for as-die-cast (F).'
    },
    {
        'category': 'Aluminum', 'subcategory': 'Cast Aluminum', 'name': 'Aluminum 390.0 Cast Alloy',
        'density': 2.73, 'tensile_strength_min': 275, 'yield_strength_min': 240, 'elongation': 1, 'hardness': '120 HB', 'elastic_modulus': 81, 'thermal_conductivity': 134, 'specific_heat': 963, 'melting_point_min': 505,
        'source_url': 'https://www.matweb.com/search/datasheet.aspx?matguid=749e09f1cc2b45fc98213c6ca968f72c', 'source_name': 'MatWeb', 'is_verified': True,
        'description': 'Hypereutectic Al-Si casting alloy with excellent wear resistance. Values for T5 sand cast.'
    },

    # COPPER
    {
        'category': 'Copper', 'subcategory': 'Pure Copper', 'name': 'Phosphorus-Deoxidized (DHP) Copper (UNS C12200)',
        'density': 8.94, 'tensile_strength_min': 220, 'yield_strength_min': 70, 'elongation': 40, 'hardness': '50 HRF', 'elastic_modulus': 117, 'thermal_conductivity': 339, 'specific_heat': 385, 'melting_point_min': 1083,
        'source_url': 'https://alloys.copper.org/alloy/C12200', 'source_name': 'Copper.org (CDA)', 'is_verified': True,
        'description': 'Phosphorus-deoxidized, high residual phosphorus. Commonly used for plumbing and HVAC tubing.'
    },
    {
        'category': 'Copper', 'subcategory': 'Free-Machining Copper', 'name': 'Tellurium Copper (UNS C14500)',
        'density': 8.94, 'tensile_strength_min': 220, 'yield_strength_min': 70, 'elongation': 40, 'hardness': '45 HRB', 'elastic_modulus': 117, 'thermal_conductivity': 355, 'specific_heat': 385, 'melting_point_min': 1075,
        'source_url': 'https://alloys.copper.org/alloy/C14500', 'source_name': 'Copper.org (CDA)', 'is_verified': True,
        'description': 'Free-machining pure copper containing tellurium. High conductivity with vastly improved machinability.'
    },
    {
        'category': 'Copper', 'subcategory': 'Beryllium Copper', 'name': 'Beryllium Copper (UNS C17200)',
        'density': 8.25, 'tensile_strength_min': 1170, 'yield_strength_min': 1030, 'elongation': 3, 'hardness': '38 HRC', 'elastic_modulus': 125, 'thermal_conductivity': 105, 'specific_heat': 420, 'melting_point_min': 865,
        'source_url': 'https://alloys.copper.org/alloy/C17200', 'source_name': 'Copper.org (CDA)', 'is_verified': True,
        'description': 'High-strength copper alloy used for springs, load cells, and non-sparking tools. Values for TH04 temper.'
    },
    {
        'category': 'Copper', 'subcategory': 'Brass', 'name': 'Muntz Metal (60/40 Brass) (UNS C28000)',
        'density': 8.39, 'tensile_strength_min': 372, 'yield_strength_min': 145, 'elongation': 50, 'hardness': '55 HRB', 'elastic_modulus': 105, 'thermal_conductivity': 123, 'specific_heat': 377, 'melting_point_min': 900,
        'source_url': 'https://alloys.copper.org/alloy/C28000', 'source_name': 'Copper.org (CDA)', 'is_verified': True,
        'description': '60% Cu / 40% Zn. High strength structural brass, commonly used for architectural applications.'
    },
    {
        'category': 'Copper', 'subcategory': 'Brass', 'name': 'Naval Brass (UNS C46400)',
        'density': 8.41, 'tensile_strength_min': 380, 'yield_strength_min': 170, 'elongation': 45, 'hardness': '55 HRB', 'elastic_modulus': 103, 'thermal_conductivity': 116, 'specific_heat': 377, 'melting_point_min': 888,
        'source_url': 'https://alloys.copper.org/alloy/C46400', 'source_name': 'Copper.org (CDA)', 'is_verified': True,
        'description': 'Muntz metal with ~1% Tin added for marine corrosion resistance.'
    },
    {
        'category': 'Copper', 'subcategory': 'Bronze', 'name': 'Nickel Aluminum Bronze (UNS C63000)',
        'density': 7.58, 'tensile_strength_min': 760, 'yield_strength_min': 470, 'elongation': 15, 'hardness': '210 HB', 'elastic_modulus': 117, 'thermal_conductivity': 38, 'specific_heat': 377, 'melting_point_min': 1040,
        'source_url': 'https://www.azom.com/article.aspx?ArticleID=8922', 'source_name': 'AZoM (Verified Source)', 'is_verified': True,
        'description': 'Very high strength and excellent marine/abrasion corrosion resistance.'
    },
    {
        'category': 'Copper', 'subcategory': 'Bronze', 'name': 'High Silicon Bronze (UNS C65500)',
        'density': 8.53, 'tensile_strength_min': 395, 'yield_strength_min': 125, 'elongation': 50, 'hardness': '60 HRB', 'elastic_modulus': 105, 'thermal_conductivity': 36, 'specific_heat': 377, 'melting_point_min': 970,
        'source_url': 'https://alloys.copper.org/alloy/C65500', 'source_name': 'Copper.org (CDA)', 'is_verified': True,
        'description': 'High strength, excellent weldability, commonly used in marine hardware and artistic casting.'
    },
    {
        'category': 'Copper', 'subcategory': 'Cupronickel', 'name': 'Copper-Nickel 90/10 (UNS C70600)',
        'density': 8.94, 'tensile_strength_min': 275, 'yield_strength_min': 105, 'elongation': 40, 'hardness': '50 HRB', 'elastic_modulus': 135, 'thermal_conductivity': 40, 'specific_heat': 377, 'melting_point_min': 1100,
        'source_url': 'https://www.azom.com/article.aspx?ArticleID=6297', 'source_name': 'AZoM (Verified Source)', 'is_verified': True,
        'description': '90% Cu / 10% Ni. Outstanding resistance to seawater corrosion and biofouling.'
    },
    {
        'category': 'Copper', 'subcategory': 'Cupronickel', 'name': 'Copper-Nickel 70/30 (UNS C71500)',
        'density': 8.94, 'tensile_strength_min': 370, 'yield_strength_min': 125, 'elongation': 40, 'hardness': '60 HRB', 'elastic_modulus': 152, 'thermal_conductivity': 29, 'specific_heat': 377, 'melting_point_min': 1170,
        'source_url': 'https://www.azom.com/article.aspx?ArticleID=6298', 'source_name': 'AZoM (Verified Source)', 'is_verified': True,
        'description': '70% Cu / 30% Ni. Higher strength and even better seawater resistance than 90/10.'
    },
    {
        'category': 'Copper', 'subcategory': 'Nickel Silver', 'name': 'Nickel Silver 65-18 (UNS C75200)',
        'density': 8.73, 'tensile_strength_min': 385, 'yield_strength_min': 125, 'elongation': 40, 'hardness': '50 HRB', 'elastic_modulus': 125, 'thermal_conductivity': 33, 'specific_heat': 377, 'melting_point_min': 1110,
        'source_url': 'https://alloys.copper.org/alloy/C75200', 'source_name': 'Copper.org (CDA)', 'is_verified': True,
        'description': 'Contains no actual silver. 65% Cu, 18% Ni, 17% Zn. Bright silvery appearance, high corrosion resistance.'
    },

    # ZINC
    {
        'category': 'Zinc', 'subcategory': 'Zinc Die Cast Alloy', 'name': 'Zamak 3',
        'density': 6.60, 'tensile_strength_min': 283, 'yield_strength_min': 221, 'elongation': 10, 'hardness': '82 HB', 'elastic_modulus': 85, 'thermal_conductivity': 113, 'specific_heat': 419, 'melting_point_min': 381,
        'source_url': 'https://eazall.com/zamak-3', 'source_name': 'Eastern Alloys', 'is_verified': True,
        'description': 'Standard zinc die-casting alloy. Excellent balance of physical and mechanical properties.'
    },
    {
        'category': 'Zinc', 'subcategory': 'Zinc Die Cast Alloy', 'name': 'Zamak 5',
        'density': 6.60, 'tensile_strength_min': 331, 'yield_strength_min': 228, 'elongation': 7, 'hardness': '91 HB', 'elastic_modulus': 85, 'thermal_conductivity': 109, 'specific_heat': 419, 'melting_point_min': 380,
        'source_url': 'https://eazall.com/zamak-5', 'source_name': 'Eastern Alloys', 'is_verified': True,
        'description': 'Similar to Zamak 3 but with 1% copper added for increased strength, hardness, and creep resistance.'
    },
    {
        'category': 'Zinc', 'subcategory': 'Zinc Die Cast Alloy', 'name': 'Zamak 2',
        'density': 6.60, 'tensile_strength_min': 359, 'yield_strength_min': 250, 'elongation': 7, 'hardness': '100 HB', 'elastic_modulus': 85, 'thermal_conductivity': 105, 'specific_heat': 419, 'melting_point_min': 379,
        'source_url': 'https://eazall.com/zamak-2', 'source_name': 'Eastern Alloys', 'is_verified': True,
        'description': 'Highest strength and hardness of the Zamak alloys (3% Cu). Retains strength well after aging.'
    },
    {
        'category': 'Zinc', 'subcategory': 'Zinc Die Cast Alloy', 'name': 'Zamak 7',
        'density': 6.60, 'tensile_strength_min': 283, 'yield_strength_min': 221, 'elongation': 13, 'hardness': '82 HB', 'elastic_modulus': 85, 'thermal_conductivity': 113, 'specific_heat': 419, 'melting_point_min': 381,
        'source_url': 'https://eazall.com/zamak-7', 'source_name': 'Eastern Alloys', 'is_verified': True,
        'description': 'High-purity variant of Zamak 3 with slightly lower magnesium content for higher fluidity and ductility.'
    },
    {
        'category': 'Zinc', 'subcategory': 'Zinc-Aluminum Alloy', 'name': 'ZA-8',
        'density': 6.30, 'tensile_strength_min': 374, 'yield_strength_min': 290, 'elongation': 8, 'hardness': '103 HB', 'elastic_modulus': 85, 'thermal_conductivity': 115, 'specific_heat': 419, 'melting_point_min': 375,
        'source_url': 'https://eazall.com/za8', 'source_name': 'Eastern Alloys', 'is_verified': True,
        'description': '8% aluminum. Ideal for hot-chamber die casting. High strength, creep resistant.'
    },
    {
        'category': 'Zinc', 'subcategory': 'Zinc-Aluminum Alloy', 'name': 'ZA-12',
        'density': 6.03, 'tensile_strength_min': 404, 'yield_strength_min': 317, 'elongation': 5, 'hardness': '105 HB', 'elastic_modulus': 85, 'thermal_conductivity': 116, 'specific_heat': 419, 'melting_point_min': 377,
        'source_url': 'https://eazall.com/za12', 'source_name': 'Eastern Alloys', 'is_verified': True,
        'description': '11% aluminum. Best balance of strength, castability, and bearing properties.'
    },
    {
        'category': 'Zinc', 'subcategory': 'Zinc-Aluminum Alloy', 'name': 'ZA-27',
        'density': 5.00, 'tensile_strength_min': 426, 'yield_strength_min': 371, 'elongation': 2, 'hardness': '118 HB', 'elastic_modulus': 78, 'thermal_conductivity': 125, 'specific_heat': 419, 'melting_point_min': 375,
        'source_url': 'https://eazall.com/za27', 'source_name': 'Eastern Alloys', 'is_verified': True,
        'description': '27% aluminum. Highest strength, highest melting point, and lowest density of the ZA alloys.'
    },

    # LEAD
    {
        'category': 'Lead', 'subcategory': 'Pure Lead', 'name': 'Chemical Lead (Pure Lead)',
        'density': 11.34, 'tensile_strength_min': 16, 'yield_strength_min': 8, 'elongation': 50, 'hardness': '4 HB', 'elastic_modulus': 14, 'thermal_conductivity': 35, 'specific_heat': 130, 'melting_point_min': 327,
        'source_url': 'https://store.astm.org/b0029-19.html', 'source_name': 'ASTM B29', 'is_verified': True,
        'description': 'Refined Lead/Chemical-Copper Lead per ASTM B29. Extremely malleable, extremely dense, high corrosion resistance.'
    },
    {
        'category': 'Lead', 'subcategory': 'Antimonial Lead', 'name': 'Antimonial Lead (4% Sb)',
        'density': 11.04, 'tensile_strength_min': 28, 'yield_strength_min': 14, 'elongation': 30, 'hardness': '8 HB', 'elastic_modulus': 14, 'thermal_conductivity': 29, 'specific_heat': 130, 'melting_point_min': 299,
        'source_url': 'https://www.goodfellow.com/usa/antimonial-lead-alloy-foil-pb96-sb4-group', 'source_name': 'Goodfellow', 'is_verified': True,
        'description': 'Lead alloyed with 4% Antimony (Hard Lead) for significantly increased strength and hardness.'
    },
    {
        'category': 'Lead', 'subcategory': 'Antimonial Lead', 'name': 'Antimonial Lead (6% Sb)',
        'density': 10.88, 'tensile_strength_min': 45, 'yield_strength_min': 20, 'elongation': 20, 'hardness': '11 HB', 'elastic_modulus': 14, 'thermal_conductivity': 24, 'specific_heat': 130, 'melting_point_min': 291,
        'source_url': 'https://www.belmontmetals.com/product/6-antimonial-lead/', 'source_name': 'Belmont Metals', 'is_verified': True,
        'description': '6% Antimonial Lead. Common in battery grids, bullet casting, and radiation shielding.'
    },
    {
        'category': 'Lead', 'subcategory': 'Babbitt Metal', 'name': 'Lead Babbitt (ASTM B23 Grade 7)',
        'density': 10.40, 'tensile_strength_min': 35, 'yield_strength_min': 22, 'elongation': 1, 'hardness': '15 HB', 'elastic_modulus': 20, 'thermal_conductivity': 25, 'specific_heat': 130, 'melting_point_min': 240,
        'source_url': 'https://www.kappalloy.com/babbitt-alloy/lead-babbitt-alloys/durakapp-7/', 'source_name': 'Kapp Alloy (DuraKapp #7)', 'is_verified': True,
        'description': 'Heavy-duty lead-based bearing alloy. Contains ~75% Pb, 15% Sb, 10% Sn.'
    },
    {
        'category': 'Lead', 'subcategory': 'Lead-Calcium Alloy', 'name': 'Lead-Calcium-Tin Alloy',
        'density': 11.30, 'tensile_strength_min': 34, 'yield_strength_min': 25, 'elongation': 30, 'hardness': '9 HB', 'elastic_modulus': 14, 'thermal_conductivity': 33, 'specific_heat': 130, 'melting_point_min': 327,
        'source_url': 'https://www.matweb.com/search/datasheet.aspx?MatGUID=cc3ce46e955e4a68a00bbb041d44e38f', 'source_name': 'MatWeb', 'is_verified': True,
        'description': 'Modern battery grid alloy (UNS L50740). Replaces antimonial lead for maintenance-free SLA batteries.'
    }
]

print("Processing Batch 4...")
for m in batch_4:
    res = supabase.table('materials').select('id').eq('name', m['name']).execute()
    if res.data:
        supabase.table('materials').update(m).eq('id', res.data[0]['id']).execute()
        print(f"Updated {m['name']}")
    else:
        supabase.table('materials').insert(m).execute()
        print(f"Inserted {m['name']}")
        
print("Batch 4 complete!")
