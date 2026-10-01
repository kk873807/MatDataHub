import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

# Count remaining makeitfrom materials
res = supabase.table('materials').select('id, name, source_url').ilike('source_url', '%makeitfrom%').execute()
print(f"Remaining MakeItFrom targets in DB: {len(res.data)}")
for r in res.data[:15]:
    print(f"  {r['id']}: {r['name']}")
if len(res.data) > 15:
    print(f"  ... and {len(res.data)-15} more")
