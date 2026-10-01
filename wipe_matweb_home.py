
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Fetch ALL MatWeb links
res = supabase.table('materials').select('id, source_url').ilike('source_url', '%matweb.com%').execute()

bad_links = {'https://www.matweb.com', 'https://www.matweb.com/', 'http://www.matweb.com', 'http://www.matweb.com/'}
count = 0

for m in res.data:
    url_str = m.get('source_url', '')
    if not url_str:
        continue
        
    links = [l.strip() for l in url_str.split(',')]
    original_len = len(links)
    
    # Remove bad links
    good_links = [l for l in links if l not in bad_links]
    
    if len(good_links) != original_len:
        new_url_str = ', '.join(good_links) if good_links else None
        supabase.table('materials').update({'source_url': new_url_str}).eq('id', m['id']).execute()
        count += 1

print(f'Wiped generic MatWeb homepage links from {count} materials.')

