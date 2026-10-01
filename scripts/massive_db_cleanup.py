import os
import csv
from collections import defaultdict
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from supabase import create_client

# Setup
load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

print("Fetching all materials from the database...")
all_materials = []
page = 0
while True:
    res = supabase.table('materials').select('*').range(page*1000, (page+1)*1000 - 1).execute()
    if not res.data: break
    all_materials.extend(res.data)
    if len(res.data) < 1000: break
    page += 1

print(f"Total materials fetched: {len(all_materials)}")

# ==========================================
# PHASE 1: DEDUPLICATION
# ==========================================
print("\n--- PHASE 1: DEDUPLICATION ---")
name_groups = defaultdict(list)
for m in all_materials:
    name_key = str(m.get('name', '')).strip().lower()
    if name_key:
        name_groups[name_key].append(m)

ids_to_delete = []
for name_key, group in name_groups.items():
    if len(group) > 1:
        # Score materials based on how many non-null fields they have
        def score(mat):
            return sum(1 for v in mat.values() if v is not None and str(v).strip() != "")
        
        # Sort so the material with the most data is first
        sorted_group = sorted(group, key=lambda x: (score(x), x['id']), reverse=True)
        
        # Keep the best one, flag the rest for deletion
        for dup in sorted_group[1:]:
            ids_to_delete.append(dup['id'])

if ids_to_delete:
    print(f"Found {len(ids_to_delete)} exact name duplicates. Deleting the less complete versions...")
    # Delete in batches of 100
    for i in range(0, len(ids_to_delete), 100):
        batch = ids_to_delete[i:i+100]
        supabase.table('materials').delete().in_('id', batch).execute()
    print("Deduplication complete!")
    
    # Remove deleted items from our working list for Phase 2
    all_materials = [m for m in all_materials if m['id'] not in ids_to_delete]
else:
    print("No exact name duplicates found!")

# ==========================================
# PHASE 2: LINK VALIDATION
# ==========================================
print("\n--- PHASE 2: LINK VALIDATION ---")
print(f"Checking {len(all_materials)} links using 30 concurrent threads. This will take a few minutes...")

broken_links = []
# Mimic a standard browser to avoid basic blocks
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def check_url(mat):
    url = mat.get('source_url')
    if not url or not str(url).startswith('http'):
        return (mat, "Missing or Invalid URL Format")
    
    try:
        # 1. Try a fast HEAD request first
        res = requests.head(url, headers=headers, timeout=8, allow_redirects=True)
        
        # 2. If servers block HEAD requests (403, 405), fallback to GET
        if res.status_code >= 400:
            if res.status_code in [403, 405, 503]:
                res_get = requests.get(url, headers=headers, timeout=8, stream=True)
                if res_get.status_code >= 400:
                    return (mat, f"HTTP {res_get.status_code}")
                return (mat, "OK")
            return (mat, f"HTTP {res.status_code}")
            
        return (mat, "OK")
        
    except requests.exceptions.Timeout:
        return (mat, "Timeout")
    except requests.exceptions.ConnectionError:
        return (mat, "DNS / Connection Error")
    except Exception as e:
        return (mat, f"Error: {str(e)[:30]}")

completed = 0
# Use ThreadPoolExecutor to check URLs concurrently
with ThreadPoolExecutor(max_workers=30) as executor:
    futures = {executor.submit(check_url, m): m for m in all_materials}
    for future in as_completed(futures):
        mat, status = future.result()
        completed += 1
        
        if completed % 500 == 0:
            print(f"  Progress: {completed} / {len(all_materials)} checked...")
            
        if status != "OK":
            broken_links.append({
                'id': mat['id'],
                'name': mat['name'],
                'category': mat.get('category', ''),
                'source_url': mat.get('source_url', ''),
                'error_status': status
            })

if broken_links:
    csv_path = 'Broken_Links_Report.csv'
    # Sort so 404s (dead) and DNS errors show up first, followed by 403s (bot blocks)
    broken_links = sorted(broken_links, key=lambda x: x['error_status'])
    
    print(f"\nFound {len(broken_links)} problematic links. Saving report to {csv_path}...")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'category', 'source_url', 'error_status'])
        writer.writeheader()
        writer.writerows(broken_links)
    print("Link validation complete!")
else:
    print("All links are perfectly healthy!")

print("\nMassive database cleanup finished successfully!")
