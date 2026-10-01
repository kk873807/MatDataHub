import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

batch_8 = [
    {
        'name': 'Depleted Uranium (DU)', 'category': 'Uranium', 'subcategory': 'Depleted Uranium',
        'density': 19.05, 'tensile_strength_min': 462, 'yield_strength_min': 200, 'elongation': 8, 'elastic_modulus': 208, 'melting_point_min': 1132,
        'composition': 'Uranium (Depleted in U-235)',
        'description': 'Unalloyed DU metal. High density material used in penetrators, counterweights, and shielding. Tensile range 462-703 MPa depending on rolling/heat-treat.',
        'source_url': 'https://www.osti.gov/servlets/purl/6087232', 'source_name': 'OSTI/DOE', 'is_verified': True
    },
    {
        'name': 'Natural Uranium Metal', 'category': 'Uranium', 'subcategory': 'Natural Uranium',
        'density': 19.05, 'tensile_strength_min': 460, 'elastic_modulus': 208, 'thermal_conductivity': 27.5, 'hardness': '200 HV', 'melting_point_min': 1132,
        'composition': 'Uranium (0.711% U-235)',
        'description': 'Malleable, ductile, highly dense heavy metal. Poor electrical conductor. Hardness ~1960-2500 MPa (Vickers).',
        'source_url': 'https://periodic.lanl.gov/92.shtml', 'source_name': 'LANL / Wikipedia (CRC)', 'is_verified': True
    },
    {
        'name': 'Enriched Uranium (LEU, 3-5% U-235)', 'category': 'Uranium', 'subcategory': 'Enriched Uranium',
        'density': 19.05, 'tensile_strength_min': 460, 'elastic_modulus': 208, 'thermal_conductivity': 27.5, 'hardness': '200 HV', 'melting_point_min': 1132,
        'composition': 'Uranium (3-5% U-235)',
        'description': 'Low-Enriched Uranium (LEU) reactor fuel grade. Isotopic enrichment does not significantly alter bulk mechanical/thermal properties from natural U.',
        'source_url': 'https://www.energy.gov/ne/nuclear-fuel-facts-uranium', 'source_name': 'U.S. DOE / World Nuclear Association', 'is_verified': True
    },
    {
        'name': 'Uranium-0.75Ti (U-0.75Ti) Alloy', 'category': 'Uranium', 'subcategory': 'Uranium-Titanium Alloy',
        'density': 18.6, 'tensile_strength_min': 1380, 'yield_strength_min': 850, 'elongation': 2,
        'composition': 'U 99.25%, Ti 0.75%',
        'description': 'Staballoy. High-strength ductile DU alloy. Peak-aged values show extreme strength (yield ~850-1380 MPa).',
        'source_url': 'https://patents.google.com/patent/US5273711A/en', 'source_name': 'Google Patents / LANL', 'is_verified': True
    },
    {
        'name': 'Uranium-6Nb (U-6Nb, Mulberry) Alloy', 'category': 'Uranium', 'subcategory': 'Uranium-Niobium Alloy',
        'density': 17.5,
        'composition': 'U 94%, Nb 6%',
        'description': 'Mulberry alloy. Known for excellent corrosion resistance due to a passivating oxide layer.',
        'source_url': 'https://www.mdpi.com/2076-3417/11/12/5643', 'source_name': 'MDPI Applied Sciences / LLNL', 'is_verified': True
    },
    {
        'name': 'Uranium-2Mo (U-2Mo) Alloy', 'category': 'Uranium', 'subcategory': 'Uranium-Molybdenum Alloy',
        'density': 18.4,
        'composition': 'U 98%, Mo 2%',
        'description': 'Uranium alloyed with 2 wt% Molybdenum. Commonly cast for radioactive shipping-cask shielding applications.',
        'source_url': 'https://digital.library.unt.edu/ark:/67531/metadc1113266/', 'source_name': 'DOE / UNT Digital Library', 'is_verified': True
    },
    {
        'name': 'Uranium-10Mo (U-10Mo) Alloy', 'category': 'Uranium', 'subcategory': 'Uranium-Molybdenum Alloy',
        'density': 17.13,
        'composition': 'U 90%, Mo 10%',
        'description': 'Uranium-10wt% Molybdenum. Standardized high-performance research reactor (HPRR) fuel alloy.',
        'source_url': 'https://publications.anl.gov/anlpubs/2020/07/160836.pdf', 'source_name': 'ANL / OSTI', 'is_verified': True
    },
    {
        'name': 'Uranium-Zirconium (U-Zr) Alloy', 'category': 'Uranium', 'subcategory': 'Uranium-Zirconium Alloy',
        'composition': 'Uranium-Zirconium (binary alloy, variable Zr wt%)',
        'description': 'Metallic nuclear fuel alloy. Properties (density, thermal conductivity) scale strongly with Zr wt%. Evaluated extensively for EBR-II.',
        'source_url': 'https://www.osti.gov/servlets/purl/1482119', 'source_name': 'OSTI / INL', 'is_verified': True
    },
    {
        'name': 'Uranium-Plutonium-Zirconium (U-Pu-Zr) Fuel', 'category': 'Uranium', 'subcategory': 'Nuclear Fuel Alloy',
        'composition': 'U-Pu-Zr (ternary metallic fuel)',
        'description': 'Metallic fast reactor fuel. Extensively modeled for thermal conductivity and specific heat by ANL SAS4A/SASSYS-1 codes.',
        'source_url': 'https://sas-doc.nse.anl.gov/latest/Part03/Ch10/metal-fuel-properties.html', 'source_name': 'Argonne National Laboratory', 'is_verified': True
    }
]

print("=== Processing Uranium Batch ===")
for m in batch_8:
    name = m['name']
    r = supabase.table('materials').select('id').eq('name', name).execute()
    if r.data:
        supabase.table('materials').update(m).eq('id', r.data[0]['id']).execute()
        print(f"Updated: {name}")
    else:
        supabase.table('materials').insert(m).execute()
        print(f"Inserted: {name}")

print("\nUranium batch complete!")
