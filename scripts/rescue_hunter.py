import os
import sys
import json
import time
import re
import csv
import warnings
from urllib.parse import urlparse
warnings.filterwarnings('ignore')

from supabase import create_client
from dotenv import load_dotenv
import itertools
from firecrawl import FirecrawlApp
from groq import Groq
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import Optional

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
load_dotenv()
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
firecrawl_app = FirecrawlApp(api_key=os.environ.get('FIRECRAWL_API_KEY'))

with open('.env', 'r', encoding='utf-8') as f:
    env_text = f.read()

groq_keys = re.findall(r'GROQ_API_KEY.*?=([^\s]+)', env_text)
gemini_keys = re.findall(r'GEMINI_API_KEY.*?=([^\s]+)', env_text)
groq_clients = [Groq(api_key=key) for key in groq_keys if key]
gemini_clients = [genai.Client(api_key=key) for key in gemini_keys if key]
gemini_cycle = itertools.cycle(gemini_clients) if gemini_clients else None

GEMINI_MODELS = ['gemini-3.6-flash', 'gemini-3.5-flash-lite']

VALID_DB_COLUMNS = {
    'category', 'subcategory', 'grade', 'standard',
    'density', 'tensile_strength_min', 'tensile_strength_max',
    'yield_strength_min', 'yield_strength_max', 'elongation',
    'hardness', 'elastic_modulus',
    'thermal_conductivity', 'specific_heat',
    'melting_point_min', 'melting_point_max', 'max_service_temp',
    'cost_per_kg_min', 'cost_per_kg_max', 'cost_currency',
    'applications', 'equivalent_grades', 'composition', 'description',
    'source_url', 'source_name', 'extraction_method', 'is_verified',
}

FLOAT_COLUMNS = {
    'density', 'tensile_strength_min', 'tensile_strength_max',
    'yield_strength_min', 'yield_strength_max', 'elongation',
    'elastic_modulus', 'thermal_conductivity', 'specific_heat',
    'melting_point_min', 'melting_point_max', 'max_service_temp',
    'cost_per_kg_min', 'cost_per_kg_max',
}

BAD_DOMAINS = [
    'makeitfrom.com', 'wikipedia.org', 'researchgate.net', 'sciencedirect.com',
    'kaggle.com', 'ccsteels.com', 'suppliersonline.com', 'mehdikhannn.shop',
    'alibaba.com', 'aliexpress.com', 'made-in-china.com', 'scribd.com', 
    'studocu.com', 'reddit.com', 'quora.com'
]

LOW_QUALITY_DOMAINS_TO_REPLACE = [
    'wikipedia.org', 'researchgate.net', 'sciencedirect.com', 'springer.com', 
    'alibaba.com', 'aliexpress.com', 'made-in-china.com', 'indiamart.com',    
    'quora.com', 'reddit.com', 'scribd.com', 'studocu.com'
]

class MaterialSchema(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    density: Optional[float] = None
    yield_strength_min: Optional[float] = None
    tensile_strength_min: Optional[float] = None
    elongation_min: Optional[float] = None
    elastic_modulus: Optional[float] = None
    hardness: Optional[float] = None
    melting_point_min: Optional[float] = None
    melting_point_max: Optional[float] = None
    thermal_conductivity: Optional[float] = None
    specific_heat: Optional[float] = None
    electrical_resistivity: Optional[float] = None
    magnetic_permeability: Optional[float] = None

def sanitize_float(value):
    if value is None: return None
    if isinstance(value, (int, float)): return float(value)
    if isinstance(value, str):
        match = re.search(r'-?\d+\.?\d*', value)
        if match: return float(match.group())
    if isinstance(value, dict):
        v = value.get('value')
        if v is not None: return float(v)
    return None

# ==========================================
# 2. SEARCH ENGINE
# ==========================================
def generate_search_queries(material_name):
    queries = []
    queries.append(f"{material_name} material properties datasheet -makeitfrom -wikipedia")
    
    paren_match = re.search(r'\(([^)]+)\)', material_name)
    if paren_match:
        core_name = paren_match.group(1).split(',')[0].strip()
        queries.append(f"{core_name} alloy properties datasheet pdf")
        
    std_match = re.search(r'(EN\s*\d+\.\d+|AISI\s*\d+\w*|UNS\s*[A-Z]\d+|ASTM\s*[A-Z]?\d+|SAE-AISI\s*\w+|AWS\s*\w+)', material_name)
    if std_match:
        queries.append(f"{std_match.group(1)} mechanical properties density tensile strength")
        
    queries.append(f"site:azom.com OR site:matweb.com {material_name}")
    return queries

def deep_search(material_name):
    queries = generate_search_queries(material_name)
    
    for qi, query in enumerate(queries, 1):
        print(f"    🔎 Query {qi}/{len(queries)}: {query[:80]}...")
        try:
            result = firecrawl_app.search(query)
            search_results = result if isinstance(result, list) else result.get('data', []) if isinstance(result, dict) else getattr(result, 'web', [])
            
            for r in search_results[:3]:
                link = getattr(r, 'url', None) or (r.get('url') if isinstance(r, dict) else None)
                if not link or any(b in link.lower() for b in BAD_DOMAINS):
                    continue
                
                publisher = "Primary Web Source"
                if "matweb.com" in link: publisher = "MatWeb"
                elif "azom.com" in link: publisher = "AZoM"
                elif ".pdf" in link.lower(): publisher = "Manufacturer Datasheet (PDF)"
                
                print(f"    🕷️ Trying: {link[:80]}...")
                try:
                    scrape_res = firecrawl_app.scrape_url(link)
                    markdown_content = scrape_res.markdown if hasattr(scrape_res, 'markdown') else scrape_res.get('markdown', scrape_res.get('data', {}).get('markdown', '')) if isinstance(scrape_res, dict) else str(scrape_res)
                    
                    if markdown_content and len(markdown_content) >= 50:
                        print(f"    ✅ Scraped successfully ({len(markdown_content)} chars)")
                        return link, publisher, markdown_content
                except Exception as e:
                    print(f"    ⚠️ Scrape failed: {str(e)[:50]}")
                    continue
        except Exception as e:
            if "credits" in str(e).lower() or "payment" in str(e).lower():
                print(f"    ❌ FIRECRAWL CREDITS EXHAUSTED! Stopping.")
                return None, None, None
            print(f"    ⚠️ Search failed: {str(e)[:50]}")
        time.sleep(3)
    return None, None, None

# ==========================================
# 3. AI EXTRACTION
# ==========================================
def extract_properties(markdown_text, material_name):
    prompt = f"""Extract the material properties for '{material_name}' from the text.
    Return a JSON strictly matching the schema. Convert to SI units (MPa, g/cm³, W/m·K).
    For numbers, return ONLY the number (no units). If missing, return null.
    TEXT: {markdown_text[:12000]}"""
    
    if groq_clients:
        try:
            print("    🧠 Trying Groq...")
            response = groq_clients[0].chat.completions.create(
                messages=[{"role": "system", "content": f"Output JSON matching schema: {MaterialSchema.model_json_schema()}"}, {"role": "user", "content": prompt}],
                model="qwen/qwen3.8-27b", response_format={"type": "json_object"}, temperature=0.1, timeout=30
            )
            data = json.loads(response.choices[0].message.content)
            data["extraction_method"] = "Groq Rescue Hunt"
            print("    ✅ Groq succeeded!")
            return data
        except Exception as e:
            print(f"    ⚠️ Groq failed: {str(e)[:50]}")

    print("    🧠 Trying Gemini...")
    if gemini_cycle and gemini_clients:
        for model_name in GEMINI_MODELS:
            for attempt in range(len(gemini_clients)):
                current_gemini = next(gemini_cycle)
                try:
                    res = current_gemini.models.generate_content(
                        model=model_name, contents=prompt,
                        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.1, automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True))
                    )
                    data = json.loads(res.text)
                    data["extraction_method"] = "Gemini Rescue Hunt"
                    print(f"    ✅ Gemini ({model_name}) succeeded!")
                    return data
                except Exception as e:
                    if '404' in str(e): break
                    continue
    raise Exception("All AIs exhausted")

# ==========================================
# 4. MAIN
# ==========================================
def main():
    print("=" * 60)
    print("🚑 RESCUE HUNTER — Fixing Dead & Low-Quality Links")
    print("=" * 60)
    
    target_ids = set()
    
    # 1. Load dead links (exclude 429s)
    if os.path.exists('dead_links_report.csv'):
        with open('dead_links_report.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Error/Status'] != '429':
                    target_ids.add(int(row['ID']))
                    
    # 2. Fetch all materials to find low-quality links
    print("Scanning database for low-quality URLs...")
    materials = []
    page = 0
    while True:
        res = supabase.table('materials').select('id, name, source_url, source_name').range(page * 1000, (page + 1) * 1000 - 1).execute()
        if not res.data: break
        materials.extend(res.data)
        if len(res.data) < 1000: break
        page += 1
        
    targets = []
    for m in materials:
        source_name = m.get('source_name') or ''
        
        # Skip if we already rescued this one in a previous run
        if '(Rescued)' in source_name or '(Deep Hunt)' in source_name:
            continue
            
        if m['id'] in target_ids:
            targets.append(m)
            continue
            
        url = m.get('source_url', '') or ''
        try:
            domain = urlparse(url).netloc.lower()
            if any(bad in domain for bad in LOW_QUALITY_DOMAINS_TO_REPLACE):
                targets.append(m)
        except:
            pass
            
    print(f"Total materials to rescue: {len(targets)}\n")
    
    success = 0
    for i, mat in enumerate(targets, 1):
        mat_id, mat_name = mat['id'], mat['name']
        print(f"[{i}/{len(targets)}] {mat_name}")
        print(f"  Old URL: {mat['source_url'][:60]}")
        
        new_url, publisher, markdown = deep_search(mat_name)
        
        if not new_url or not markdown:
            print(f"  ❌ No new source found. Keeping old data.")
            time.sleep(2)
            continue
            
        try:
            extracted_data = extract_properties(markdown, mat_name)
            
            clean_data = {}
            for k, v in extracted_data.items():
                if v is None or k not in VALID_DB_COLUMNS: continue
                if k in FLOAT_COLUMNS:
                    sanitized = sanitize_float(v)
                    if sanitized is not None: clean_data[k] = sanitized
                else:
                    clean_data[k] = v
            
            clean_data['source_url'] = new_url
            clean_data['source_name'] = f"{publisher} (Rescued)"
            
            print(f"  💾 Overwriting DB with new properties ({len(clean_data)} fields updated)...")
            supabase.table('materials').update(clean_data).eq('id', mat_id).execute()
            print(f"  ✅ SUCCESS! Replaced with: {new_url[:60]}")
            success += 1
            
        except Exception as e:
            print(f"  ⚠️ Extraction failed: {e}")
            if "All AIs exhausted" in str(e): time.sleep(60)
        
        time.sleep(5)
        
    print("\n" + "=" * 60)
    print(f"RESCUE COMPLETE — ✅ Successfully updated: {success} / {len(targets)}")

if __name__ == "__main__":
    main()
