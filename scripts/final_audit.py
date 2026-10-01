import os
from urllib.parse import urlparse
from collections import Counter
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Fetch ALL materials
all_mats = []
page = 0
while True:
    res = supabase.table('materials').select('id, name, source_url, source_name').range(page * 1000, (page + 1) * 1000 - 1).execute()
    if not res.data: break
    all_mats.extend(res.data)
    if len(res.data) < 1000: break
    page += 1

print(f"Total materials in database: {len(all_mats)}")

# Categorize by source type
categories = Counter()
domain_counts = Counter()
source_methods = Counter()

LOW_QUALITY = ['wikipedia.org', 'researchgate.net', 'sciencedirect.com', 'springer.com',
               'alibaba.com', 'aliexpress.com', 'made-in-china.com', 'indiamart.com',
               'quora.com', 'reddit.com', 'scribd.com', 'studocu.com']

for m in all_mats:
    url = (m.get('source_url') or '').strip()
    sname = (m.get('source_name') or '')
    
    if not url:
        categories['Empty/NULL'] += 1
    elif 'makeitfrom' in url.lower():
        categories['MakeItFrom (BAD)'] += 1
    elif 'materialsproject.org' in url.lower():
        categories['Materials Project'] += 1
    elif 'oqmd.org' in url.lower():
        categories['OQMD'] += 1
    elif 'kaggle.com' in url.lower():
        categories['Kaggle Dataset'] += 1
    else:
        domain = urlparse(url).netloc.lower().replace('www.', '')
        if any(lq in domain for lq in LOW_QUALITY):
            categories['Low-Quality Source'] += 1
        else:
            categories['Primary Source'] += 1
        domain_counts[domain] += 1
    
    if sname:
        source_methods[sname.split('(')[0].strip()] += 1

print("\n--- SOURCE URL BREAKDOWN ---")
for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
    pct = count / len(all_mats) * 100
    print(f"  {cat:30s}: {count:5d}  ({pct:.1f}%)")

print("\n--- TOP 20 DOMAINS (Primary Sources) ---")
for domain, count in domain_counts.most_common(20):
    print(f"  {domain:50s}: {count}")

print("\n--- EXTRACTION METHOD BREAKDOWN ---")
for method, count in source_methods.most_common(15):
    print(f"  {method:45s}: {count}")

# Check for any remaining low-quality
lq_remaining = []
for m in all_mats:
    url = (m.get('source_url') or '')
    try:
        domain = urlparse(url).netloc.lower()
        if any(lq in domain for lq in LOW_QUALITY):
            lq_remaining.append(m)
    except:
        pass

if lq_remaining:
    print(f"\n--- REMAINING LOW-QUALITY SOURCES ({len(lq_remaining)}) ---")
    for m in lq_remaining[:10]:
        print(f"  {m['id']}: {m['name'][:50]} -> {m['source_url'][:60]}")
else:
    print("\n[OK] Zero low-quality sources remaining!")
