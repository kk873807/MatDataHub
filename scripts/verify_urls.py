import os
import csv
import time
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
from supabase import create_client
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Domains that are considered non-primary or low quality for a materials database
LOW_QUALITY_DOMAINS = [
    'wikipedia.org', 'researchgate.net', 'sciencedirect.com', 'springer.com', # Papers/Abstracts
    'alibaba.com', 'aliexpress.com', 'made-in-china.com', 'indiamart.com',    # Shopping/B2B directories
    'quora.com', 'reddit.com', 'scribd.com', 'studocu.com'                    # UGC / Document sharing
]

print("="*60)
print("[*] DATABASE URL DEEP SCANNER")
print("="*60)

# 1. Fetch all materials
print("Fetching materials from database...")
all_materials = []
page = 0
while True:
    res = supabase.table('materials').select('id, name, source_url').range(page * 1000, (page + 1) * 1000 - 1).execute()
    if not res.data: break
    all_materials.extend(res.data)
    if len(res.data) < 1000: break
    page += 1

print(f"Total materials fetched: {len(all_materials)}")

# 2. Filter out known bulk datasets (MaterialsProject, Kaggle, OQMD)
target_materials = []
unique_urls = set()

for m in all_materials:
    url = (m.get('source_url') or '').strip()
    if not url:
        continue
    url_lower = url.lower()
    
    # Skip known bulk datasets
    if 'materialsproject.org' in url_lower or 'oqmd.org' in url_lower or 'kaggle.com' in url_lower:
        continue
        
    target_materials.append(m)
    unique_urls.add(url)

print(f"Materials to verify (excluding MP/OQMD/Kaggle): {len(target_materials)}")
print(f"Unique URLs to test: {len(unique_urls)}")

# 3. Check for low-quality domains
print("\n--- CHECKING FOR LOW-QUALITY / NON-PRIMARY SOURCES ---")
low_quality_found = []
for m in target_materials:
    url = m['source_url']
    try:
        domain = urlparse(url).netloc.lower()
        if any(bad in domain for bad in LOW_QUALITY_DOMAINS):
            low_quality_found.append(m)
    except:
        pass

if low_quality_found:
    print(f"[!] Found {len(low_quality_found)} materials with low-quality sources:")
    for m in low_quality_found[:10]:
        print(f"  {m['id']} | {m['name']} -> {m['source_url'][:60]}...")
    if len(low_quality_found) > 10: print(f"  ...and {len(low_quality_found)-10} more.")
else:
    print("[OK] No low-quality or non-primary domains detected!")

# 4. Concurrently check URL health
print("\n--- PINGING URLs FOR DEAD LINKS (404, Timeouts, etc.) ---")
def check_url(url):
    try:
        # Some sites block default python requests user-agent
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers, timeout=10, allow_redirects=True, stream=True)
        return url, res.status_code
    except requests.exceptions.Timeout:
        return url, "TIMEOUT"
    except requests.exceptions.ConnectionError:
        return url, "CONNECTION_ERROR"
    except Exception as e:
        return url, "ERROR"

dead_links = []
start_time = time.time()

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(check_url, url): url for url in unique_urls}
    
    completed = 0
    for future in as_completed(futures):
        url, status = future.result()
        completed += 1
        
        if completed % 50 == 0 or completed == len(unique_urls):
            print(f"  Progress: {completed}/{len(unique_urls)} URLs checked...")
            
        if str(status) != '200' and str(status) != '403':  # 403 usually means anti-bot (Cloudflare), link is likely alive
            dead_links.append((url, status))

print(f"\nScan completed in {time.time() - start_time:.1f} seconds.")

# 5. Map dead URLs back to materials
dead_materials = []
dead_url_dict = {url: status for url, status in dead_links}

for m in target_materials:
    if m['source_url'] in dead_url_dict:
        m['error'] = dead_url_dict[m['source_url']]
        dead_materials.append(m)

# 6. Report
if dead_materials:
    print(f"\n[FAILED] FOUND {len(dead_materials)} MATERIALS WITH BROKEN/DEAD LINKS:")
    
    with open('dead_links_report.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Material Name', 'Error/Status', 'URL'])
        for m in dead_materials:
            writer.writerow([m['id'], m['name'], m['error'], m['source_url']])
            
    # Print a sample
    for m in dead_materials[:10]:
        print(f"  [{m['error']}] {m['name']} -> {m['source_url'][:60]}")
    if len(dead_materials) > 10:
        print(f"  ... Full list saved to 'dead_links_report.csv'")
else:
    print("\n[OK] All URLs returned healthy HTTP status codes!")

