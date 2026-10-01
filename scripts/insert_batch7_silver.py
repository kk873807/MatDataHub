import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

batch_7 = [
    {
        'name': 'Pure Silver (99.99% Ag, Fine Silver)', 'category': 'Silver', 'subcategory': 'Pure Silver',
        'density': 10.49, 'tensile_strength_min': 125, 'elastic_modulus': 71, 'thermal_conductivity': 429, 'specific_heat': 235, 'melting_point_min': 961,
        'composition': 'Ag 99.99%', 'hardness': '25 HV',
        'description': 'FCC crystal structure (a=0.408621 nm). Values based on 5mm wire annealed at 600°C.',
        'source_url': 'https://www.espimetals.com/index.php/technical-data/194-Silver', 'source_name': 'ESPI Metals / NIST', 'is_verified': True
    },
    {
        'name': 'Sterling Silver (92.5% Ag)', 'category': 'Silver', 'subcategory': 'Silver Alloy',
        'density': 10.36, 'tensile_strength_min': 207, 'yield_strength_min': 124, 'elongation': 41, 'hardness': '140 HV', 'elastic_modulus': 75, 'melting_point_min': 788,
        'composition': 'Ag 92.5%, Cu 7.5%',
        'description': 'Standard jewelry/silversmithing alloy. Values are for annealed state; wire hard states can reach 552 MPa and 140 HV.',
        'source_url': 'https://www.espimetals.com/index.php/technical-data/81-Silver%20-%20Sterling', 'source_name': 'ESPI Metals', 'is_verified': True
    },
    {
        'name': 'Argentium Silver (93.5% Ag)', 'category': 'Silver', 'subcategory': 'Silver Alloy',
        'density': 10.35, 'tensile_strength_min': 249, 'yield_strength_min': 111, 'elongation': 29, 'hardness': '68 HV', 'melting_point_min': 803,
        'composition': 'Ag 93.5%, Ge replacing part of Cu',
        'description': 'Precipitation-hardenable sterling silver variant. Germanium addition prevents firescale and vastly improves tarnish resistance. As-cast grain size ~90 μm.',
        'source_url': 'https://products.riogrande.com/content/Instruction-Sheets/Argentium-935-Silver-Casting-Grain-Technical-Sheet-IS.pdf', 'source_name': 'Rio Grande / Argentium', 'is_verified': True
    },
    {
        'name': 'Coin Silver (90% Ag)', 'category': 'Silver', 'subcategory': 'Silver Alloy',
        'density': 10.31, 'tensile_strength_min': 270, 'melting_point_min': 779,
        'composition': 'Ag 90%, Cu 10%',
        'description': 'Legacy US coinage standard. Base physical properties track closely with standard Ag-Cu binary curves.',
        'source_url': 'https://www.espimetals.com/index.php/technical-data/194-Silver', 'source_name': 'ESPI Metals', 'is_verified': True
    },
    {
        'name': 'Silver-Copper Brazing Alloy (BAg-1, 45% Ag)', 'category': 'Silver', 'subcategory': 'Silver Brazing Alloy',
        'density': 9.4, 'melting_point_min': 605,
        'composition': 'Ag 45%, Cu 15%, Zn 16%, Cd 24%',
        'description': 'AWS A5.8 BAg-1 / AMS 4769. General purpose low-temperature braze. Contains Cadmium (fume hazard during brazing).',
        'source_url': 'https://princewebstorage1.blob.core.windows.net/websitefiles/SilverAlloy45(BAg-1)(AMS4769)TDS.pdf', 'source_name': 'Prince & Izant / AWS A5.8', 'is_verified': True
    },
    {
        'name': 'Silver-Copper Brazing Alloy (BAg-7, 56% Ag)', 'category': 'Silver', 'subcategory': 'Silver Brazing Alloy',
        'density': 9.2, 'tensile_strength_min': 275, 'melting_point_min': 620,
        'composition': 'Ag 56%, Cu 22%, Zn 17%, Sn 5%',
        'description': 'AWS BAg-7 / AMS 4763. Cadmium-free substitute. Brazed joint tensile strength: 25,000–50,000 psi depending on base metal (steel/copper/brass).',
        'source_url': 'https://princeizant.com/product/AG56-CU22-ZN17', 'source_name': 'Prince & Izant TDS', 'is_verified': True
    },
    {
        'name': 'Silver-Copper Eutectic (72Ag-28Cu)', 'category': 'Silver', 'subcategory': 'Silver-Copper Alloy',
        'density': 10.0, 'tensile_strength_min': 300, 'melting_point_min': 780,
        'composition': 'Ag 72%, Cu 28%',
        'description': 'UNS P07720 / AWS BAg-8. True eutectic point composition. Excellent for vacuum brazing of copper/nickel.',
        'source_url': 'https://www.matweb.com/search/datasheet_print.aspx?matguid=7f60ee352a634641bc63d09fc8b3a718', 'source_name': 'MatWeb', 'is_verified': True
    },
    {
        'name': 'Silver-Palladium Alloy (70Ag-30Pd)', 'category': 'Silver', 'subcategory': 'Silver-Palladium Alloy',
        'density': 10.7, 'melting_point_min': 1050,
        'composition': 'Ag 70wt%, Pd 25-30wt%, Trace modifiers',
        'description': 'ADA classified noble alloy. High tarnish resistance. Used heavily in dental restoration prior to modern ceramics.',
        'source_url': 'https://www.sciencedirect.com/topics/pharmacology-toxicology-and-pharmaceutical-science/dental-alloy', 'source_name': 'ScienceDirect', 'is_verified': True
    },
    {
        'name': 'Silver Thick Film Paste (Conductor)', 'category': 'Silver', 'subcategory': 'Silver Paste',
        'composition': 'Ag 100% (in active conductive phase)',
        'description': 'Conductivity ≤3.5 mΩ/sq at 12μm. Viscosity 150–200 Kcps. Firing range 490–550°C. Used for PCBs, thick-film sensors.',
        'source_url': 'https://pim.heraeus.com/datasheets/HET/TFM/C8829A.pdf', 'source_name': 'Heraeus (C8829A TDS)', 'is_verified': True
    },
    {
        'name': 'Silver-Cadmium Oxide (AgCdO) Contact Material', 'category': 'Silver', 'subcategory': 'Electrical Contact',
        'density': 9.95, 'tensile_strength_min': 250, 'hardness': '60 HV', 'thermal_conductivity': 350,
        'composition': 'Ag ~85-90%, CdO 10-15%',
        'description': 'Electrical contact material. Resistivity 2.0–2.25 μΩ·cm. Excellent arc-erosion and welding resistance for relays/switches.',
        'source_url': 'https://americanelements.com/silver-cadmium-oxide', 'source_name': 'American Elements', 'is_verified': True
    },
    {
        'name': 'Silver-Tungsten (AgW) Contact Material', 'category': 'Silver', 'subcategory': 'Electrical Contact',
        'density': 14.0, 'hardness': '68 HRB', 'elastic_modulus': 190, 'thermal_conductivity': 490,
        'composition': 'W 51.8-58%, Ag 42-46%',
        'description': 'ASTM B631 Class C compliant. High density pressed and sintered alloy for heavy-duty circuit breakers and EDM electrodes.',
        'source_url': 'https://samaterials.com/tungsten-alloy-composites/138-tungsten-silver.html', 'source_name': 'Stanford Advanced Materials / ASTM B631', 'is_verified': True
    }
]

print("=== Processing Silver Batch ===")
for m in batch_7:
    name = m['name']
    r = supabase.table('materials').select('id').eq('name', name).execute()
    if r.data:
        supabase.table('materials').update(m).eq('id', r.data[0]['id']).execute()
        print(f"Updated: {name}")
    else:
        supabase.table('materials').insert(m).execute()
        print(f"Inserted: {name}")

print("\nSilver batch complete!")
