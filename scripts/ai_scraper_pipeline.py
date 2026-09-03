import os
import sys
import json
import requests
from bs4 import BeautifulSoup
import groq

# Setup path so we can import the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import SessionLocal
from app.models import Material

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def scrape_url(url: str):
    print(f"Scraping {url} ...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch URL: {e}")
        return None
        
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Strip scripts and styles
    for script in soup(["script", "style", "nav", "footer"]):
        script.extract()
        
    text = soup.get_text(separator=' ', strip=True)
    # Truncate to avoid blowing up context limits
    return text[:15000] 

def extract_materials_via_ai(text: str, family_hint: str):
    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY environment variable is not set.")
        return []
        
    client = groq.Groq(api_key=GROQ_API_KEY)
    
    prompt = f"""
    You are an AI data extraction pipeline. Below is raw text scraped from a webpage about materials (Hint: {family_hint}).
    Extract ALL specific material grades and their engineering properties into a RAW JSON array.
    
    Format:
    [
      {{
        "name": "String (e.g. Inconel 718)",
        "category": "Metal",
        "subcategory": "String",
        "grade": "String",
        "density": Float (g/cm3),
        "tensile_strength_min": Float (MPa),
        "tensile_strength_max": Float (MPa),
        "yield_strength_min": Float (MPa),
        "yield_strength_max": Float (MPa),
        "elongation": Float (%),
        "elastic_modulus": Float (GPa),
        "thermal_conductivity": Float (W/mK),
        "max_service_temp": Float (Celsius)
      }}
    ]
    ONLY Output JSON. Do not include markdown blocks.
    
    RAW TEXT:
    {text}
    """
    
    print("Extracting structured properties using AI...")
    try:
        # Auto-discover models from Groq to avoid deprecation errors
        available_models = []
        try:
            models_data = client.models.list()
            # In 2026, Groq uses compound and oss models for free tiers
            valid = ["groq/compound", "openai/gpt-oss-20b", "qwen/qwen3.6-27b"]
            available_models = [m.id for m in models_data.data if m.id in valid]
        except Exception as e:
            print(f"Failed to fetch model list: {e}")
            available_models = ["groq/compound"]

        raw = None
        last_error = None
        for model in available_models:
            try:
                print(f"  [AI] Attempting extraction with dynamically discovered model: {model}...")
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=model,
                    temperature=0.1
                )
                raw = response.choices[0].message.content.strip()
                print(f"  [AI] Successfully used model: {model}")
                break
            except Exception as e:
                print(f"  [!] Model {model} failed: {e}")
                last_error = e
                continue
                
        if not raw:
            raise last_error
        if raw.startswith("```json"): raw = raw[7:]
        if raw.endswith("```"): raw = raw[:-3]
        return json.loads(raw.strip())
    except Exception as e:
        print(f"Extraction failed: {e}")
        return []

def run_pipeline(urls, hint):
    db = SessionLocal()
    total_added = 0
    for url in urls:
        text = scrape_url(url)
        if not text: continue
        
        data = extract_materials_via_ai(text, hint)
        print(f"AI found {len(data)} materials from {url}.")
        
        for mat in data:
            name = mat.get("name")
            if not name: continue
            
            exists = db.query(Material).filter(Material.name == name).first()
            if not exists:
                new_mat = Material(
                    name=name,
                    category=mat.get("category", "Metal"),
                    subcategory=mat.get("subcategory"),
                    grade=mat.get("grade"),
                    density=mat.get("density"),
                    tensile_strength_min=mat.get("tensile_strength_min"),
                    tensile_strength_max=mat.get("tensile_strength_max"),
                    yield_strength_min=mat.get("yield_strength_min"),
                    yield_strength_max=mat.get("yield_strength_max"),
                    elongation=mat.get("elongation"),
                    elastic_modulus=mat.get("elastic_modulus"),
                    thermal_conductivity=mat.get("thermal_conductivity"),
                    max_service_temp=mat.get("max_service_temp"),
                    source_url=url,
                    source_name="AI Pipeline Web Scraper",
                    is_verified=False
                )
                db.add(new_mat)
                total_added += 1
                print(f"  -> Added {name}")
            else:
                print(f"  -> {name} already exists.")
    db.commit()
    db.close()
    print(f"Pipeline finished. {total_added} new materials inserted.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI-Powered Web Scraper Pipeline for MatDataHub")
    parser.add_argument("urls", nargs='+', help="URLs to scrape")
    parser.add_argument("--hint", default="Engineering Materials", help="Hint to help the LLM identify the material family")
    
    args = parser.parse_args()
    run_pipeline(args.urls, args.hint)
