import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

materials = [
    {
        "name": "AlSiC-9 (Al-SiC Metal Matrix Composite)",
        "category": "Composite",
        "subcategory": "Metal Matrix Composite",
        "source_url": "https://cpstechnologysolutions.com/wp-content/uploads/2025/09/CPS-Alsic-2025-Final.pdf, https://ceramics.ferrotec.com/materials/metal-matrix/al-sic/, https://sst.semiconductor-digest.com/?p=37330",
        "extraction_method": "Verified Source Datasheet",
        "density": 3.01,
        "tensile_strength_max": 488.0, # Using Bend Strength
        "elastic_modulus": 188.0,
        "shear_modulus": 76.0,
        "thermal_conductivity": 190.0,
        "specific_heat": 0.741,
        "thermal_expansion_coefficient": 8.00,
        "description": "CPS AlSiC-9 (63 vol% SiC). Used heavily for thermal management (IGBT baseplates) due to low CTE (8 ppm/C) matching semiconductors and high thermal conductivity.",
        "computational_properties": {
            "bend_strength_4_pt_MPa": 488,
            "fracture_toughness_MPa_m_half": 11.3,
            "elongation_pct": 0.295,
            "electrical_resistance_uOhm_cm": 20.7,
            "sic_volume_fraction_pct": 63
        }
    },
    {
        "name": "AlSiC-12 (Al-SiC Metal Matrix Composite)",
        "category": "Composite",
        "subcategory": "Metal Matrix Composite",
        "source_url": "https://cpstechnologysolutions.com/wp-content/uploads/2025/09/CPS-Alsic-2025-Final.pdf, https://ceramics.ferrotec.com/materials/metal-matrix/al-sic/",
        "extraction_method": "Verified Source Datasheet",
        "density": 2.89,
        "tensile_strength_max": 471.0, # Using Bend Strength
        "elastic_modulus": 167.0,
        "shear_modulus": 69.0,
        "thermal_conductivity": 180.0,
        "specific_heat": 0.808,
        "thermal_expansion_coefficient": 10.90,
        "description": "CPS AlSiC-12 (37 vol% SiC). Lower SiC loading trades off higher CTE (10.9 ppm/C) for slightly lower density and stiffness.",
        "computational_properties": {
            "bend_strength_4_pt_MPa": 471,
            "electrical_resistance_uOhm_cm": 20.7,
            "sic_volume_fraction_pct": 37
        }
    },
    {
        "name": "Ti-SiC (Ti-6Al-4V / SCS-6 Composite)",
        "category": "Composite",
        "subcategory": "Metal Matrix Composite",
        "source_url": "https://www.cambridge.org/core/product/F001DC9D9AA326DAA1F522F327C8788A, https://www.specmaterials.com/silicon-carbide-fiber-1, https://ntrs.nasa.gov/citations/19980223374",
        "extraction_method": "Verified Source Datasheet",
        "tensile_strength_max": 1565.0,
        "elastic_modulus": 182.0,
        "description": "Ti-6Al-4V Titanium alloy matrix reinforced with continuous SCS-6 Silicon Carbide fibers. Extensively studied for gas-turbine bladed rings (blings); ~15% lighter than Ti alloys.",
        "computational_properties": {
            "fiber_tensile_strength_MPa": 3900,
            "fiber_tensile_modulus_GPa": 380,
            "matrix_alloy": "Ti-6Al-4V"
        }
    },
    {
        "name": "B4C-Al (Metamic / Neutron Absorber Composite)",
        "category": "Composite",
        "subcategory": "Metal Matrix Composite",
        "source_url": "https://ww2.nrc.gov/docs/ML1307/ML13079A685.pdf, https://holtecinternational.com/products-and-services/innovative-technologies/neutronabsorbermaterial/",
        "extraction_method": "Verified Source Datasheet",
        "tensile_strength_max": 250.0,
        "tensile_strength_yield": 180.0,
        "description": "Al-B4C Metal Matrix Composite (e.g. Metamic, Boralyn). Al-6061 powder matrix with nuclear-grade B4C. Specifically used for neutron shielding in dry-cask nuclear storage.",
        "computational_properties": {
            "tensile_strength_range_MPa": "227 - 276",
            "yield_strength_range_MPa": "138 - 227",
            "b4c_loading_pct": "10 - 33"
        }
    }
]

print("Upserting MMC Composites...")
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
