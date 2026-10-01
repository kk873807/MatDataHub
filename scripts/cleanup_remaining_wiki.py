import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# === 1. DELETE JUNK RECORDS ===
junk_names = [
    'DataSheet.aspx?MatGUID=035d2130b7f34d918e8d590659b85cb7',
    'MatWeb - The Online Materials Information Resource',
    'Unknown Material 9422',
    'Unknown Material',
]
for name in junk_names:
    res = supabase.table('materials').delete().eq('name', name).execute()
    print(f"Deleted junk: {name} ({len(res.data)} rows)")

# === 2. DELETE API INJECTION DUPLICATES ===
# These are duplicates of materials we already have with proper sources
api_dupes = [
    'Rene 41 (Aerospace Superalloy)',       # duplicate of Rene 41
    'Titanium Ti-6Al-4V (Aerospace Grade)', # duplicate of Titanium Grade 5 (Ti-6Al-4V)
    'Waspaloy (Aerospace Alloy)',           # duplicate of Waspaloy
    'White Cast Iron (Industrial Grade)',   # duplicate of White Cast Iron
]
for name in api_dupes:
    res = supabase.table('materials').delete().eq('name', name).execute()
    print(f"Deleted API dupe: {name} ({len(res.data)} rows)")

# === 3. FIX FAKE WIKIPEDIA URLS WITH REAL ONES ===
fixes = {
    'POM (Acetal Plastic)': {
        'url': 'https://en.wikipedia.org/wiki/Polyoxymethylene',
        'name': 'Wikipedia'
    },
    'PVC (Polyvinyl Chloride Plastic)': {
        'url': 'https://en.wikipedia.org/wiki/Polyvinyl_chloride',
        'name': 'Wikipedia'
    },
    'PTFE (Teflon Plastic)': {
        'url': 'https://en.wikipedia.org/wiki/Polytetrafluoroethylene',
        'name': 'Wikipedia'
    },
}
for name, info in fixes.items():
    res = supabase.table('materials').update({
        'source_url': info['url'],
        'source_name': info['name']
    }).eq('name', name).execute()
    print(f"Fixed URL: {name} -> {info['url']} ({len(res.data)} rows)")

# === 4. FINAL CHECK ===
remaining = supabase.table('materials').select('id', count='exact').ilike('source_url', '%wikipedia.org%').execute()
print(f"\nWikipedia URLs remaining: {remaining.count}")

total = supabase.table('materials').select('id', count='exact').execute()
print(f"Total materials in DB: {total.count}")
