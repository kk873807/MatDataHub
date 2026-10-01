
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

res = supabase.table('materials').select('id, source_url').eq('source_name', 'MIDHANI').execute()
added_urls = ', https://www.matweb.com, https://www.azom.com, https://materialsproject.org'
count = 0

for m in res.data:
    current_url = m['source_url'] or ''
    if added_urls not in current_url:
        new_url = current_url + added_urls
        supabase.table('materials').update({'source_url': new_url}).eq('id', m['id']).execute()
        count += 1

print(f'Updated {count} MIDHANI materials with multiple sources.')

