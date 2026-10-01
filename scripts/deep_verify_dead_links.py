import csv
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================
# Step 1: Load dead links and filter out single-element materials
# ============================================================
csv_path = 'Genuinely_Dead_Links.csv'
all_rows = []
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        all_rows.append(row)

print(f"Total dead links loaded: {len(all_rows)}")

# Single-element symbols and names to exclude
ELEMENT_SYMBOLS = {
    'H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar',
    'K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr',
    'Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe',
    'Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu',
    'Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn',
    'Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No','Lr',
    'Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Cn','Nh','Fl','Mc','Lv','Ts','Og'
}
# Also catch binary/ternary computational compounds like SiP, GaAs etc.
COMPUTATIONAL_CATEGORIES = {'Computational Material'}

ELEMENT_NAMES = {
    'hydrogen','helium','lithium','beryllium','boron','carbon','nitrogen','oxygen','fluorine','neon',
    'sodium','magnesium','aluminum','aluminium','silicon','phosphorus','sulfur','chlorine','argon',
    'potassium','calcium','scandium','titanium','vanadium','chromium','manganese','iron','cobalt',
    'nickel','copper','zinc','gallium','germanium','arsenic','selenium','bromine','krypton',
    'rubidium','strontium','yttrium','zirconium','niobium','molybdenum','technetium','ruthenium',
    'rhodium','palladium','silver','cadmium','indium','tin','antimony','tellurium','iodine','xenon',
    'cesium','barium','lanthanum','cerium','praseodymium','neodymium','promethium','samarium',
    'europium','gadolinium','terbium','dysprosium','holmium','erbium','thulium','ytterbium',
    'lutetium','hafnium','tantalum','tungsten','rhenium','osmium','iridium','platinum','gold',
    'mercury','thallium','lead','bismuth','polonium','astatine','radon','francium','radium',
    'actinium','thorium','protactinium','uranium','neptunium','plutonium'
}

def is_single_element(name, category):
    """Check if a material is a single element or computational formula."""
    # Exclude entire "Computational Material" category
    if category in COMPUTATIONAL_CATEGORIES:
        return True
    # Exact element symbol match (e.g. "Lu", "Ne", "Er")
    if name.strip() in ELEMENT_SYMBOLS:
        return True
    # Exact element name match (e.g. "Iron", "Copper")
    if name.strip().lower() in ELEMENT_NAMES:
        return True
    return False

filtered_rows = []
removed_count = 0
for row in all_rows:
    if is_single_element(row['name'], row.get('category', '')):
        removed_count += 1
    else:
        filtered_rows.append(row)

print(f"Removed {removed_count} single-element / computational materials.")
print(f"Remaining to deep-verify: {len(filtered_rows)}")

# ============================================================
# Step 2: Deep re-verification with full GET requests
# ============================================================
print(f"\n--- DEEP VERIFICATION (full GET, retries, longer timeout) ---")
print(f"Checking {len(filtered_rows)} URLs with 15 concurrent threads...")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

def deep_check_url(row):
    url = row.get('source_url', '')
    if not url or not str(url).startswith('http'):
        return (row, "Missing/Invalid URL")

    for attempt in range(3):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True, stream=True)
            # Read first 1KB to confirm the server actually responds with content
            content_start = resp.raw.read(1024)
            resp.close()

            if resp.status_code < 400:
                return (row, "OK")
            elif resp.status_code == 403:
                return (row, "OK (403 bot-block)")
            elif resp.status_code == 429:
                return (row, "OK (429 rate-limit)")
            else:
                if attempt < 2:
                    time.sleep(2)
                    continue
                return (row, f"HTTP {resp.status_code}")

        except requests.exceptions.Timeout:
            if attempt < 2:
                time.sleep(2)
                continue
            return (row, "Timeout (3 retries)")
        except requests.exceptions.ConnectionError as e:
            err_str = str(e)
            if 'NameResolutionError' in err_str or 'getaddrinfo failed' in err_str:
                return (row, "DNS Dead")
            if attempt < 2:
                time.sleep(2)
                continue
            return (row, "Connection Error")
        except Exception as e:
            return (row, f"Error: {str(e)[:40]}")

    return (row, "Failed after 3 retries")

confirmed_dead = []
rescued = 0
completed = 0

with ThreadPoolExecutor(max_workers=15) as executor:
    futures = {executor.submit(deep_check_url, r): r for r in filtered_rows}
    for future in as_completed(futures):
        row, status = future.result()
        completed += 1

        if completed % 50 == 0:
            print(f"  Progress: {completed} / {len(filtered_rows)} deep-checked...")

        if status.startswith("OK"):
            rescued += 1
        else:
            row_copy = dict(row)
            row_copy['error_status'] = status
            confirmed_dead.append(row_copy)

print(f"\nDeep verification complete!")
print(f"  Rescued (actually alive): {rescued}")
print(f"  Confirmed dead: {len(confirmed_dead)}")

# ============================================================
# Step 3: Output fresh CSV
# ============================================================
output_path = 'Confirmed_Dead_Links.csv'
confirmed_dead.sort(key=lambda x: x['error_status'])

with open(output_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(confirmed_dead)

print(f"\nFresh CSV saved to: {output_path}")

# Summary by error type
from collections import Counter
err_counts = Counter(r['error_status'] for r in confirmed_dead)
print("\n=== Error Breakdown ===")
for err, count in err_counts.most_common():
    print(f"  {count:4d} : {err}")

domain_counts = Counter()
for r in confirmed_dead:
    url = r.get('source_url', '')
    try:
        domain = url.split('/')[2]
    except:
        domain = url
    domain_counts[domain] += 1

print("\n=== Top Dead Domains ===")
for dom, count in domain_counts.most_common(10):
    print(f"  {count:4d} : {dom}")
