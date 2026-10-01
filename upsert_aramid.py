import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

materials = [
    {
        "name": "Kevlar 49 / Epoxy (Aramid Fabric Composite)",
        "category": "Composite",
        "subcategory": "Polymer Matrix Composite",
        "source_url": "https://www.dupont.com/content/dam/aramids/amer/us/en/safety/public/documents/en/Kevlar_Technical_Guide_0319.pdf, https://acpcomposites.com/wp-content/uploads/2024/05/Mechanical-Properties-of-Carbon-Fiber-Composite-Materials.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 1.40,
        "tensile_strength_max": 480.0,
        "elastic_modulus": 30.0,
        "compressive_strength": 190.0,
        "shear_modulus": 5.0,
        "description": "Kevlar 49 / Epoxy Fabric Composite (Vf 50%). Note the severe tensile/compressive asymmetry characteristic of aramid composites (buckles in compression).",
        "computational_properties": {
            "measurement_level": "composite",
            "tension_compression_asymmetric": True,
            "shear_strength_MPa": 50,
            "fiber_density_g_cc": 1.44,
            "fiber_tensile_strength_MPa": 3000,
            "fiber_tensile_modulus_GPa": 124
        }
    },
    {
        "name": "Kevlar 49 / Epoxy (Aramid UD Composite)",
        "category": "Composite",
        "subcategory": "Polymer Matrix Composite",
        "source_url": "https://www.dupont.com/content/dam/aramids/amer/us/en/safety/public/documents/en/Kevlar_Technical_Guide_0319.pdf, https://acpcomposites.com/wp-content/uploads/2024/05/Mechanical-Properties-of-Carbon-Fiber-Composite-Materials.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 1.40,
        "tensile_strength_max": 1300.0,
        "elastic_modulus": 75.0,
        "compressive_strength": 280.0,
        "shear_modulus": 2.0,
        "description": "Kevlar 49 / Epoxy Unidirectional (UD) Composite (Vf 60%). Exhibits extreme tensile/compressive asymmetry (1300 MPa vs 280 MPa).",
        "computational_properties": {
            "measurement_level": "composite",
            "tension_compression_asymmetric": True,
            "shear_strength_MPa": 60,
            "elastic_modulus_transverse_GPa": 6
        }
    },
    {
        "name": "Dyneema / UHMWPE Composite",
        "category": "Composite",
        "subcategory": "Polymer Matrix Composite",
        "source_url": "https://norwegen-angelfreunde.de/attachment/26938-zugfestigkeit-pdf, https://www.sciencedirect.com/science/article/abs/pii/S0142941819317568, https://www.dsm.com/content/dam/dsm/dyneema/pt_BR/Downloads/LP%20Product%20Grades/DSM_Hard_Ballistic_solutions_BR.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 0.97,
        "tensile_strength_max": 725.0,
        "elastic_modulus": 130.0,
        "description": "Dyneema UHMWPE hard ballistic laminate (e.g. HB26). Tensile strength varies drastically based on test method (550 - 1150 MPa) due to grip slippage; 725 MPa anchored via Russell et al.",
        "computational_properties": {
            "measurement_level": "composite",
            "source_confidence": "Low",
            "tensile_strength_range_MPa": "550 - 1150",
            "fiber_density_g_cc": 0.97,
            "fiber_tensile_strength_GPa": "2.7 - 3.2",
            "fiber_tensile_modulus_GPa": "89 - 99",
            "warning": "Laminate properties highly dependent on testing methodology."
        }
    },
    {
        "name": "Zylon (PBO) Fiber Composite",
        "category": "Composite",
        "subcategory": "Polymer Matrix Composite",
        "source_url": "https://www.toyobo-mc.jp/wordpress/wp-content/uploads/2023/09/hp_fiber_data_zylon_en.pdf, https://www.lookpolymers.com/pdf/Toyobo-Zylon-HM-FiberEpoxy-Matrix-Unidirectional-Composite.pdf, https://en.wikipedia.org/wiki/Zylon",
        "extraction_method": "Verified Source Datasheet",
        "tensile_strength_max": 2700.0,
        "elastic_modulus": 140.0,
        "description": "Zylon HM (PBO) fiber / epoxy unidirectional composite (Vf 59%). Highest tensile strength of organic fibers.",
        "computational_properties": {
            "measurement_level": "composite",
            "source_confidence": "High",
            "flexural_yield_strength_MPa": 550,
            "flexural_modulus_GPa": 70,
            "poissons_ratio": 0.30,
            "fiber_density_g_cc": 1.56,
            "fiber_tensile_strength_GPa": 5.8,
            "fiber_tensile_modulus_GPa": 270
        }
    }
]

print("Upserting Aramid and UHMWPE Composites...")
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
