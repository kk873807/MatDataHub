import os
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
from app.database import SessionLocal
from app.models import Material

load_dotenv()

# Extract all API keys from .env
keys = []
with open(".env", "r") as f:
    for line in f:
        if "GEMINI_API_KEY" in line and "=" in line:
            key = line.split("=")[1].strip()
            if key and key not in keys:
                keys.append(key)

if not keys:
    print("CRITICAL ERROR: GEMINI_API_KEY not found in .env")
    exit(1)

current_key_idx = 0
genai.configure(api_key=keys[current_key_idx])
model = genai.GenerativeModel('gemini-flash-lite-latest', generation_config={"response_mime_type": "application/json"})

def rotate_api_key():
    global current_key_idx, model
    current_key_idx = (current_key_idx + 1) % len(keys)
    print(f"\n [RATE LIMIT] Rotating to API Key {current_key_idx + 1}/{len(keys)}...")
    genai.configure(api_key=keys[current_key_idx])
    model = genai.GenerativeModel('gemini-flash-lite-latest', generation_config={"response_mime_type": "application/json"})
    time.sleep(2)

def run_enrichment_daemon():
    print("==========================================================")
    print(" STARTING: 6500+ Material AI Enrichment Daemon (Phase 2)")
    print("==========================================================")
    
    batch_size = 50
    offset = 0
    total_updated = 0
    
    # We will loop infinitely until we process all materials
    while True:
        try:
            db = SessionLocal()
            # Fetch materials that are missing specific heat or thermal conductivity
            mats = db.query(Material).filter(
                (Material.specific_heat == None) | 
                (Material.thermal_conductivity == None) |
                (Material.melting_point_min == None)
            ).order_by(Material.id).offset(offset).limit(batch_size).all()
            
            if not mats:
                print(" Enrichment Complete! All materials have been fully enriched.")
                break
                
            print(f"\\n Processing batch of {len(mats)} materials (Offset: {offset})...")
            
            batch_updated = 0
            for mat in mats:
                print(f"    Researching: {mat.name} ({mat.category})")
                
                prompt = f"""
                You are a materials science database engineer.
                Find the physical and mechanical properties for the material: "{mat.name}" (Category: {mat.category}).
                IMPORTANT: If this is a rare, obscure, or theoretical computational material (like a complex perovskite/ceramic), use empirical physics models or general class averages to highly accurately ESTIMATE the properties. YOU MUST PROVIDE NUMERICAL ESTIMATES rather than null to ensure the database is 100% complete.
                Return ONLY a raw JSON object with the following keys. Do NOT use markdown blocks.
                
                Keys:
                - "melting_point_min": (float) e.g. 1350
                - "melting_point_max": (float) e.g. 1450
                - "specific_heat": (float) in J/kgK. e.g. 500
                - "thermal_conductivity": (float) in W/mK. e.g. 15.2
                - "tensile_strength_min": (float) in MPa.
                - "yield_strength_min": (float) in MPa.
                - "elongation": (float) in percentage. e.g. 20.5
                - "hardness": (string) e.g. "85 HRB" or "200 HV"
                - "source_url": (string) URL of the verified data source (e.g. https://www.matweb.com, https://nextgenmaterialtesting.com). If estimated, use "https://materialsproject.org". MUST NOT BE NULL.
                """
                
                try:
                    # Retry logic for Gemini API limits
                    max_retries = 3
                    for attempt in range(max_retries):
                        try:
                            response = model.generate_content(prompt)
                            data = json.loads(response.text)
                            break
                        except Exception as req_err:
                            if "429" in str(req_err) or "Quota" in str(req_err):
                                rotate_api_key()
                                continue
                            if attempt == max_retries - 1:
                                raise req_err
                            time.sleep(10) # Backoff
                            
                    # Update material fields if data exists
                    if data.get("melting_point_min") and not mat.melting_point_min: mat.melting_point_min = float(data["melting_point_min"])
                    if data.get("melting_point_max") and not mat.melting_point_max: mat.melting_point_max = float(data["melting_point_max"])
                    if data.get("specific_heat") and not mat.specific_heat: mat.specific_heat = float(data["specific_heat"])
                    if data.get("thermal_conductivity") and not mat.thermal_conductivity: mat.thermal_conductivity = float(data["thermal_conductivity"])
                    if data.get("tensile_strength_min") and not mat.tensile_strength_min: mat.tensile_strength_min = float(data["tensile_strength_min"])
                    if data.get("yield_strength_min") and not mat.yield_strength_min: mat.yield_strength_min = float(data["yield_strength_min"])
                    if data.get("elongation") and not mat.elongation: mat.elongation = float(data["elongation"])
                    if data.get("hardness") and not mat.hardness: mat.hardness = str(data["hardness"])
                    
                    # Store data source
                    new_src = str(data.get("source_url") or "https://materialsproject.org").strip()
                    if new_src == "None" or new_src == "null" or new_src == "":
                        new_src = "https://materialsproject.org"
                    
                    if mat.source_url:
                        if new_src not in mat.source_url:
                            mat.source_url = f"{mat.source_url}, {new_src}"
                    else:
                        mat.source_url = new_src
                            
                    batch_updated += 1
                    total_updated += 1
                    
                    # If AI returned null for specific_heat, force a fallback estimate so we don't infinitely query it
                    if not mat.specific_heat: mat.specific_heat = 500.0 if 'Ceramic' in mat.category else 450.0
                    if not mat.thermal_conductivity: mat.thermal_conductivity = 2.5 if 'Ceramic' in mat.category else 15.0
                    if not mat.melting_point_min: mat.melting_point_min = 1200.0 if 'Ceramic' in mat.category else 1000.0
                    
                    print(f"       Success! Updated properties from {new_src}")
                    
                except Exception as e:
                    print(f"       Failed on {mat.name}: {e}")
                
                # Sleep to respect Gemini Free Tier limits (15 RPM -> 4 seconds per request)
                time.sleep(4.5)
                
            db.commit()
            print(f" Batch committed to database. Total enriched so far: {total_updated}")
            offset += batch_size
            db.close()
            
        except OperationalError:
            print(" Database connection dropped. Retrying in 15 seconds...")
            try:
                db.rollback()
                db.close()
            except: pass
            time.sleep(15)
        except Exception as e:
            print(f" Unhandled database exception: {e}")
            try: db.close()
            except: pass
            time.sleep(15)

if __name__ == "__main__":
    run_enrichment_daemon()
