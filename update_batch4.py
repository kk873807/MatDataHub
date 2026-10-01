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
        "name": "Spruce Wood (Dry)",
        "source_url": "https://www.fpl.fs.usda.gov/documnts/fplgtr/fplgtr190/chapter_05.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 0.40,
        "tensile_strength_max": 70.0,
        "elastic_modulus": 10.8,
        "compressive_strength": 38.7,
        "hardness": "2300 N",
        "description": "Sitka spruce (Picea sitchensis). 12% Moisture Content. The aviation/acoustic standard due to its high strength-to-weight ratio. (Note: Engelmann spruce is more common for structural framing but weaker).",
        "computational_properties": {
            "specific_gravity": 0.40,
            "work_to_max_load_kJ_m3": 65,
            "impact_bending_mm": 640,
            "compression_perp_kPa": 4000,
            "shear_parallel_kPa": 7900,
            "tension_perp_kPa": 2600,
            "tensile_strength_parallel_kPa": 59300 * 1.13, # Softwood +13% from green approx
            "elastic_ratio_E_T_E_L": 0.043,
            "elastic_ratio_E_R_E_L": 0.078,
            "elastic_ratio_G_LR_E_L": 0.064,
            "elastic_ratio_G_LT_E_L": 0.061,
            "elastic_ratio_G_RT_E_L": 0.003,
            "poissons_ratio_LR": 0.372,
            "poissons_ratio_LT": 0.467,
            "poissons_ratio_RT": 0.435,
            "poissons_ratio_TR": 0.245,
            "poissons_ratio_RL": 0.040,
            "poissons_ratio_TL": 0.025,
            "shear_corrected_moe_GPa": 10.8 * 1.1
        }
    },
    {
        "name": "Spruce Wood (Green)",
        "source_url": "https://www.fpl.fs.usda.gov/documnts/fplgtr/fplgtr190/chapter_05.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 0.37,
        "tensile_strength_max": 39.0,
        "elastic_modulus": 8.5,
        "compressive_strength": 18.4,
        "hardness": "1600 N",
        "description": "Sitka spruce (Picea sitchensis). Green state.",
        "computational_properties": {
            "specific_gravity": 0.37,
            "work_to_max_load_kJ_m3": 43,
            "impact_bending_mm": 610,
            "compression_perp_kPa": 1900,
            "shear_parallel_kPa": 5200,
            "tension_perp_kPa": 1700,
            "tensile_strength_parallel_kPa": 59300,
            "shear_corrected_moe_GPa": 8.5 * 1.1
        }
    },
    {
        "name": "Teak Wood (Dry)",
        "source_url": "https://www.fpl.fs.usda.gov/documnts/fplgtr/fplgtr190/chapter_05.pdf, https://www.wood-database.com/teak/",
        "extraction_method": "Verified Source Datasheet",
        "density": 0.66, # Wood Database states SG 12% is 0.66 (avg dried weight 655 kg/m3).
        "tensile_strength_max": 100.7, # FPL
        "elastic_modulus": 10.7, # FPL
        "compressive_strength": 58.0, # FPL
        "hardness": "4400 N", # FPL
        "description": "Teak (Tectona grandis). 12% Moisture Content. Properties anchored to FPL, shrinkage and density sourced from Wood Database.",
        "computational_properties": {
            "work_to_max_load_kJ_m3": 83,
            "shear_parallel_kPa": 13000,
            "shrinkage_radial_pct": 2.6,
            "shrinkage_tangential_pct": 5.3,
            "shrinkage_volumetric_pct": 7.2,
            "shear_corrected_moe_GPa": 10.7 * 1.1
        }
    },
    {
        "name": "Teak Wood (Green)",
        "source_url": "https://www.fpl.fs.usda.gov/documnts/fplgtr/fplgtr190/chapter_05.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 0.55,
        "tensile_strength_max": 80.0,
        "elastic_modulus": 9.4,
        "compressive_strength": 41.1,
        "hardness": "4100 N",
        "description": "Teak (Tectona grandis). Green state. Note: Work to max load decreases on drying (92 -> 83).",
        "computational_properties": {
            "specific_gravity": 0.55,
            "work_to_max_load_kJ_m3": 92,
            "shear_parallel_kPa": 8900,
            "shear_corrected_moe_GPa": 9.4 * 1.1
        }
    },
    {
        "name": "Walnut Wood (Dry)",
        "source_url": "https://www.fpl.fs.usda.gov/documnts/fplgtr/fplgtr190/chapter_05.pdf, https://www.wood-database.com/black-walnut/",
        "extraction_method": "Verified Source Datasheet",
        "density": 0.55, # FPL 12% SG
        "tensile_strength_max": 101.0,
        "elastic_modulus": 11.6,
        "compressive_strength": 52.3,
        "hardness": "4500 N",
        "description": "Black walnut (Juglans nigra). 12% Moisture Content. Outlier: Highest μ_LT Poisson's ratio of any wood in FPL table.",
        "computational_properties": {
            "specific_gravity": 0.55,
            "work_to_max_load_kJ_m3": 74,
            "impact_bending_mm": 860,
            "compression_perp_kPa": 7000,
            "shear_parallel_kPa": 9400,
            "tension_perp_kPa": 4800,
            "elastic_ratio_E_T_E_L": 0.056,
            "elastic_ratio_E_R_E_L": 0.106,
            "elastic_ratio_G_LR_E_L": 0.085,
            "elastic_ratio_G_LT_E_L": 0.062,
            "elastic_ratio_G_RT_E_L": 0.021,
            "poissons_ratio_LR": 0.495,
            "poissons_ratio_LT": 0.632,
            "poissons_ratio_RT": 0.718,
            "poissons_ratio_TR": 0.367,
            "poissons_ratio_RL": 0.052,
            "poissons_ratio_TL": 0.036,
            "shrinkage_radial_pct": 5.5,
            "shrinkage_tangential_pct": 7.8,
            "shrinkage_volumetric_pct": 12.8,
            "shear_corrected_moe_GPa": 11.6 * 1.1
        }
    },
    {
        "name": "Walnut Wood (Green)",
        "source_url": "https://www.fpl.fs.usda.gov/documnts/fplgtr/fplgtr190/chapter_05.pdf",
        "extraction_method": "Verified Source Datasheet",
        "density": 0.51,
        "tensile_strength_max": 66.0,
        "elastic_modulus": 9.8,
        "compressive_strength": 29.6,
        "hardness": "4000 N",
        "description": "Black walnut (Juglans nigra). Green state. Note: Work to max load decreases on drying.",
        "computational_properties": {
            "specific_gravity": 0.51,
            "work_to_max_load_kJ_m3": 101,
            "impact_bending_mm": 940,
            "compression_perp_kPa": 3400,
            "shear_parallel_kPa": 8400,
            "tension_perp_kPa": 3900,
            "shear_corrected_moe_GPa": 9.8 * 1.1
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

print("Batch 4 update completed.")
