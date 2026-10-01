
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

materials = [
    {
        "name": "CFRP (Standard Modulus UD / Epoxy)",
        "category": "Composite",
        "subcategory": "Polymer Matrix Composite",
        "source_url": "https://www.toraycma.com/wp-content/uploads/T300-Data-Sheet.pdf, https://hexcel.com/wp-content/uploads/2025/12/HexPly_8552_eu_DataSheet1.pdf, https://wichita.edu/industry_and_defense/NIAR/Research/hexcel-8552/AS4-Unitape-2.pdf, https://eng.libretexts.org/Under_Construction/Aerospace_Structures_(Johnson)/08%3A_Laminated_bars_of_fiber-reinforced_polymer_composites/8.01%3A_Nomenclature_of_composite_materials",
        "extraction_method": "Verified Source Datasheet",
        "density": 1.58,
        "tensile_strength_max": 2137.0,
        "elastic_modulus": 135.0,
        "compressive_strength": 1530.0,
        "shear_modulus": 5.61,
        "thermal_expansion_coefficient": -0.63,
        "description": "Aerospace-grade standard modulus carbon fiber UD prepreg (AS4 / T300). Values anchored to Hexcel AS4/8552 at 60% Vf. Hexcel revision 2025/2018 tracked."
    },
    {
        "name": "CFRP (High Modulus UD / Epoxy)",
        "category": "Composite",
        "subcategory": "Polymer Matrix Composite",
        "source_url": "https://www.toraycma.com/wp-content/uploads/M46J-Data-Sheet.pdf, https://hexcel.com/wp-content/uploads/2025/12/IM7_HexTow_DataSheet.pdf, https://wichita.edu/industry_and_defense/NIAR/Documents/NCP-RP-2009-028-Rev-B-HEXCEL-8552-IM7-Uni-SAR-4-16-2019.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 1.60,
        "tensile_strength_max": 2190.0,
        "elastic_modulus": 267.0,
        "compressive_strength": 1090.0,
        "thermal_expansion_coefficient": -0.9,
        "description": "Aerospace-grade high modulus carbon fiber UD prepreg. Anchored to Toray M46J at 60% Vf (IM7/8552 treated as intermediate modulus comparator). Thermal conductivity approx 83 W/mK."
    },
    {
        "name": "CFRP (Woven 3K 2x2 Twill / Epoxy)",
        "category": "Composite",
        "subcategory": "Polymer Matrix Composite",
        "source_url": "https://acpcomposites.com/shop/carbon-fiber/carbon-prepregs/5-8-oz-carbon-fiber-2x2-twill-weave-rts-prepreg, https://pmc.ncbi.nlm.nih.gov/articles/PMC9679481/, https://www.wichita.edu/industry_and_defense/NIAR/Research/hexcel-8552/AS4-PW-2.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 1.578,
        "tensile_strength_max": 750.0,
        "elastic_modulus": 76.0,
        "compressive_strength": 620.0,
        "shear_modulus": 2.87,
        "description": "Standard 3K 2x2 twill carbon fiber / epoxy fabric composite (Vf ~50%). Strength anchors from ACP Composites 5.8oz prepreg. Shear modulus and Poisson ratio from Liu et al (2022)."
    },
    {
        "name": "Carbon-Carbon Composite (C/C)",
        "category": "Composite",
        "subcategory": "Ceramic Matrix Composite",
        "source_url": "https://www.semcocarbon.com/file-downloads-folder/carbon-composite-spec-sheet-REV2.pdf, https://www.ias.ac.in/article/fulltext/sadh/028/01-02/0349-0358, https://doi.org/10.3389/fmats.2024.1374034",
        "extraction_method": "Verified Source Datasheet",
        "density": 1.75,
        "tensile_strength_max": 103.0,
        "elastic_modulus": 35.8,
        "compressive_strength": 200.0,
        "thermal_expansion_coefficient": 1.0,
        "description": "Industrial hot-zone grade C/C composite (Semco Carbon SHD/SHL series). Stable to 1500-2000 C. Not an F1-brake or nozzle grade."
    }
]

print("Upserting Advanced Carbon Composites...")
for mat in materials:
    # check if exists
    name = mat["name"]
    existing = supabase.table("materials").select("id").eq("name", name).execute()
    if existing.data:
        # update
        res = supabase.table("materials").update(mat).eq("name", name).execute()
        print(f"Updated {name}")
    else:
        # insert
        res = supabase.table("materials").insert(mat).execute()
        print(f"Inserted {name}")

print("Done.")

