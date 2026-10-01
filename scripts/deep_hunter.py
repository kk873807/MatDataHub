"""
Deep Hunt Script — Specialized for the final ~20 stubborn materials.
Uses multiple search query variations and tries multiple results per material.
"""
import os
import sys
import json
import time
import re
import csv
import warnings
warnings.filterwarnings('ignore')

from supabase import create_client
from dotenv import load_dotenv
import itertools
from firecrawl import FirecrawlApp

# AI Imports
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

# Domains that always fail to scrape — skip them immediately
BAD_DOMAINS = [
    'makeitfrom.com', 'wikipedia.org', 'researchgate.net', 'sciencedirect.com',
    'kaggle.com', 'ccsteels.com', 'suppliersonline.com', 'mehdikhannn.shop',
    'stb.by',
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
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        match = re.search(r'-?\d+\.?\d*', value)
        if match:
            return float(match.group())
    if isinstance(value, dict):
        # Handle {"value": 7.89, "unit": "g/cm³"} from AI
        v = value.get('value')
        if v is not None:
            return float(v)
    return None

# ==========================================
# 2. DEEP SEARCH — Multiple query strategies
# ==========================================
def generate_search_queries(material_name):
    """Generate multiple search query variations for a stubborn material."""
    queries = []
    
    # Query 1: Standard query (same as autonomous_hunter)
    queries.append(f"{material_name} material properties datasheet -makeitfrom -wikipedia")
    
    # Query 2: Shorter — just the core alloy designation
    # Extract the key identifier (e.g., "36MnB4" from "EN 1.5537 (36MnB4) Boron Steel")
    paren_match = re.search(r'\(([^)]+)\)', material_name)
    if paren_match:
        core_name = paren_match.group(1).split(',')[0].strip()
        queries.append(f"{core_name} steel alloy properties datasheet")
    
    # Query 3: Use the EN/AISI/UNS number directly
    std_match = re.search(r'(EN\s*\d+\.\d+|AISI\s*\d+\w*|UNS\s*[A-Z]\d+|ASTM\s*[A-Z]?\d+|SAE-AISI\s*\w+|AWS\s*\w+)', material_name)
    if std_match:
        queries.append(f"{std_match.group(1)} mechanical properties density tensile strength")
    
    # Query 4: Material type focus
    type_match = re.search(r'(Steel|Aluminum|Cast Iron|Stainless Steel|Weld Metal|Copper|Titanium|Cast Stainless Steel)', material_name)
    if type_match:
        clean_name = material_name.replace(type_match.group(1), '').strip().strip('()')
        queries.append(f"{clean_name} {type_match.group(1)} datasheet PDF properties")
    
    # Query 5: AZoM/MatWeb focused
    queries.append(f"site:azom.com OR site:matweb.com {material_name}")
    
    return queries

def deep_search_primary_source(material_name):
    """Try multiple search queries and multiple results per query."""
    queries = generate_search_queries(material_name)
    
    for qi, query in enumerate(queries, 1):
        print(f"    🔎 Query {qi}/{len(queries)}: {query[:80]}...")
        
        try:
            result = firecrawl_app.search(query)
            
            search_results = []
            if isinstance(result, list):
                search_results = result
            elif isinstance(result, dict) and 'data' in result:
                search_results = result['data']
            elif hasattr(result, 'web'):
                search_results = result.web
            
            # Try multiple results from this query (up to 3)
            for r in search_results[:3]:
                link = getattr(r, 'url', None)
                if not link and isinstance(r, dict):
                    link = r.get('url')
                if not link:
                    continue
                
                # Skip known-bad domains
                if any(b in link.lower() for b in BAD_DOMAINS):
                    continue
                
                publisher = "Primary Web Source"
                if "matweb.com" in link: publisher = "MatWeb"
                elif "azom.com" in link: publisher = "AZoM"
                elif "appluslaboratories.com" in link: publisher = "Applus Laboratories"
                elif "virgamet.com" in link: publisher = "Virgamet"
                elif "fabdigit.com" in link: publisher = "FabDigit"
                elif ".pdf" in link.lower(): publisher = "Manufacturer Datasheet (PDF)"
                
                # Try scraping this URL
                print(f"    🕷️ Trying: {link[:80]}...")
                try:
                    scrape_res = firecrawl_app.scrape_url(link)
                    
                    markdown_content = None
                    if hasattr(scrape_res, 'markdown') and scrape_res.markdown:
                        markdown_content = scrape_res.markdown
                    elif isinstance(scrape_res, dict):
                        markdown_content = scrape_res.get('markdown', scrape_res.get('data', {}).get('markdown', ''))
                    else:
                        markdown_content = str(scrape_res)
                    
                    if markdown_content and len(markdown_content) >= 50:
                        print(f"    ✅ Scraped successfully ({len(markdown_content)} chars)")
                        return link, publisher, markdown_content
                    else:
                        print(f"    ⚠️ Empty scrape, trying next...")
                        
                except Exception as e:
                    err = str(e)[:80]
                    print(f"    ⚠️ Scrape failed: {err}, trying next...")
                    continue
                    
        except Exception as e:
            err = str(e)
            if "Payment Required" in err or "Insufficient credits" in err:
                print(f"    ❌ FIRECRAWL CREDITS EXHAUSTED! Stopping.")
                return None, None, None
            print(f"    ⚠️ Search failed: {str(e)[:80]}")
            
        time.sleep(3)  # Pause between queries to respect rate limits
    
    return None, None, None

# ==========================================
# 3. AI EXTRACTION (same waterfall as before)
# ==========================================
def extract_properties(markdown_text, material_name):
    prompt = f"""
    Extract the material properties for '{material_name}' from the following text.
    Return a JSON object strictly matching the schema. 
    IMPORTANT: For numeric fields (density, strength, etc.), return ONLY the number, no units.
    Example: density should be 7.93 not "7.93 g/cm³"
    If a value is missing, return null.
    Convert all units to standard SI/metric (MPa for strength, g/cm³ for density, W/m·K for conductivity).

    TEXT:
    {markdown_text[:12000]}
    """
    
    # 1. Try Groq
    try:
        if groq_clients:
            print("    🧠 AI: Trying Groq...")
            client = groq_clients[0]
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"You are a data extractor. Output ONLY valid JSON matching this schema: {MaterialSchema.model_json_schema()}"},
                    {"role": "user", "content": prompt}
                ],
                model="qwen/qwen3.8-27b",
                response_format={"type": "json_object"},
                temperature=0.1,
                timeout=30
            )
            material_data = json.loads(chat_completion.choices[0].message.content)
            material_data["extraction_method"] = "Groq Deep Hunt"
            print("    ✅ Groq succeeded!")
            return material_data
    except Exception as e:
        print(f"    ⚠️ Groq failed: {str(e)[:60]}")

    # 2. Try Gemini
    print("    🧠 AI: Trying Gemini rotation...")
    if gemini_cycle and gemini_clients:
        for model_name in GEMINI_MODELS:
            for attempt in range(len(gemini_clients)):
                current_gemini = next(gemini_cycle)
                try:
                    response = current_gemini.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            temperature=0.1,
                            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                        ),
                    )
                    material_data = json.loads(response.text)
                    material_data["extraction_method"] = "Gemini Deep Hunt"
                    print(f"    ✅ Gemini ({model_name} key {attempt+1}) succeeded!")
                    return material_data
                except Exception as e:
                    err_msg = str(e)[:60]
                    if '404' in err_msg:
                        break
                    continue
    
    raise Exception("All AIs exhausted")

# ==========================================
# 4. MAIN
# ==========================================
def main():
    print("=" * 60)
    print("🔬 DEEP HUNT — Final Stubborn Materials")
    print("=" * 60)
    
    # Get remaining MakeItFrom materials directly from DB
    print("Fetching remaining targets from database...")
    materials = []
    page = 0
    while True:
        res = supabase.table('materials').select('id, name, source_url').ilike('source_url', '%makeitfrom%').range(page * 1000, (page + 1) * 1000 - 1).execute()
        if not res.data:
            break
        materials.extend(res.data)
        if len(res.data) < 1000:
            break
        page += 1
    
    print(f"Remaining targets: {len(materials)}\n")
    
    if not materials:
        print("🎉 No MakeItFrom materials left! Database is fully migrated!")
        return
    
    success_count = 0
    fail_count = 0
    
    for i, mat in enumerate(materials, 1):
        mat_id = mat['id']
        mat_name = mat['name']
        print(f"\n[{i}/{len(materials)}] {mat_name}")
        print(f"  Current URL: {mat['source_url'][:60]}...")
        
        # Deep search with multiple queries and multiple results
        new_url, publisher, markdown = deep_search_primary_source(mat_name)
        
        if not new_url or not markdown:
            print(f"  ❌ Could not find ANY source after deep search. Truly manual.")
            fail_count += 1
            time.sleep(3)
            continue
        
        # AI extraction
        try:
            extracted_data = extract_properties(markdown, mat_name)
            
            clean_data = {}
            for k, v in extracted_data.items():
                if v is None or k not in VALID_DB_COLUMNS:
                    continue
                if k in FLOAT_COLUMNS:
                    sanitized = sanitize_float(v)
                    if sanitized is not None:
                        clean_data[k] = sanitized
                else:
                    clean_data[k] = v
            
            clean_data['source_url'] = new_url
            clean_data['source_name'] = f"{publisher} (Deep Hunt)"
            
            print(f"  💾 Updating database ({len(clean_data)} fields)...")
            supabase.table('materials').update(clean_data).eq('id', mat_id).execute()
            print(f"  ✅ SUCCESS! Replaced MakeItFrom with: {new_url[:60]}")
            success_count += 1
            
        except Exception as e:
            if "All AIs exhausted" in str(e):
                print(f"  ⏳ AI quotas exhausted! Waiting 60s...")
                time.sleep(60)
                continue
            else:
                print(f"  ⚠️ Extraction failed: {e}")
                fail_count += 1
        
        time.sleep(7)  # Slower pace — each material uses multiple searches
    
    print("\n" + "=" * 60)
    print(f"DEEP HUNT COMPLETE — ✅ Rescued: {success_count} | ❌ Truly Manual: {fail_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
