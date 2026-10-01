
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

res = supabase.table("materials").select("name, yield_strength_min, tensile_strength_min").eq("category", "Polymer").execute()
db_polymers = [m["name"] for m in res.data]
db_polymers.sort()

# Write current polymers to artifact
md_path_current = r"C:\Users\KISHAN\.gemini\antigravity\brain\eff86858-6371-4a19-a4ad-4c179410bba2\current_polymers.md"
with open(md_path_current, "w") as f:
    f.write("---\nsummary: \"A list of all polymer materials currently in the database.\"\nuser_facing: true\nrequest_feedback: false\n---\n")
    f.write("# Current Polymer Database\n\n")
    f.write("| Material Name | Yield Strength | Tensile Strength |\n")
    f.write("|---------------|----------------|------------------|\n")
    for m in res.data:
        ys = m.get("yield_strength_min") or "N/A"
        ts = m.get("tensile_strength_min") or "N/A"
        f.write(f"| {m['name']} | {ys} | {ts} |\n")

# Define major missing polymers
# We know the DB has ABS, PETG, HDPE, Natural Rubber, Neoprene, Nylon 6/6, PEEK, POM, PTFE, PVC, Phenolic, Polycarbonate, PMMA, PP, Silicone.
missing = [
    "LDPE (Low-Density Polyethylene)",
    "LLDPE (Linear Low-Density Polyethylene)",
    "UHMWPE (Ultra-High-Molecular-Weight Polyethylene)",
    "PET (Polyethylene Terephthalate)",
    "PS (Polystyrene, General Purpose)",
    "HIPS (High Impact Polystyrene)",
    "PUR (Polyurethane)",
    "TPU (Thermoplastic Polyurethane)",
    "Epoxy (Unfilled)",
    "Epoxy (Carbon Fiber Reinforced)",
    "PA 12 (Nylon 12)",
    "PA 6 (Nylon 6)",
    "PPS (Polyphenylene Sulfide)",
    "PEI (Polyetherimide / Ultem)",
    "PAI (Polyamide-imide / Torlon)",
    "PI (Polyimide / Kapton)",
    "FEP (Fluorinated Ethylene Propylene)",
    "PVDF (Polyvinylidene Fluoride)",
    "EPDM Rubber",
    "Nitrile Rubber (NBR)",
    "SBR (Styrene-Butadiene Rubber)",
    "FKM (Viton / Fluoroelastomer)"
]

md_path_missing = r"C:\Users\KISHAN\.gemini\antigravity\brain\eff86858-6371-4a19-a4ad-4c179410bba2\missing_polymers.md"
with open(md_path_missing, "w") as f:
    f.write("---\nsummary: \"A list of major industrial polymers missing from the database.\"\nuser_facing: true\nrequest_feedback: false\n---\n")
    f.write("# Missing Industrial Polymers\n\n")
    f.write("Unlike Aluminum alloys, polymers do not use a 1000-9000 numerical series classification system. Instead, they are categorized by families (Thermoplastics, Thermosets, Elastomers) and chemical acronyms (PE, PP, PVC, etc.).\n\n")
    f.write("Based on what is currently in your database, here are the most critical industrial and commercial polymers you are missing:\n\n")
    
    f.write("### Commodity Plastics\n")
    for p in missing[:6]:
        f.write(f"- {p}\n")
    
    f.write("\n### Engineering & High-Performance Plastics\n")
    for p in missing[6:18]:
        f.write(f"- {p}\n")
        
    f.write("\n### Elastomers & Rubbers\n")
    for p in missing[18:]:
        f.write(f"- {p}\n")

print("Generated both lists!")

