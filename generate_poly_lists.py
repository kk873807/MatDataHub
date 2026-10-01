
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# 1. Update current_polymers.md (NAMES ONLY)
res = supabase.table("materials").select("name").eq("category", "Polymer").execute()
db_polymers = sorted([m["name"] for m in res.data])

md_path_current = r"C:\Users\KISHAN\.gemini\antigravity\brain\eff86858-6371-4a19-a4ad-4c179410bba2\current_polymers.md"
with open(md_path_current, "w") as f:
    f.write("---\nsummary: \"A list of all polymer names currently in the database.\"\nuser_facing: true\nrequest_feedback: false\n---\n")
    f.write("# Current Polymer Database\n\n")
    for name in db_polymers:
        f.write(f"- {name}\n")

# 2. Comprehensive missing polymers list
# There are hundreds of standard base resins and unfilled variants.
missing = {
    "Commodity Thermoplastics": [
        "LDPE (Low-Density Polyethylene)",
        "LLDPE (Linear Low-Density Polyethylene)",
        "MDPE (Medium-Density Polyethylene)",
        "UHMWPE (Ultra-High-Molecular-Weight Polyethylene)",
        "PET (Polyethylene Terephthalate)",
        "PBT (Polybutylene Terephthalate)",
        "PS (Polystyrene, General Purpose)",
        "HIPS (High Impact Polystyrene)",
        "EPS (Expanded Polystyrene)",
        "PVC (Polyvinyl Chloride, Flexible)",
        "CPVC (Chlorinated Polyvinyl Chloride)",
        "EVA (Ethylene Vinyl Acetate)",
        "PLA (Polylactic Acid)"
    ],
    "Engineering Thermoplastics": [
        "PA 6 (Nylon 6)",
        "PA 11 (Nylon 11)",
        "PA 12 (Nylon 12)",
        "PA 46 (Nylon 46)",
        "PC/ABS (Polycarbonate/ABS Blend)",
        "PPE/PS (Polyphenylene Ether / Noryl)",
        "POM-H (Acetal Homopolymer / Delrin)",
        "POM-C (Acetal Copolymer / Celcon)",
        "SAN (Styrene Acrylonitrile)",
        "ASA (Acrylonitrile Styrene Acrylate)",
        "MABS (Methyl Methacrylate ABS)"
    ],
    "High-Performance & Specialty Polymers": [
        "PEI (Polyetherimide / Ultem)",
        "PPS (Polyphenylene Sulfide / Ryton)",
        "PAI (Polyamide-imide / Torlon)",
        "PI (Polyimide / Kapton / Vespel)",
        "LCP (Liquid Crystal Polymer)",
        "PES (Polyethersulfone)",
        "PSU (Polysulfone)",
        "PPSU (Polyphenylsulfone / Radel)",
        "PEKK (Polyetherketoneketone)",
        "PPA (Polyphthalamide)",
        "FEP (Fluorinated Ethylene Propylene)",
        "PFA (Perfluoroalkoxy)",
        "PVDF (Polyvinylidene Fluoride / Kynar)",
        "ETFE (Ethylene Tetrafluoroethylene / Tefzel)"
    ],
    "Thermosets": [
        "Epoxy (Unfilled)",
        "Epoxy (Glass Fiber Reinforced / FR4)",
        "Epoxy (Carbon Fiber Reinforced)",
        "PUR (Polyurethane, Rigid)",
        "PUR (Polyurethane, Flexible)",
        "Melamine Formaldehyde (MF)",
        "Urea Formaldehyde (UF)",
        "Vinyl Ester",
        "Unsaturated Polyester (UP)"
    ],
    "Elastomers & Rubbers": [
        "EPDM (Ethylene Propylene Diene Monomer)",
        "NBR (Nitrile Butadiene Rubber / Buna-N)",
        "HNBR (Hydrogenated Nitrile Butadiene Rubber)",
        "SBR (Styrene-Butadiene Rubber)",
        "FKM (Fluoroelastomer / Viton)",
        "FFKM (Perfluoroelastomer / Kalrez)",
        "IIR (Butyl Rubber)",
        "CSM (Chlorosulfonated Polyethylene / Hypalon)",
        "ACM (Polyacrylate Rubber)",
        "TPU (Thermoplastic Polyurethane)",
        "TPE (Thermoplastic Elastomer)",
        "TPV (Thermoplastic Vulcanizate / Santoprene)"
    ]
}

md_path_missing = r"C:\Users\KISHAN\.gemini\antigravity\brain\eff86858-6371-4a19-a4ad-4c179410bba2\missing_polymers.md"
with open(md_path_missing, "w") as f:
    f.write("---\nsummary: \"A comprehensive list of engineering and industrial polymers missing from the database.\"\nuser_facing: true\nrequest_feedback: false\n---\n")
    f.write("# Comprehensive Missing Polymers\n\n")
    f.write("Because the polymer industry does not use a numbering series like metals, this list represents every **major base chemical family** and **standard commercial grade** of plastic and rubber used in modern engineering and industrial manufacturing that is currently missing from your database.\n\n")
    f.write("*(Note: Including every single proprietary glass/carbon/mineral filled variant would result in tens of thousands of items, so this list focuses strictly on the foundational base polymers)*.\n\n")
    
    for category, items in missing.items():
        f.write(f"### {category}\n")
        for item in items:
            f.write(f"- {item}\n")
        f.write("\n")

print("Lists regenerated!")

