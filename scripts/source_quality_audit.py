import os
from supabase import create_client
from dotenv import load_dotenv
from collections import Counter

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Fetch all materials
all_data = []
page = 0
page_size = 1000
while True:
    res = supabase.table('materials').select('name, source_url, source_name').range(page * page_size, (page + 1) * page_size - 1).execute()
    if not res.data:
        break
    all_data.extend(res.data)
    if len(res.data) < page_size:
        break
    page += 1

print(f"Total materials: {len(all_data)}\n")

# Categorize by source quality
categories = {
    'makeitfrom': [],       # Dedicated property page per material - GOOD
    'matweb': [],           # Dedicated datasheet per material - GOOD
    'kaggle': [],           # Dataset landing page, no per-material view - BAD
    'wikipedia': [],        # General article, may or may not have properties - BAD
    'oqmd': [],             # Specific entry page - OK
    'osti_mp': [],          # Materials Project / OSTI - OK (computed data page)
    'manufacturer_pdf': [], # Mill datasheets - GOOD
    'other_good': [],       # Other verified sources with property data
    'unknown': [],          # Can't classify
}

for r in all_data:
    url = r['source_url'] or ''
    sn = r['source_name'] or ''
    
    if 'makeitfrom.com' in url:
        categories['makeitfrom'].append(r)
    elif 'matweb.com' in url:
        categories['matweb'].append(r)
    elif 'kaggle.com' in url:
        categories['kaggle'].append(r)
    elif 'wikipedia.org' in url:
        categories['wikipedia'].append(r)
    elif 'oqmd.org' in url:
        categories['oqmd'].append(r)
    elif 'osti.gov' in url or 'materialsproject.org' in url:
        categories['osti_mp'].append(r)
    elif any(x in url for x in ['.pdf', 'haynesintl', 'specialmetals', 'atimaterials',
                                  'outokumpu', 'rolledalloys', 'bibusmetals', 'upmet',
                                  'wood-database', 'leverrefluore', 'schott.com',
                                  'fwmetals', 'elgiloy', 'concast']):
        categories['manufacturer_pdf'].append(r)
    elif url:
        categories['other_good'].append(r)
    else:
        categories['unknown'].append(r)

print("=== SOURCE QUALITY AUDIT ===\n")
print(f"{'Category':<25s} {'Count':>6s}  {'Trust Level'}")
print("-" * 60)
print(f"{'MakeItFrom (per-material)':25s} {len(categories['makeitfrom']):6d}  HIGH - Properties on landing page")
print(f"{'MatWeb (per-datasheet)':25s} {len(categories['matweb']):6d}  HIGH - Properties on landing page")
print(f"{'Manufacturer PDFs':25s} {len(categories['manufacturer_pdf']):6d}  HIGH - Mill datasheet with properties")
print(f"{'OQMD (per-entry)':25s} {len(categories['oqmd']):6d}  MEDIUM - Computed properties shown")
print(f"{'OSTI/Materials Project':25s} {len(categories['osti_mp']):6d}  MEDIUM - Computed data page")
print(f"{'Other verified':25s} {len(categories['other_good']):6d}  VARIES - Needs review")
print(f"{'Kaggle (dataset page)':25s} {len(categories['kaggle']):6d}  LOW - No per-material view")
print(f"{'Wikipedia (general)':25s} {len(categories['wikipedia']):6d}  LOW - General article")
print(f"{'Unknown/empty':25s} {len(categories['unknown']):6d}  NONE")
print("-" * 60)

trustworthy = len(categories['makeitfrom']) + len(categories['matweb']) + len(categories['manufacturer_pdf']) + len(categories['oqmd']) + len(categories['osti_mp'])
needs_work = len(categories['kaggle']) + len(categories['wikipedia'])
print(f"\nTrustworthy (properties on page): {trustworthy}")
print(f"Needs better source:              {needs_work}")
print(f"Other (needs review):             {len(categories['other_good'])}")

# Show a sample of 'other_good' to understand what's in there
print(f"\n=== SAMPLE 'other_good' sources ===")
source_domains = Counter()
for r in categories['other_good']:
    url = r['source_url']
    try:
        domain = url.split('/')[2]
    except:
        domain = url
    source_domains[domain] += 1

for domain, count in source_domains.most_common(20):
    print(f"  {domain}: {count}")
