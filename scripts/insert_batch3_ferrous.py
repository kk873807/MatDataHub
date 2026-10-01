import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

batch_3 = [
    {
        'category': 'Tool Steel', 'subcategory': 'Cold Work Tool Steel', 'name': 'A2 Tool Steel',
        'density': 7.86, 'tensile_strength_min': 760, 'yield_strength_min': 460, 'elongation': 12, 'hardness': '60 HRC', 'elastic_modulus': 200, 'thermal_conductivity': 26, 'specific_heat': 460, 'melting_point_min': 1420,
        'source_url': 'https://www.matweb.com/search/datasheet.aspx?matguid=1becaffb06b746a8b31690bbf1f53426', 'source_name': 'MatWeb / TheWorldMaterial', 'is_verified': True,
        'description': 'Air-hardening cold work tool steel. Good toughness and excellent dimensional stability.'
    },
    {
        'category': 'Tool Steel', 'subcategory': 'Hot Work Tool Steel', 'name': 'H13 Tool Steel',
        'density': 7.80, 'tensile_strength_min': 1200, 'yield_strength_min': 1000, 'elongation': 9, 'hardness': '50 HRC', 'elastic_modulus': 210, 'thermal_conductivity': 24.3, 'specific_heat': 460, 'melting_point_min': 1427,
        'source_url': 'https://www.onlinemetals.com/en/product-guide/alloy/H13', 'source_name': 'OnlineMetals', 'is_verified': True,
        'description': 'Chromium-molybdenum hot work tool steel. Excellent high-temperature toughness and thermal fatigue resistance.'
    },
    {
        'category': 'Tool Steel', 'subcategory': 'High Speed Steel', 'name': 'M2 Tool Steel',
        'density': 8.16, 'tensile_strength_min': 1000, 'hardness': '65 HRC', 'elastic_modulus': 207, 'thermal_conductivity': 41.5, 'specific_heat': 460, 'melting_point_min': 1427,
        'source_url': 'https://www.azom.com/article.aspx?ArticleID=6167', 'source_name': 'AZoM (Replaced MakeItFrom)', 'is_verified': True,
        'description': 'Tungsten-molybdenum high-speed steel. Widely used for cutting tools. Yield strength not defined for fully hardened HSS.'
    },
    {
        'category': 'Cast Iron', 'subcategory': 'Gray Iron', 'name': 'Gray Iron Class 20',
        'density': 7.15, 'tensile_strength_min': 138, 'hardness': '156 HB', 'elastic_modulus': 100, 'thermal_conductivity': 46, 'specific_heat': 544, 'melting_point_min': 1150,
        'source_url': 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=c4571dc3bc8447d48dc7b9ecf86e3f01', 'source_name': 'MatWeb (Replaced MakeItFrom)', 'is_verified': True,
        'description': 'ASTM A48 Class 20. Low-strength gray cast iron with excellent machinability and damping capacity.'
    },
    {
        'category': 'Cast Iron', 'subcategory': 'Gray Iron', 'name': 'Gray Iron Class 30',
        'density': 7.15, 'tensile_strength_min': 207, 'hardness': '187 HB', 'elastic_modulus': 110, 'thermal_conductivity': 46, 'specific_heat': 544, 'melting_point_min': 1150,
        'source_url': 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=eec3193e8aeb4b3e8957baab1c1b18c5', 'source_name': 'MatWeb (Replaced MakeItFrom)', 'is_verified': True,
        'description': 'ASTM A48 Class 30. General purpose gray cast iron.'
    },
    {
        'category': 'Cast Iron', 'subcategory': 'Gray Iron', 'name': 'Gray Iron Class 40',
        'density': 7.15, 'tensile_strength_min': 276, 'hardness': '235 HB', 'elastic_modulus': 117, 'thermal_conductivity': 46, 'specific_heat': 544, 'melting_point_min': 1150,
        'source_url': 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=274b7700201d4fc6a9787edeb1b4b7c6', 'source_name': 'MatWeb (Replaced MakeItFrom)', 'is_verified': True,
        'description': 'ASTM A48 Class 40. High-strength gray cast iron, pearlite matrix.'
    },
    {
        'category': 'Cast Iron', 'subcategory': 'Gray Iron', 'name': 'Gray Iron Class 50',
        'density': 7.15, 'tensile_strength_min': 345, 'hardness': '262 HB', 'elastic_modulus': 124, 'thermal_conductivity': 46, 'specific_heat': 544, 'melting_point_min': 1150,
        'source_url': 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=2dafcba8842045e2a3c94295325cd6fc', 'source_name': 'MatWeb (Replaced MakeItFrom)', 'is_verified': True,
        'description': 'ASTM A48 Class 50. High-strength gray cast iron with alloy additions.'
    },
    {
        'category': 'Cast Iron', 'subcategory': 'Gray Iron', 'name': 'Gray Iron Class 60',
        'density': 7.15, 'tensile_strength_min': 414, 'hardness': '302 HB', 'elastic_modulus': 131, 'thermal_conductivity': 46, 'specific_heat': 544, 'melting_point_min': 1150,
        'source_url': 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=95db59c1c5e4407abff6cc262a67e42d', 'source_name': 'MatWeb (Replaced MakeItFrom)', 'is_verified': True,
        'description': 'ASTM A48 Class 60. Very high-strength gray cast iron.'
    },
    {
        'category': 'Cast Iron', 'subcategory': 'Ductile Iron', 'name': 'Ductile Iron 60-40-18',
        'density': 7.10, 'tensile_strength_min': 414, 'yield_strength_min': 276, 'elongation': 18, 'hardness': '160 HB', 'elastic_modulus': 165, 'thermal_conductivity': 36, 'specific_heat': 515, 'melting_point_min': 1150,
        'source_url': 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=c2bfdcdddc104b28b7e2832eeedc3ad2', 'source_name': 'MatWeb (Replaced MakeItFrom)', 'is_verified': True,
        'description': 'ASTM A536 Grade 60-40-18. Fully ferritic matrix, maximum ductility and impact resistance.'
    },
    {
        'category': 'Cast Iron', 'subcategory': 'Ductile Iron', 'name': 'Ductile Iron 100-70-03',
        'density': 7.10, 'tensile_strength_min': 689, 'yield_strength_min': 483, 'elongation': 3, 'hardness': '270 HB', 'elastic_modulus': 165, 'thermal_conductivity': 36, 'specific_heat': 515, 'melting_point_min': 1150,
        'source_url': 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=46a3a4c0eb3c42bebd7916bf280540cf', 'source_name': 'MatWeb (Replaced MakeItFrom)', 'is_verified': True,
        'description': 'ASTM A536 Grade 100-70-03. Pearlitic matrix, high strength and wear resistance.'
    },
    {
        'category': 'Cast Iron', 'subcategory': 'Austempered Ductile Iron', 'name': 'Austempered Ductile Iron (ADI)',
        'density': 7.10, 'tensile_strength_min': 900, 'yield_strength_min': 650, 'elongation': 9, 'hardness': '300 HB', 'elastic_modulus': 160, 'thermal_conductivity': 33, 'specific_heat': 515, 'melting_point_min': 1150,
        'source_url': 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=82bcfcd729db4af5be557551065ec090', 'source_name': 'MatWeb (Replaced MakeItFrom)', 'is_verified': True,
        'description': 'ASTM A897 Grade 1 (900/650/09). Heat treated ductile iron with superior strength-to-weight ratio.'
    },
    {
        'category': 'Cast Iron', 'subcategory': 'Malleable Iron', 'name': 'Malleable Iron',
        'density': 7.25, 'tensile_strength_min': 414, 'yield_strength_min': 310, 'elongation': 4, 'hardness': '163 HB', 'elastic_modulus': 170, 'thermal_conductivity': 45, 'specific_heat': 530, 'melting_point_min': 1220,
        'source_url': 'https://www.matweb.com/search/DataSheet.aspx?MatGUID=2f6fbf8c51cd476c8cb81a2818c3de75', 'source_name': 'MatWeb (Replaced MakeItFrom)', 'is_verified': True,
        'description': 'ASTM A602 Grade M4504. Pearlitic malleable iron.'
    },
    {
        'category': 'Cast Iron', 'subcategory': 'CGI', 'name': 'Compacted Graphite Iron (CGI)',
        'density': 7.10, 'tensile_strength_min': 400, 'yield_strength_min': 280, 'elongation': 1.5, 'hardness': '220 HB', 'elastic_modulus': 145, 'thermal_conductivity': 36, 'specific_heat': 515, 'melting_point_min': 1150,
        'source_url': 'https://www.sintercast.com/media/1239/compacted-graphite-iron-material-data-sheet.pdf', 'source_name': 'SinterCast PDF', 'is_verified': True,
        'description': 'Used for highly stressed engine blocks. Combines properties between gray and ductile iron.'
    },
    {
        'category': 'Cast Iron', 'subcategory': 'White Iron', 'name': 'Ni-Hard Cast Iron',
        'density': 7.60, 'tensile_strength_min': 400, 'hardness': '600 HB', 'elastic_modulus': 190, 'thermal_conductivity': 30, 'specific_heat': 500, 'melting_point_min': 1150,
        'source_url': 'https://wilfley.com/lit/materials/nihard-4-hard-iron.pdf', 'source_name': 'Wilfley NiHard 4 (Replaced MatMatch)', 'is_verified': True,
        'description': 'Ni-Hard 4. Abrasion-resistant white cast iron. Yield point is typically absent due to extreme hardness/brittleness.'
    },
    {
        'category': 'Cast Iron', 'subcategory': 'Austenitic Cast Iron', 'name': 'Ni-Resist Cast Iron',
        'density': 7.30, 'tensile_strength_min': 172, 'yield_strength_min': 103, 'elongation': 2, 'hardness': '131 HB', 'elastic_modulus': 100, 'thermal_conductivity': 40, 'specific_heat': 500, 'melting_point_min': 1230,
        'source_url': 'https://www.matweb.com/search/datasheet.aspx?matguid=c0277bd24b894101859dd6c32daec0eb', 'source_name': 'MatWeb (Replaced MakeItFrom)', 'is_verified': True,
        'description': 'ASTM A436 Type 1. Austenitic cast iron (Ni-Resist), high corrosion and heat resistance.'
    }
]

print("Processing Batch 3...")
for m in batch_3:
    res = supabase.table('materials').select('id').eq('name', m['name']).execute()
    if res.data:
        supabase.table('materials').update(m).eq('id', res.data[0]['id']).execute()
        print(f"Updated {m['name']}")
    else:
        supabase.table('materials').insert(m).execute()
        print(f"Inserted {m['name']}")
        
print("Batch 3 complete!")
