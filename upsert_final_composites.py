import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

materials = [
    {
        "name": "SiC/SiC (Ceramic Matrix Composite)",
        "category": "Composite",
        "subcategory": "Ceramic Matrix Composite",
        "source_url": "https://technology.nasa.gov/patent/LEW-TOPS-25, https://ntrs.nasa.gov/api/citations/20080006463/downloads/20080006463.pdf, https://www.ornl.gov/news/ceramic-matrix-composites-take-flight-leap-jet-engine",
        "extraction_method": "Verified Source Datasheet",
        "description": "Silicon Carbide fiber in a Silicon Carbide matrix. Replaces superalloys in LEAP jet engine shrouds. Withstands continuous operation up to 2400-2700F (1315-1480C).",
        "computational_properties": {
            "max_use_temperature_C": 1450,
            "application": "Gas turbine liners, vanes, engine shrouds"
        }
    },
    {
        "name": "C/SiC (Ceramic Matrix Composite)",
        "category": "Composite",
        "subcategory": "Ceramic Matrix Composite",
        "source_url": "https://ntrs.nasa.gov/api/citations/20020072848/downloads/20020072848.pdf, https://elib.dlr.de/92428, https://tf.uns.ac.rs/publikacije/PAC/pdf/PAC%2066%2001.pdf",
        "extraction_method": "Verified Source Datasheet",
        "thermal_conductivity": 135.0, # avg of 110-160
        "description": "Carbon fiber reinforced Silicon Carbide. Liquid silicon infiltrated for automotive brake discs (e.g. Porsche PCCB) due to thermal stability, low wear, and high thermal conductivity.",
        "computational_properties": {
            "thermal_conductivity_range_W_mK": "110 - 160",
            "application": "Automotive brake discs, high-temperature structural components"
        }
    },
    {
        "name": "Alumina/Alumina (Oxide/Oxide CMC)",
        "category": "Composite",
        "subcategory": "Ceramic Matrix Composite",
        "source_url": "https://etheses.bham.ac.uk/id/eprint/5924/, https://www.3m.com/3M/en_US/p/dc/v100778233/",
        "extraction_method": "Verified Source Datasheet",
        "tensile_strength_max": 146.0,
        "description": "Alumina fiber in Alumina matrix (e.g. Nextel 720/alumina). Electrically insulating and electromagnetically transparent. Continuous use up to 1200C. Ideal for high-temperature radomes.",
        "computational_properties": {
            "flexural_strength_MPa_min": 205,
            "interlaminar_shear_MPa_min": 12,
            "max_use_temperature_C": 1200
        }
    },
    {
        "name": "Nomex Honeycomb (Aramid Core)",
        "category": "Composite",
        "subcategory": "Core Material",
        "source_url": "https://hexcel.com/wp-content/uploads/2026/01/HexWeb_HRH10_DataSheet_us.pdf, https://hexcel.com/wp-content/uploads/2025/12/HexWeb_NonmetallicFlexCore_DataSheet_us.pdf",
        "extraction_method": "Verified Source Datasheet",
        "description": "Aramid fiber paper (Nomex) dipped in phenolic resin and expanded into honeycomb (e.g. Hexcel HRH-10). Excellent dielectric properties for radomes. Formable variants like Flex-Core available.",
        "computational_properties": {
            "dielectric": "Excellent",
            "max_temperature_F": 300
        }
    },
    {
        "name": "Aluminum Honeycomb (Core)",
        "category": "Composite",
        "subcategory": "Core Material",
        "source_url": "https://hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf, https://plascore.com/honeycomb-core/metallic/pamg-xr1-5052",
        "extraction_method": "Verified Source Datasheet",
        "description": "Aerospace-grade 5052 and 5056 aluminum honeycomb core. Used in aircraft floors, leading edges, helicopter rotor blades, and space payloads.",
        "computational_properties": {
            "density_range_pcf": "1.0 - 12.0",
            "alloy_grades": ["5052", "5056"]
        }
    },
    {
        "name": "Rohacell (PMI) Core",
        "category": "Composite",
        "subcategory": "Core Material",
        "source_url": "https://products.evonik.com/assets/35/22/ROHACELL_HERO_2022_April_EN_243522.pdf, https://products.evonik.com/assets/23/50/ROHACELL_WF_and_WF_HT_May_2026_EN_Asset_4252350.pdf",
        "extraction_method": "Verified Source Datasheet",
        "description": "Polymethacrylimide (PMI) rigid foam core (e.g. Rohacell HERO, WF-HT). High compressive strength for its density. Used in radomes and surface impact zones. Creep resistant up to 190C.",
        "computational_properties": {
            "density_range_kg_m3": "52 - 205",
            "compressive_strength_range_MPa": "0.6 - 7.1",
            "creep_resistance_temp_C": 190
        }
    },
    {
        "name": "MDF (Medium Density Fiberboard)",
        "category": "Composite",
        "subcategory": "Engineered Wood",
        "source_url": "https://www.compositepanel.org/products/medium-density-fiberboard/, https://wfs.swst.org/index.php/wfs/article/view/298",
        "extraction_method": "Verified Source Datasheet",
        "description": "Medium Density Fiberboard standard to ANSI A208.2. Density varies by panel specification, affecting shear and elastic moduli.",
        "computational_properties": {
            "density_range_kg_m3": "540 - 800",
            "standard": "ANSI A208.2"
        }
    },
    {
        "name": "OSB (Oriented Strand Board)",
        "category": "Composite",
        "subcategory": "Engineered Wood",
        "source_url": "https://apawood.org/osb, https://cwc.ca/wp-content/uploads/2019/03/Oriented-Strand-Board-OSB-Grades-.pdf",
        "extraction_method": "Verified Source Datasheet",
        "description": "Oriented Strand Board. Structural engineered wood panel formed by compressing layers of wood strands with adhesives (e.g. CSA O325).",
        "computational_properties": {
            "standard": "CSA O325"
        }
    },
    {
        "name": "Glulam (Glued Laminated Timber)",
        "category": "Composite",
        "subcategory": "Engineered Wood",
        "source_url": "https://awc.org/wp-content/uploads/2021/10/AWC_NDS2018-withCommentary_20200827_AWCWebsite_Chapter05.pdf, https://www.hasslacher.com/data/_dateimanager/broschuere/HNT0213_US_202002_Glulam.pdf",
        "extraction_method": "Verified Source Datasheet",
        "elastic_modulus": 12.4, # 1.8M psi
        "tensile_strength_max": 16.5, # 2400 psi bending
        "description": "Glued Laminated Timber per ANSI A190.1. Displayed values are for 24F-1.8E design class (2,400 psi bending stress, 1.8M psi modulus).",
        "computational_properties": {
            "bending_stress_psi": 2400,
            "modulus_of_elasticity_psi": 1800000,
            "design_class": "24F-1.8E"
        }
    },
    {
        "name": "Concrete (Steel Reinforced)",
        "category": "Composite",
        "subcategory": "Structural Composite",
        "source_url": "https://www.fhwa.dot.gov/publications/research/infrastructure/bridge/05056/chapt3c.cfm, https://rosap.ntl.bts.gov/view/dot/35984/dot_35984_DS1.pdf",
        "extraction_method": "Verified Source Datasheet",
        "description": "Standard steel-reinforced concrete for structural infrastructure.",
        "computational_properties": {
            "cte_range_per_F": "3.0e-6 - 8.0e-6"
        }
    },
    {
        "name": "UHPC (Ultra-High Performance Concrete)",
        "category": "Composite",
        "subcategory": "Structural Composite",
        "source_url": "https://www.fhwa.dot.gov/publications/research/infrastructure/structures/06103/06103.pdf, https://www.fhwa.dot.gov/publications/research/infrastructure/structures/14084/14084.pdf",
        "extraction_method": "Verified Source Datasheet",
        "compressive_strength": 193.0,
        "tensile_strength_max": 9.0,
        "elastic_modulus": 52.4,
        "description": "Ultra-High Performance Concrete per FHWA definition (compressive > 150 MPa). Typical mix includes steel fibers at 6.2% by weight.",
        "computational_properties": {
            "post_cracking_tensile_strength_MPa_min": 5.0,
            "steel_fiber_loading_wt_pct": 6.2
        }
    },
    {
        "name": "CNT / Epoxy (Carbon Nanotube Composite)",
        "category": "Composite",
        "subcategory": "Nanocomposite",
        "source_url": "https://khazna.ku.ac.ae/en/publications/effects-of-carbon-nanotube-alignment-on-electrical-and-mechanical/",
        "extraction_method": "Verified Source Datasheet",
        "description": "Carbon Nanotube / Epoxy nanocomposite. Aligning CNTs drastically lowers electrical percolation threshold (e.g. 0.0031 vol% vs 0.034 vol% random) and increases modulus and fracture toughness.",
        "computational_properties": {
            "percolation_threshold_aligned_vol_pct": 0.0031,
            "variance": "Highly dependent on CNT alignment and dispersion."
        }
    },
    {
        "name": "Graphene / Polymer Nanocomposite",
        "category": "Composite",
        "subcategory": "Nanocomposite",
        "source_url": "https://www2.mdpi.com/2073-4360/9/9/437, https://arxiv.org/pdf/2101.09063",
        "extraction_method": "Verified Source Datasheet",
        "description": "Graphene-infused polymer composite. Significantly enhances thermal and electrical conductivity over neat polymers.",
        "computational_properties": {
            "variance": "Performance highly sensitive to volume fraction and dispersion."
        }
    },
    {
        "name": "Buckypaper / Resin Composite",
        "category": "Composite",
        "subcategory": "Nanocomposite",
        "source_url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7696086, https://pmc.ncbi.nlm.nih.gov/articles/PMC5245188",
        "extraction_method": "Verified Source Datasheet",
        "thermal_conductivity": 74.0, # avg 65 - 83
        "description": "Buckypaper infused with resin (epoxy/PDMS/Parmax). Infusion dramatically increases modulus (82%) and strength (194%) over raw buckypaper.",
        "computational_properties": {
            "thermal_conductivity_range_W_mK": "65 - 83",
            "electrical_conductivity_S_cm_approx": 700
        }
    }
]

print("Upserting Final Composite Batch...")
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
