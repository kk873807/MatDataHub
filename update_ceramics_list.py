
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

res = supabase.table("materials").select("name").eq("category", "Ceramic").execute()
current_names = [m["name"] for m in res.data]
current_names.sort()

with open(r"C:\Users\KISHAN\.gemini\antigravity\brain\eff86858-6371-4a19-a4ad-4c179410bba2\current_ceramics.md", "w", encoding="utf-8") as f:
    f.write("# Current Ceramic Materials in Database\n\n")
    f.write(f"The database currently holds {len(current_names)} distinct ceramic materials, including hundreds of complex multi-element crystalline compounds, optical glasses, and advanced structural ceramics.\n\n")
    f.write("## Full List\n\n")
    for name in current_names:
        f.write(f"- {name}\n")
        
print("Updated current_ceramics.md")

