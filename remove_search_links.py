
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

print('Fetching all materials...')
offset = 0
count = 0
while True:
    res = supabase.table('materials').select('id, source_url').range(offset, offset+999).execute()
    if not res.data:
        break
    
    for m in res.data:
        urls = m['source_url']
        if not urls: continue
        
        # split by comma
        url_list = [u.strip() for u in urls.split(',')]
        
        # filter out search links
        clean_urls = []
        for u in url_list:
            if 'QuickText.aspx' in u or 'search.aspx' in u or 'sciencedirect.com/search' in u or 'search' in u.lower():
                continue
            clean_urls.append(u)
            
        new_url_string = ', '.join(clean_urls) if clean_urls else None
        
        if new_url_string != urls:
            # if empty, fallback to wikipedia or matweb home depending on category
            if not new_url_string:
                new_url_string = 'https://en.wikipedia.org/wiki/Steel' if 'Bainitic' in str(m) else None
                
            supabase.table('materials').update({'source_url': new_url_string}).eq('id', m['id']).execute()
            count += 1
            
    offset += 1000

print(f'Removed search links from {count} materials.')

