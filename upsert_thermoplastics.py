import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

materials = [
    {
        "name": "PA66-GF30 (Nylon 66 + 30% Glass Fiber)",
        "category": "Composite",
        "subcategory": "Thermoplastic Composite",
        "source_url": "https://download.basf.com/p1/8a8082587fd4b608017fd6587a9757d9/en/ULTRAMID%3Csup%3E%C2%AE%3Csup%3E_A3EG6, https://www.lookpolymers.com/polymer_Kingfa-PA66-G30-30-Glass-Fiber-Reinforced-PA66.php",
        "extraction_method": "Verified Source Datasheet",
        "tensile_strength_max": 190.0,
        "elastic_modulus": 10.0,
        "description": "BASF Ultramid A3EG6 standard PA66-GF30 injection-molding grade. Headline values are 'Dry as molded'. Moisture absorption significantly reduces strength and stiffness (see conditioned properties).",
        "computational_properties": {
            "moisture_state": "Dry as molded",
            "flexural_strength_MPa": 280,
            "flexural_modulus_GPa": 8.6,
            "strain_at_break_pct": 3.0,
            "charpy_notched_impact_kJ_m2": 11,
            "ul94_flammability": "HB",
            "conditioned_50RH_properties": {
                "tensile_strength_MPa": 130,
                "elastic_modulus_GPa": 7.2,
                "flexural_strength_MPa": 210,
                "flexural_modulus_GPa": 6.5,
                "strain_at_break_pct": 5.0
            }
        }
    },
    {
        "name": "PEEK-CF30 (PEEK + 30% Carbon Fiber)",
        "category": "Composite",
        "subcategory": "Thermoplastic Composite",
        "source_url": "https://www.victrex.com/en/downloads/datasheets/victrex-peek-90ca30, https://www.lookpolymers.com/polymer_Victrex-PEEK-450CA30-30-Carbon-Fiber-Reinforced.php, https://ceadgroup.com/wp-content/uploads/2021/05/Materials-Victrex-PEEK-90CA30.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 1.40,
        "tensile_strength_max": 275.0,
        "elastic_modulus": 28.0,
        "compressive_strength": 300.0,
        "description": "VICTREX PEEK 90CA30 high-flow 30% CF injection-molding grade. Exceptional property retention at high temperatures; aerospace/medical implant grade.",
        "computational_properties": {
            "flexural_strength_MPa": 380,
            "flexural_modulus_GPa": 24.0,
            "water_absorption_saturation_100C_pct": 0.45,
            "temperature_dependent_properties": {
                "125C": {"tensile_strength_MPa": 180, "flexural_strength_MPa": 275, "compressive_strength_MPa": 200},
                "175C": {"tensile_strength_MPa": 110, "flexural_strength_MPa": 130},
                "225C": {"tensile_strength_MPa": 85, "flexural_strength_MPa": 65, "compressive_strength_MPa": 70},
                "275C": {"tensile_strength_MPa": 65}
            }
        }
    },
    {
        "name": "PC-GF20 (Polycarbonate + 20% Glass Fiber)",
        "category": "Composite",
        "subcategory": "Thermoplastic Composite",
        "source_url": "https://materialdatacenter.com/ms/zh/Makrolon/Covestro+Deutschland+AG/Makrolon%C2%AE+9125/640afdd0/410, https://samtion.com/product/covestro-makrolon-9125/, https://www.lookpolymers.com/polymer_PolyOne-Edgetek-PC-20GF000-Polycarbonate-PC.php",
        "extraction_method": "Verified Source Datasheet",
        "density": 1.34,
        "tensile_strength_max": 85.0,
        "elastic_modulus": 5.8,
        "description": "Covestro Makrolon 9125 (20% glass fiber, flame-retardant UL94V-0). Electronics housing grade.",
        "computational_properties": {
            "flexural_strength_MPa": 140,
            "flexural_modulus_GPa": 5.6,
            "strain_at_break_pct": 2.5,
            "charpy_notched_impact_kJ_m2": 8,
            "heat_deflection_temp_1_8MPa_C": 138,
            "ul94_flammability": "V-0"
        }
    }
]

print("Upserting Thermoplastic Composites...")
for mat in materials:
    name = mat["name"]
    existing = supabase.table("materials").select("id").eq("name", name).execute()
    if existing.data:
        res = supabase.table("materials").update(mat).eq("name", name).execute()
        print(f"Updated {name}")
    else:
        res = supabase.table("materials").insert(mat).execute()
        print(f"Inserted {name}")

print("Done.")
