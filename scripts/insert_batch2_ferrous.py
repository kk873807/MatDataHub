import os
import json
import re
import time
from dotenv import load_dotenv
from supabase import create_client
from firecrawl import FirecrawlApp
from google import genai
from google.genai import types

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
firecrawl_app = FirecrawlApp(api_key=os.environ.get('FIRECRAWL_API_KEY'))

with open('.env', 'r', encoding='utf-8') as f:
    env_text = f.read()
gemini_clients = [genai.Client(api_key=k) for k in re.findall(r'GEMINI_API_KEY.*?=([^\s]+)', env_text) if k]
gemini_client = gemini_clients[0] if gemini_clients else None

VALID_DB_COLUMNS = {
    'category','subcategory','name','density','tensile_strength_min','yield_strength_min',
    'elongation','hardness','elastic_modulus','thermal_conductivity','specific_heat',
    'melting_point_min','composition','description','source_url','source_name','is_verified'
}

batch_2 = [
    {"name": "AISI Nitronic 50 (XM-19) Stainless Steel", "cat": "Stainless Steel", "sub": "Austenitic Stainless Steel", "url": "https://www.azom.com/article.aspx?ArticleID=9201"},
    {"name": "AISI 405 Stainless Steel", "cat": "Stainless Steel", "sub": "Ferritic Stainless Steel", "url": None}, # MakeItFrom replaced
    {"name": "AISI 409 Stainless Steel", "cat": "Stainless Steel", "sub": "Ferritic Stainless Steel", "url": None}, # MakeItFrom replaced
    {"name": "AISI 434 Stainless Steel", "cat": "Stainless Steel", "sub": "Ferritic Stainless Steel", "url": None}, # MakeItFrom replaced
    {"name": "AISI 446 Stainless Steel", "cat": "Stainless Steel", "sub": "Ferritic Stainless Steel", "url": None}, # MakeItFrom replaced
    {"name": "2101 Duplex Stainless Steel (LDX 2101)", "cat": "Stainless Steel", "sub": "Duplex Stainless Steel", "url": "https://www.rolledalloys.com/wp-content/uploads/2022/07/LDX-2101_Data-sheet-rolled-alloys.pdf"}
]

def sanitize_float(value):
    if value is None: return None
    if isinstance(value, (int, float)): return float(value)
    if isinstance(value, str):
        m = re.search(r'-?\d+\.?\d*', value)
        if m: return float(m.group())
    if isinstance(value, dict):
        v = value.get('value')
        if v is not None: return float(v)
    return None

def extract_properties(markdown, name):
    schema = '{"density":null,"tensile_strength_min":null,"yield_strength_min":null,"elongation":null,"hardness":null,"elastic_modulus":null,"thermal_conductivity":null,"specific_heat":null,"melting_point_min":null,"composition":""}'
    prompt = f"System Instruction: Output JSON matching exactly: {schema}\n\nUser Task: Extract numerical properties for '{name}'. Return JSON ONLY matching schema. SI units. Strip units. Null if missing.\nTEXT: {markdown[:15000]}"
    
    r = gemini_client.models.generate_content(
        model="gemini-3.5-flash-lite", 
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.1)
    )
    return json.loads(r.text)

print("Processing Batch 2...")
for item in batch_2:
    print(f"\n[*] Processing: {item['name']}")
    url = item['url']
    md = ""
    
    if url:
        print(f"  Scraping provided URL: {url}")
        try:
            res = firecrawl_app.scrape_url(url)
            md = res.get('markdown', '') if isinstance(res, dict) else res.markdown
        except Exception as e:
            print(f"  Failed to scrape URL: {e}")
            url = None
            
    if not url:
        query = f"{item['name']} material properties datasheet -makeitfrom -wikipedia -alibaba"
        print(f"  Searching alternative: {query}")
        try:
            search_res = firecrawl_app.search(query)
            results = search_res.get('data', []) if isinstance(search_res, dict) else search_res
            for r in results[:3]:
                link = r.get('url') if isinstance(r, dict) else r.url
                if 'makeitfrom.com' in link: continue
                print(f"  Trying alternative URL: {link}")
                try:
                    scrape = firecrawl_app.scrape_url(link)
                    md = scrape.get('markdown', '') if isinstance(scrape, dict) else scrape.markdown
                    if md and len(md) > 100:
                        url = link
                        break
                except: continue
        except Exception as e:
            print(f"  Search failed: {e}")

    if not url or not md:
        print("  => FAILED: Could not retrieve markdown data.")
        continue
        
    print(f"  Extracting properties from {len(md)} chars of markdown...")
    try:
        data = extract_properties(md, item['name'])
        
        payload = {
            'category': item['cat'],
            'subcategory': item['sub'],
            'name': item['name'],
            'source_url': url,
            'source_name': "Verified Source",
            'is_verified': True
        }
        
        for k, v in data.items():
            if v is None or str(v).strip() == "" or str(v).strip() == "null": continue
            if k in ['density', 'tensile_strength_min', 'yield_strength_min', 'elastic_modulus', 'thermal_conductivity', 'specific_heat', 'melting_point_min', 'elongation']:
                s = sanitize_float(v)
                if s is not None: payload[k] = s
            else:
                payload[k] = v
                
        # Check if exists
        res = supabase.table('materials').select('id').eq('name', item['name']).execute()
        if res.data:
            supabase.table('materials').update(payload).eq('id', res.data[0]['id']).execute()
            print(f"  => Updated existing record! Fields populated: {len(payload)}")
        else:
            supabase.table('materials').insert(payload).execute()
            print(f"  => Inserted new record! Fields populated: {len(payload)}")
            
    except Exception as e:
        print(f"  => EXTRACTION/DB FAILED: {e}")
        
    time.sleep(3)
