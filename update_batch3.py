import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

def add_comp_props(base_dict, new_props):
    res = dict(base_dict) if base_dict else {}
    res.update(new_props)
    return res

updates = [
    {
        "name": "Oak Wood (Dry)",
        "source_url": "https://www.fpl.fs.usda.gov/documnts/fplgtr/fplgtr190/chapter_05.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 0.68,
        "tensile_strength_max": 105.0, # MOR MPa
        "elastic_modulus": 12.3, # MOE GPa
        "compressive_strength": 51.3, # Comp// MPa
        "hardness": "6000 N",
        "description": "White oak (Quercus alba), 12% Moisture Content. Selected as representative over red/bur oak.",
        "computational_properties": {
            "specific_gravity": 0.68,
            "work_to_max_load_kJ_m3": 102,
            "impact_bending_mm": 940,
            "compression_perp_kPa": 7400,
            "shear_parallel_kPa": 13800,
            "tension_perp_kPa": 5500,
            "elastic_ratio_E_T_E_L": 0.072,
            "elastic_ratio_E_R_E_L": 0.163,
            "elastic_ratio_G_LR_E_L": 0.086,
            "poissons_ratio_LR": 0.369,
            "poissons_ratio_LT": 0.428,
            "poissons_ratio_RT": 0.618,
            "poissons_ratio_TR": 0.300,
            "poissons_ratio_RL": 0.074,
            "poissons_ratio_TL": 0.036,
            "shear_corrected_moe_GPa": 12.3 * 1.1
        }
    },
    {
        "name": "Oak Wood (Green)",
        "source_url": "https://www.fpl.fs.usda.gov/documnts/fplgtr/fplgtr190/chapter_05.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 0.60,
        "tensile_strength_max": 57.0,
        "elastic_modulus": 8.6,
        "compressive_strength": 24.5,
        "hardness": "4700 N",
        "description": "White oak (Quercus alba), Green state.",
        "computational_properties": {
            "specific_gravity": 0.60,
            "work_to_max_load_kJ_m3": 80,
            "impact_bending_mm": 1070,
            "compression_perp_kPa": 4600,
            "shear_parallel_kPa": 8600,
            "tension_perp_kPa": 5300,
            "shear_corrected_moe_GPa": 8.6 * 1.1
        }
    },
    {
        "name": "Pine Wood (Dry)",
        "source_url": "https://www.fpl.fs.usda.gov/documnts/fplgtr/fplgtr190/chapter_05.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 0.51,
        "tensile_strength_max": 88.0,
        "elastic_modulus": 12.3,
        "compressive_strength": 49.2,
        "hardness": "3100 N",
        "description": "Loblolly pine (Pinus taeda). 12% Moisture Content. Note: 'Pine' spans a wide strength range; Loblolly is used here as the Southern Yellow Pine standard.",
        "computational_properties": {
            "specific_gravity": 0.51,
            "work_to_max_load_kJ_m3": 72,
            "impact_bending_mm": 760,
            "compression_perp_kPa": 5400,
            "shear_parallel_kPa": 9600,
            "tension_perp_kPa": 3200,
            "tensile_strength_parallel_kPa": 80000 * 1.13, # green + 13%
            "toughness_radial_J": 2600,
            "toughness_tangential_J": 4200,
            "elastic_ratio_E_T_E_L": 0.078,
            "elastic_ratio_E_R_E_L": 0.113,
            "elastic_ratio_G_LR_E_L": 0.082,
            "elastic_ratio_G_LT_E_L": 0.081,
            "elastic_ratio_G_RT_E_L": 0.013,
            "poissons_ratio_LR": 0.328,
            "poissons_ratio_LT": 0.292,
            "poissons_ratio_RT": 0.382,
            "poissons_ratio_TR": 0.362,
            "shear_corrected_moe_GPa": 12.3 * 1.1
        }
    },
    {
        "name": "Pine Wood (Green)",
        "source_url": "https://www.fpl.fs.usda.gov/documnts/fplgtr/fplgtr190/chapter_05.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 0.47,
        "tensile_strength_max": 50.0,
        "elastic_modulus": 9.7,
        "compressive_strength": 24.2,
        "hardness": "2000 N",
        "description": "Loblolly pine (Pinus taeda), Green state.",
        "computational_properties": {
            "specific_gravity": 0.47,
            "work_to_max_load_kJ_m3": 57,
            "impact_bending_mm": 760,
            "compression_perp_kPa": 2700,
            "shear_parallel_kPa": 5900,
            "tension_perp_kPa": 1800,
            "tensile_strength_parallel_kPa": 80000,
            "toughness_radial_J": 5000,
            "toughness_tangential_J": 6200,
            "shear_corrected_moe_GPa": 9.7 * 1.1
        }
    },
    {
        "name": "Redwood Wood (Dry)",
        "source_url": "https://www.fpl.fs.usda.gov/documnts/fplgtr/fplgtr190/chapter_05.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 0.35,
        "tensile_strength_max": 54.0,
        "elastic_modulus": 7.6,
        "compressive_strength": 36.0,
        "hardness": "1900 N",
        "description": "Coast redwood (Sequoia sempervirens), 12% Moisture Content. Young-growth values used for realistic commercial availability.",
        "computational_properties": {
            "specific_gravity": 0.35,
            "work_to_max_load_kJ_m3": 36,
            "impact_bending_mm": 380,
            "compression_perp_kPa": 3600,
            "shear_parallel_kPa": 7600,
            "tension_perp_kPa": 1700,
            "tensile_strength_parallel_kPa": 62700 * 1.13, # roughly +13% for softwood dry
            "elastic_ratio_E_T_E_L": 0.089,
            "elastic_ratio_E_R_E_L": 0.087,
            "elastic_ratio_G_LR_E_L": 0.066,
            "elastic_ratio_G_LT_E_L": 0.077,
            "elastic_ratio_G_RT_E_L": 0.011,
            "poissons_ratio_LR": 0.360,
            "poissons_ratio_LT": 0.346,
            "poissons_ratio_RT": 0.373,
            "poissons_ratio_TR": 0.400,
            "shear_corrected_moe_GPa": 7.6 * 1.1
        }
    },
    {
        "name": "Redwood Wood (Green)",
        "source_url": "https://www.fpl.fs.usda.gov/documnts/fplgtr/fplgtr190/chapter_05.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 0.34,
        "tensile_strength_max": 41.0,
        "elastic_modulus": 6.6,
        "compressive_strength": 21.4,
        "hardness": "1600 N",
        "description": "Coast redwood (Sequoia sempervirens), Green state. Young-growth.",
        "computational_properties": {
            "specific_gravity": 0.34,
            "work_to_max_load_kJ_m3": 39,
            "impact_bending_mm": 410,
            "compression_perp_kPa": 1900,
            "shear_parallel_kPa": 6100,
            "tension_perp_kPa": 2100,
            "tensile_strength_parallel_kPa": 62700,
            "shear_corrected_moe_GPa": 6.6 * 1.1
        }
    },
    {
        "name": "Rosewood Wood (Dry)",
        "source_url": "https://www.fpl.fs.usda.gov/documnts/fplgtr/fplgtr190/chapter_05.pdf, https://www.wood-database.com/east-indian-rosewood/",
        "extraction_method": "Verified Source Datasheet",
        "density": 0.83, # Wood Database states avg dried weight is 52 lbs/ft3 which is ~830 kg/m3. FPL doesn't give 12% SG.
        "tensile_strength_max": 116.5,
        "elastic_modulus": 12.3,
        "compressive_strength": 63.6,
        "hardness": "14100 N",
        "description": "Indian rosewood (Dalbergia latifolia), 12% Moisture Content. Note: Hardness value doubles from green, which is an unusually large jump. FPL Table 5-5 warns of inadequate sampling.",
        "computational_properties": {
            "work_to_max_load_kJ_m3": 90,
            "shear_parallel_kPa": 14400,
            "source_confidence": "Low",
            "shear_corrected_moe_GPa": 12.3 * 1.1
        }
    },
    {
        "name": "Rosewood Wood (Green)",
        "source_url": "https://www.fpl.fs.usda.gov/documnts/fplgtr/fplgtr190/chapter_05.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 0.75,
        "tensile_strength_max": 63.4,
        "elastic_modulus": 8.2,
        "compressive_strength": 31.2,
        "hardness": "6900 N",
        "description": "Indian rosewood (Dalbergia latifolia), Green state.",
        "computational_properties": {
            "specific_gravity": 0.75,
            "work_to_max_load_kJ_m3": 80,
            "shear_parallel_kPa": 9700,
            "source_confidence": "Low",
            "shear_corrected_moe_GPa": 8.2 * 1.1
        }
    }
]

for up in updates:
    name = up.pop("name")
    
    # fetch existing computational_properties to merge
    existing = supabase.table("materials").select("computational_properties").eq("name", name).execute()
    if existing.data:
        curr_comp = existing.data[0].get("computational_properties")
        if "computational_properties" in up:
            up["computational_properties"] = add_comp_props(curr_comp, up["computational_properties"])
            
    try:
        res = supabase.table("materials").update(up).eq("name", name).execute()
        if len(res.data) > 0:
            print(f"Updated {name}")
        else:
            print(f"Failed to find {name} in DB.")
    except Exception as e:
        print(f"Error updating {name}: {e}")

print("Batch 3 update completed.")
