import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

def update_source(name, url, notes=None):
    source_name = "MakeItFrom" if "makeitfrom.com" in url else "MatWeb" if "matweb.com" in url else "Verified Source"
    if notes:
        source_name = f"{source_name} ({notes})"

    data = {"source_url": url, "source_name": source_name}
    print(f"Updating {name} -> {url} ({source_name})")
    supabase.table("materials").update(data).eq("name", name).execute()

# Note: Deletions already ran successfully for 1018 Annealed/Q&T.

# --- Base 1018-4340 Updates (Resuming from 1045 Annealed) ---
update_source("AISI 1045 Steel (Annealed)", "https://www.makeitfrom.com/material-properties/Annealed-and-Cold-Drawn-1045-Carbon-Steel", "Substituted: Annealed+Cold-Drawn")
update_source("AISI 1045 Steel (Cold Drawn)", "https://www.makeitfrom.com/material-properties/Cold-Drawn-1045-Carbon-Steel")
update_source("AISI 1045 Steel (Hot Rolled)", "https://www.makeitfrom.com/material-properties/Hot-Rolled-1045-Carbon-Steel")
update_source("AISI 1045 Steel (Quenched & Tempered)", "https://dl.asminternational.org/alloy-digest/article/20/10/CS-44/1863/AISI-1045Medium-Carbon-Steel", "ASM Alloy Digest CS-44")

update_source("AISI 4130 Steel", "https://www.makeitfrom.com/material-properties/SAE-AISI-4130-SCM430-G41300-Cr-Mo-Steel")
update_source("AISI 4130 Steel (Annealed)", "https://www.makeitfrom.com/material-properties/Annealed-4130-Cr-Mo-Steel")
update_source("AISI 4130 Steel (Cold Drawn)", "https://www.makeitfrom.com/material-properties/Cold-Finished-4130-Cr-Mo-Steel")
update_source("AISI 4130 Steel (Hot Rolled)", "https://www.makeitfrom.com/material-properties/Normalized-4130-Cr-Mo-Steel", "Substituted: Normalized")
update_source("AISI 4130 Steel (Quenched & Tempered)", "https://www.makeitfrom.com/material-properties/Quenched-and-Tempered-4130-Cr-Mo-Steel")

update_source("AISI 4140 Steel", "https://www.makeitfrom.com/material-properties/SAE-AISI-4140-SCM440-G41400-Cr-Mo-Steel")
update_source("AISI 4140 Steel (Annealed)", "https://www.makeitfrom.com/material-properties/Annealed-4140-Cr-Mo-Steel")
update_source("AISI 4140 Steel (Cold Drawn)", "https://www.makeitfrom.com/material-properties/Cold-Finished-4140-Cr-Mo-Steel")
update_source("AISI 4140 Steel (Hot Rolled)", "https://www.makeitfrom.com/material-properties/Normalized-4140-Cr-Mo-Steel", "Substituted: Normalized") 
update_source("AISI 4140 Steel (Quenched & Tempered)", "https://www.makeitfrom.com/material-properties/Quenched-and-Tempered-4140-Cr-Mo-Steel")

update_source("AISI 4340 Steel", "https://www.makeitfrom.com/material-properties/SAE-AISI-4340-SNCM439-G43400-Ni-Cr-Mo-Steel")
update_source("AISI 4340 Steel (Annealed)", "https://www.makeitfrom.com/material-properties/Annealed-4340-Ni-Cr-Mo-Steel")
update_source("AISI 4340 Steel (Cold Drawn)", "https://www.makeitfrom.com/material-properties/Cold-Finished-4340-Ni-Cr-Mo-Steel")
update_source("AISI 4340 Steel (Hot Rolled)", "https://www.makeitfrom.com/material-properties/Normalized-4340-Ni-Cr-Mo-Steel", "Substituted: Normalized")
update_source("AISI 4340 Steel (Quenched & Tempered)", "https://www.makeitfrom.com/material-properties/Quenched-and-Tempered-4340-Ni-Cr-Mo-Steel")

# --- 8620 Group Updates ---
update_source("AISI 8620 Steel", "https://www.makeitfrom.com/material-properties/SAE-AISI-8620-SNCM220-G86200-Ni-Cr-Mo-Steel")
update_source("AISI 8620 Steel (Annealed)", "https://www.makeitfrom.com/material-properties/Annealed-8620-Ni-Cr-Mo-Steel")
update_source("AISI 8620 Steel (Cold Drawn)", "https://www.makeitfrom.com/material-properties/Cold-Finished-8620-Ni-Cr-Mo-Steel")
update_source("AISI 8620 Steel (Hot Rolled)", "https://www.makeitfrom.com/material-properties/Normalized-8620-Ni-Cr-Mo-Steel", "Substituted: Normalized")
update_source("AISI 8620 Steel (Quenched & Tempered)", "https://matweb.com/search/datasheettext.aspx?matid=8298", "core properties, carburized 230C temper")

print("Database updates complete.")
