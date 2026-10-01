
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Fetch ALL MatWeb links to analyze what's left
res = supabase.table('materials').select('id, source_url').ilike('source_url', '%matweb.com%').execute()

suspicious_links = set()
for m in res.data:
    url = m.get('source_url', '')
    if url:
        for link in url.split(','):
            link = link.strip()
            if 'matweb.com' in link:
                if 'DataSheet.aspx' not in link:
                    suspicious_links.add(link)

print(f'Total materials with matweb links: {len(res.data)}')
print('Suspicious MatWeb Links:')
for link in list(suspicious_links)[:20]:
    print(link)

