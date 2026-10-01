
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

res = supabase.table("materials").select("name, extraction_method, source_url").eq("category", "Composite").order("name").execute()
materials = res.data

with open("current_composites.md", "w", encoding="utf-8") as f:
    f.write("# Current Composites in Database\n\n")
    f.write("| Material Name | Extraction Method | Source URLs |\n")
    f.write("|---|---|---|\n")
    for m in materials:
        name = m["name"]
        method = m.get("extraction_method") or "Unverified (AI Estimate / None)"
        url = m.get("source_url") or "None"
        # truncate long urls for table display
        if len(url) > 100:
            url = url[:97] + "..."
        f.write(f"| {name} | {method} | {url} |\n")

print(f"Exported {len(materials)} composites to current_composites.md")

