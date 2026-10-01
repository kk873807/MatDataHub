"""Fix the final 3 low-quality sources."""
import os, json, re, time, itertools, warnings
warnings.filterwarnings('ignore')
from supabase import create_client
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from groq import Groq
from google import genai
from google.genai import types

load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
firecrawl_app = FirecrawlApp(api_key=os.environ.get('FIRECRAWL_API_KEY'))

with open('.env', 'r', encoding='utf-8') as f:
    env_text = f.read()
groq_clients = [Groq(api_key=k) for k in re.findall(r'GROQ_API_KEY.*?=([^\s]+)', env_text) if k]
gemini_clients = [genai.Client(api_key=k) for k in re.findall(r'GEMINI_API_KEY.*?=([^\s]+)', env_text) if k]
gemini_cycle = itertools.cycle(gemini_clients) if gemini_clients else None

VALID_DB_COLUMNS = {
    'category','subcategory','grade','standard','density','tensile_strength_min','tensile_strength_max',
    'yield_strength_min','yield_strength_max','elongation','hardness','elastic_modulus',
    'thermal_conductivity','specific_heat','melting_point_min','melting_point_max','max_service_temp',
    'cost_per_kg_min','cost_per_kg_max','cost_currency','applications','equivalent_grades',
    'composition','description','source_url','source_name','extraction_method','is_verified',
}
FLOAT_COLUMNS = {
    'density','tensile_strength_min','tensile_strength_max','yield_strength_min','yield_strength_max',
    'elongation','elastic_modulus','thermal_conductivity','specific_heat','melting_point_min',
    'melting_point_max','max_service_temp','cost_per_kg_min','cost_per_kg_max',
}
BAD_DOMAINS = ['makeitfrom.com','wikipedia.org','researchgate.net','sciencedirect.com','kaggle.com',
    'ccsteels.com','suppliersonline.com','alibaba.com','scribd.com','springer.com','studocu.com']

TARGET_IDS = [10433, 575, 11051]

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

def search_and_scrape(material_name):
    queries = [
        f"{material_name} material properties datasheet -makeitfrom -wikipedia -scribd -springer",
        f"site:azom.com OR site:matweb.com OR site:fabdigit.com {material_name}",
    ]
    paren = re.search(r'\(([^)]+)\)', material_name)
    if paren:
        queries.insert(1, f"{paren.group(1).split(',')[0].strip()} alloy properties datasheet")
    
    for qi, query in enumerate(queries, 1):
        print(f"    Query {qi}/{len(queries)}: {query[:80]}...")
        try:
            result = firecrawl_app.search(query)
            results = result if isinstance(result, list) else result.get('data', []) if isinstance(result, dict) else getattr(result, 'web', [])
            for r in results[:3]:
                link = getattr(r, 'url', None) or (r.get('url') if isinstance(r, dict) else None)
                if not link or any(b in link.lower() for b in BAD_DOMAINS): continue
                print(f"    Trying: {link[:80]}...")
                try:
                    scrape = firecrawl_app.scrape_url(link)
                    md = scrape.markdown if hasattr(scrape, 'markdown') else scrape.get('markdown','') if isinstance(scrape, dict) else str(scrape)
                    if md and len(md) >= 50:
                        print(f"    Scraped OK ({len(md)} chars)")
                        pub = "MatWeb" if "matweb" in link else "AZoM" if "azom" in link else "Primary Web Source"
                        return link, pub, md
                except: continue
        except Exception as e:
            print(f"    Search failed: {str(e)[:50]}")
        time.sleep(3)
    return None, None, None

def extract(markdown, material_name):
    prompt = f"Extract properties for '{material_name}'. Return JSON only. Numbers only (no units). SI units. Null if missing.\nTEXT: {markdown[:12000]}"
    schema = '{"density":null,"tensile_strength_min":null,"yield_strength_min":null,"elongation":null,"hardness":null,"elastic_modulus":null,"thermal_conductivity":null,"specific_heat":null,"melting_point_min":null,"melting_point_max":null,"category":null,"subcategory":null}'
    
    if groq_clients:
        try:
            r = groq_clients[0].chat.completions.create(
                messages=[{"role":"system","content":f"Output JSON matching: {schema}"},{"role":"user","content":prompt}],
                model="qwen/qwen3.8-27b", response_format={"type":"json_object"}, temperature=0.1, timeout=30)
            data = json.loads(r.choices[0].message.content)
            data["extraction_method"] = "Groq Final Fix"
            print("    Groq OK!")
            return data
        except: pass
    
    if gemini_cycle:
        for model in ['gemini-3.6-flash','gemini-3.5-flash-lite']:
            for _ in range(len(gemini_clients)):
                try:
                    r = next(gemini_cycle).models.generate_content(model=model, contents=prompt,
                        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.1,
                            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)))
                    data = json.loads(r.text)
                    data["extraction_method"] = "Gemini Final Fix"
                    print(f"    Gemini ({model}) OK!")
                    return data
                except: continue
    raise Exception("All AIs failed")

# Main
print("Fixing the final 3 low-quality materials...\n")
for tid in TARGET_IDS:
    res = supabase.table('materials').select('id, name, source_url').eq('id', tid).execute()
    if not res.data: continue
    mat = res.data[0]
    print(f"[{mat['id']}] {mat['name']}")
    print(f"  Old: {mat['source_url'][:70]}")
    
    url, pub, md = search_and_scrape(mat['name'])
    if not url:
        print("  SKIP - no source found\n")
        continue
    
    try:
        data = extract(md, mat['name'])
        clean = {}
        for k, v in data.items():
            if v is None or k not in VALID_DB_COLUMNS: continue
            if k in FLOAT_COLUMNS:
                s = sanitize_float(v)
                if s is not None: clean[k] = s
            else: clean[k] = v
        clean['source_url'] = url
        clean['source_name'] = f"{pub} (Final Fix)"
        supabase.table('materials').update(clean).eq('id', tid).execute()
        print(f"  DONE! -> {url[:60]}")
        print(f"  Updated {len(clean)} fields\n")
    except Exception as e:
        print(f"  FAILED: {e}\n")
    time.sleep(5)

print("All done!")
