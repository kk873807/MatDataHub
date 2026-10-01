import os
import requests
from supabase import create_client
from dotenv import load_dotenv
import time

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

res = supabase.table('materials').select('id, name, source_url, source_name').ilike('source_url', '%wikipedia.org%').execute()

print(f"Found {len(res.data)} remaining Wikipedia URLs. Checking which are real...\n")

real_wiki = []
fake_wiki = []
junk_records = []

for r in res.data:
    name = r['name']
    url = r['source_url']
    source = r['source_name'] or ''
    rid = r['id']
    
    # Junk records that shouldn't exist at all
    if 'Unknown Material' in name or 'DataSheet.aspx' in name or name == 'MatWeb - The Online Materials Information Resource':
        junk_records.append(r)
        print(f"  JUNK: {name}")
        continue
    
    # Check if Wikipedia article actually exists
    try:
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True, timeout=10)
        if resp.status_code == 200 and 'does not have an article' not in resp.text and 'Wikipedia does not have an article' not in resp.text:
            real_wiki.append(r)
            print(f"  REAL: {name} -> {url}")
        else:
            fake_wiki.append(r)
            print(f"  FAKE: {name} -> {url} (status {resp.status_code})")
    except Exception as e:
        fake_wiki.append(r)
        print(f"  ERROR: {name} -> {url} ({e})")
    
    time.sleep(0.5)  # Be polite to Wikipedia

print(f"\n--- Summary ---")
print(f"Real Wikipedia articles: {len(real_wiki)}")
print(f"Fake Wikipedia URLs:     {len(fake_wiki)}")
print(f"Junk records to delete:  {len(junk_records)}")
print(f"\nReal articles (keep as-is):")
for r in real_wiki:
    print(f"  {r['name']}: {r['source_url']}")
print(f"\nFake articles (need replacement URL):")
for r in fake_wiki:
    print(f"  {r['name']}: {r['source_url']}")
print(f"\nJunk records (delete):")
for r in junk_records:
    print(f"  {r['name']}: {r['source_url']}")
