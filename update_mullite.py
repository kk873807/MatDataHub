
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

bad_url = "https://ceramics.net/wp-content/uploads/stc-material-property-chart-individual-silicates-mullite-01052021.pdf"
good_url = "https://ceramics.net/wp-content/uploads/stc-material-property-chart.pdf"
all_urls = "https://www.coorstek.com/en/materials/silicates/, " + good_url

supabase.table("materials").update({"source_url": all_urls}).eq("name", "Mullite").execute()
print("Updated Mullite URLs")

