import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Paginate to get ALL materials
all_mats = []
page = 0
while True:
    res = supabase.table('materials').select('id, name, source_url, source_name').range(page * 1000, (page + 1) * 1000 - 1).execute()
    if not res.data:
        break
    all_mats.extend(res.data)
    if len(res.data) < 1000:
        break
    page += 1

print(f"Total materials in database: {len(all_mats)}")

# Categorize
makeitfrom = []
kaggle = []
materialsproject_bare = []
materialsproject_specific = []
primary = []
empty = []

for m in all_mats:
    url = (m.get('source_url') or '').strip()
    if not url:
        empty.append(m)
    elif 'makeitfrom' in url.lower():
        makeitfrom.append(m)
    elif 'kaggle' in url.lower():
        kaggle.append(m)
    elif url == 'https://materialsproject.org':
        materialsproject_bare.append(m)
    elif 'materialsproject.org' in url.lower():
        materialsproject_specific.append(m)
    else:
        primary.append(m)

print(f"\n--- SOURCE URL BREAKDOWN ---")
print(f"  [OK] Primary sources (replaced):       {len(primary)}")
print(f"  [KG] Kaggle dataset links:             {len(kaggle)}")
print(f"  [MP] MaterialsProject (specific):      {len(materialsproject_specific)}")
print(f"  [??] MaterialsProject (bare/generic):  {len(materialsproject_bare)}")
print(f"  [XX] MakeItFrom (still remaining):     {len(makeitfrom)}")
print(f"  [--] Empty/NULL:                       {len(empty)}")

# Show Kaggle samples
print(f"\n--- KAGGLE SAMPLES (first 5) ---")
for m in kaggle[:5]:
    print(f"  {m['id']}: {m['name']}")
    print(f"    URL: {m['source_url']}")
    print(f"    Source: {m.get('source_name', 'N/A')}")

# Show bare MP samples
print(f"\n--- BARE MATERIALSPROJECT SAMPLES (first 5) ---")
for m in materialsproject_bare[:5]:
    print(f"  {m['id']}: {m['name']}")
    print(f"    URL: {m['source_url']}")

# Show specific MP samples
print(f"\n--- SPECIFIC MATERIALSPROJECT SAMPLES (first 5) ---")
for m in materialsproject_specific[:5]:
    print(f"  {m['id']}: {m['name']}")
    print(f"    URL: {m['source_url']}")
