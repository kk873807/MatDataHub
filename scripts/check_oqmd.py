import os
import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Find all OQMD materials
all_oqmd = []
page = 0
while True:
    res = supabase.table('materials').select('id, name, source_url').ilike('source_url', '%oqmd%').range(page * 1000, (page + 1) * 1000 - 1).execute()
    if not res.data:
        break
    all_oqmd.extend(res.data)
    if len(res.data) < 1000:
        break
    page += 1

print(f"Total OQMD materials in DB: {len(all_oqmd)}")

# Show sample URLs
unique_urls = set()
for m in all_oqmd[:10]:
    print(f"  {m['id']}: {m['name']}")
    print(f"    URL: {m['source_url']}")
    unique_urls.add(m['source_url'])

# Test if OQMD server is responding now
print(f"\n--- TESTING OQMD SERVER ---")
test_urls = list(unique_urls)[:3]
for url in test_urls:
    try:
        resp = requests.get(url, timeout=10, allow_redirects=True)
        print(f"  {url[:70]}...")
        print(f"    Status: {resp.status_code} | Size: {len(resp.text)} bytes")
    except Exception as e:
        print(f"  {url[:70]}...")
        print(f"    ERROR: {str(e)[:80]}")
