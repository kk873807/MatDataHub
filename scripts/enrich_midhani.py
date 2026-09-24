import os
import json
import time
from supabase import create_client, Client
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field
from typing import Optional, List

# Initialize Environment
load_dotenv()
supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

class EnrichmentSchema(BaseModel):
    composition: Optional[str] = Field(description="Nominal chemical composition string, e.g., 'Ni 72%, Cr 15%, Fe 8%'")
    density: Optional[float] = Field(description="Density in g/cm3")
    yield_strength_min: Optional[float] = Field(description="Minimum Yield strength in MPa")
    tensile_strength_min: Optional[float] = Field(description="Minimum Tensile strength in MPa")
    elongation: Optional[float] = Field(description="Elongation at break in %")
    elastic_modulus: Optional[float] = Field(description="Elastic modulus in GPa")
    thermal_conductivity: Optional[float] = Field(description="Thermal conductivity in W/mK")
    specific_heat: Optional[float] = Field(description="Specific heat in J/kgK")
    melting_point_min: Optional[float] = Field(description="Minimum melting point in Celsius")
    cost_per_kg_min: Optional[float] = Field(description="Estimated historical minimum cost per kg in INR")
    cost_per_kg_max: Optional[float] = Field(description="Estimated historical maximum cost per kg in INR")
    cost_currency: Optional[str] = Field(description="Always 'INR'")
    uns_number: Optional[str] = Field(description="UNS identifier")
    en_number: Optional[str] = Field(description="European (EN/British) standard number")
    din_number: Optional[str] = Field(description="German (DIN) standard number")
    is_number: Optional[str] = Field(description="Indian Standard (IS) number")
    gb_number: Optional[str] = Field(description="Chinese (GB) standard number")
    equivalent_grades_clean: Optional[List[str]] = Field(description="List of other trade names/specs cleaned up")

def run_enrichment():
    print("🚀 Starting MIDHANI Enrichment with Groq (openai/gpt-oss-20b)...")
    
    response = supabase.table('materials').select('*').eq('source_name', 'MIDHANI').execute()
    materials = response.data
    
    print(f"Found {len(materials)} materials to enrich.")
    
    for idx, mat in enumerate(materials):
        print(f"\n[{idx+1}/{len(materials)}] Enriching {mat['name']}...")
        
        prompt = f"""
        You are an expert materials scientist. 
        I have a material named "{mat['name']}" (Category: {mat['subcategory']}, source: MIDHANI).
        I need to populate missing engineering properties for a materials database.
        
        Current known equivalent specs: {mat.get('equivalent_grades', [])}
        Current UNS: {mat.get('uns_number', '')}
        
        Please provide the following typical values for this standard alloy in its annealed or most common condition:
        - Nominal chemical composition (e.g. 'Ni 72%, Cr 15%, Fe 8%')
        - Density (g/cm3)
        - Mechanical properties: Yield Strength (MPa), Tensile Strength (MPa), Elongation (%), Elastic Modulus (GPa)
        - Thermal properties: Thermal Conductivity (W/mK), Specific Heat (J/kgK), Melting Point (Celsius)
        - Historical Price: Estimate the cost per kg in INR (Indian Rupees). Provide min and max. Make a reasonable industry estimate based on the alloy type (e.g., Titanium is 2000-5000 INR/kg, Superalloys 3000-8000 INR/kg, etc.)
        
        ALSO: Parse the 'Current known equivalent specs' into the specific standard fields (en_number, din_number, etc.). If a German spec is given (e.g., 2.4816), put it in din_number. If a British spec is given, put it in en_number. Put the rest (AMS, trade names) in equivalent_grades_clean.
        """
        
        json_format_instructions = """
        Return a simple JSON object with EXACTLY these keys:
        - composition (string)
        - density (float)
        - yield_strength_min (float)
        - tensile_strength_min (float)
        - elongation (float)
        - elastic_modulus (float)
        - thermal_conductivity (float)
        - specific_heat (float)
        - melting_point_min (float)
        - cost_per_kg_min (float)
        - cost_per_kg_max (float)
        - cost_currency (string, always 'INR')
        - uns_number (string)
        - en_number (string)
        - din_number (string)
        - is_number (string)
        - gb_number (string)
        - equivalent_grades_clean (array of strings)
        """
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                res = groq_client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": f"You are a data extractor. Output ONLY valid JSON. {json_format_instructions}"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1
                )
                data = json.loads(res.choices[0].message.content)
                
                # Update payload
                update_data = {
                    "composition": data.get("composition"),
                    "density": data.get("density"),
                    "yield_strength_min": data.get("yield_strength_min"),
                    "tensile_strength_min": data.get("tensile_strength_min"),
                    "elongation": data.get("elongation"),
                    "elastic_modulus": data.get("elastic_modulus"),
                    "thermal_conductivity": data.get("thermal_conductivity"),
                    "specific_heat": data.get("specific_heat"),
                    "melting_point_min": data.get("melting_point_min"),
                    "cost_per_kg_min": data.get("cost_per_kg_min"),
                    "cost_per_kg_max": data.get("cost_per_kg_max"),
                    "cost_currency": "INR",
                    "extraction_method": "BeautifulSoup Scraper (Deterministic) + Groq Llama 3.1 Enrichment"
                }
                
                if data.get("uns_number") and not mat.get("uns_number"):
                    update_data["uns_number"] = data["uns_number"]
                if data.get("en_number"): update_data["en_number"] = data["en_number"]
                if data.get("din_number"): update_data["din_number"] = data["din_number"]
                if data.get("is_number"): update_data["is_number"] = data["is_number"]
                if data.get("gb_number"): update_data["gb_number"] = data["gb_number"]
                
                if data.get("equivalent_grades_clean"):
                    update_data["equivalent_grades"] = data["equivalent_grades_clean"]
                
                supabase.table('materials').update(update_data).eq('id', mat['id']).execute()
                print("  ✅ Enriched successfully.")
                break
                
            except Exception as e:
                print(f"  ❌ Error on attempt {attempt+1}: {e}")
                time.sleep(10)
        
        time.sleep(1)
        
if __name__ == "__main__":
    run_enrichment()
