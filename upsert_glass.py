import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

materials = [
    {
        "name": "FR4 (Glass-Reinforced Epoxy)",
        "category": "Composite",
        "subcategory": "Polymer Matrix Composite",
        "source_url": "https://laminatedplastics.com/fr-4.pdf, https://www.atlasfibre.com/material/fr-4/, https://en.wikipedia.org/wiki/FR-4",
        "extraction_method": "Verified Source Datasheet",
        "density": 1.85,
        "tensile_strength_max": 276.0,
        "elastic_modulus": 24.1,
        "compressive_strength": 262.0,
        "hardness": "Rockwell M110",
        "thermal_conductivity": 0.29,
        "description": "NEMA LI-1 Grade FR-4. Mechanical properties vary significantly across manufacturers (Tensile ranges 40k-65k psi). Carries UL94 V-0 flammability rating.",
        "computational_properties": {
            "source_variance": "High",
            "tensile_strength_range_psi": "40,000 - 65,000",
            "flexural_modulus_LW_GPa": 18.6,
            "poissons_ratio_LW": 0.136,
            "thermal_conductivity_in_plane_W_mK": 0.81,
            "shear_strength_psi": 21500
        }
    },
    {
        "name": "G-10 (Continuous Woven Glass / Epoxy)",
        "category": "Composite",
        "subcategory": "Polymer Matrix Composite",
        "source_url": "https://thegundcompany.com/wp-content/uploads/2024/03/NEMA-G-10-Glass-Epoxy-Laminate-by-The-Gund-Co.pdf, https://www.boedeker.com/Product/Micaply-G-10-Glass-Epoxy-Laminate-Sheet, https://www.makeitfrom.com/material-properties/NEMA-Grade-G-10-GEE-Glass-Epoxy-Laminate",
        "extraction_method": "Verified Source Datasheet",
        "density": 1.85,
        "tensile_strength_max": 300.0,
        "elastic_modulus": 17.0,
        "compressive_strength": 360.0,
        "hardness": "Rockwell M98",
        "thermal_expansion_coefficient": 9.0,
        "description": "NEMA Grade G-10. Near identical physical properties to FR-4, but without the brominated flame retardant (lacks UL94 V-0).",
        "computational_properties": {
            "source_variance": "High",
            "flexural_strength_MPa": 380,
            "shear_strength_MPa": 130,
            "punch_shear_strength_MPa": 172,
            "dielectric_strength_kV_mm": 18
        }
    },
    {
        "name": "GFRP (Chopped Strand Mat / Polyester Resin)",
        "category": "Composite",
        "subcategory": "Polymer Matrix Composite",
        "source_url": "https://www.fibreglast.com/blogs/learning-center/physical-properties-of-laminates",
        "extraction_method": "Verified Source Datasheet",
        "density": 1.61,
        "tensile_strength_max": 152.0,
        "elastic_modulus": 9.7,
        "description": "Indicative properties for CSM/polyester hand-layup laminates (Vf ~25-35%). Highly dependent on layup quality, resin ratio, and void content.",
        "computational_properties": {
            "source_confidence": "Low",
            "warning": "Treat as indicative ballpark data. Process variation is extremely high."
        }
    },
    {
        "name": "GFRP (S-Glass UD / Epoxy)",
        "category": "Composite",
        "subcategory": "Polymer Matrix Composite",
        "source_url": "https://wichita.edu/industry_and_defense/NIAR/Research/tencate-bt250e-6/S2-Glass-Unitape.pdf",
        "extraction_method": "Verified Source Datasheet",
        "tensile_strength_max": 1367.0,
        "elastic_modulus": 46.2,
        "compressive_strength": 383.0,
        "description": "Aerospace-qualified S-2 Glass unidirectional tape (TenCate BT250E-6). S-2 Glass delivers ~85% more tensile strength and 25% more stiffness than standard E-glass.",
        "computational_properties": {
            "shear_strength_interlaminar_MPa": 55.2,
            "raw_fiber_tensile_strength_MPa": 3551,
            "dry_Tg_C": 144
        }
    },
    {
        "name": "GFRP (E-Glass Woven / Epoxy)",
        "category": "Composite",
        "subcategory": "Polymer Matrix Composite",
        "source_url": "https://acpcomposites.com/wp-content/uploads/2024/05/Mechanical-Properties-of-Carbon-Fiber-Composite-Materials.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 1.90,
        "tensile_strength_max": 440.0,
        "elastic_modulus": 25.0,
        "compressive_strength": 425.0,
        "shear_modulus": 4.0,
        "thermal_expansion_coefficient": 11.6,
        "description": "Standard E-glass fabric / epoxy resin composite (Vf 50%). Balanced quasi-isotropic in-plane properties (0 and 90 degree values are equal).",
        "computational_properties": {
            "shear_strength_in_plane_MPa": 40,
            "poissons_ratio_v12": 0.2
        }
    }
]

print("Upserting Glass Fiber Composites...")
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
