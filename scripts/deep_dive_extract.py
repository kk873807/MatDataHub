import os
import time
import sys
from supabase import create_client
from dotenv import load_dotenv

# Ensure auto_crawler can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from auto_crawler import process_single_material
except ImportError:
    print("Could not import auto_crawler. Make sure it is in the same directory or accessible.")
    sys.exit(1)

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

def get_sparse_materials():
    all_sparse = []
    limit = 1000
    offset = 0
    
    print("Fetching materials from database to find targets for deep dive extraction...")
    while True:
        res = supabase.table("materials").select("id, name, source_name, source_url, density, yield_strength_min, thermal_conductivity, hardness").range(offset, offset + limit - 1).execute()
        data = res.data
        if not data:
            break
            
        for mat in data:
            url = mat.get("source_url") or ""
            source = mat.get("source_name") or ""
            
            # Skip MP and Kaggle since they are API/CSV bulk imports, not unstructured web pages
            if "Materials Project" in source or "Kaggle" in source:
                continue
                
            # Skip if no valid URL
            if not url.startswith("http"):
                continue
                
            # Check for sparsity - if missing multiple key mechanical/physical properties
            missing_count = sum(1 for k in ["density", "yield_strength_min", "thermal_conductivity", "hardness"] if mat.get(k) is None)
            
            # If missing at least 2 key properties, flag for deep dive
            if missing_count >= 2:
                all_sparse.append(mat)
                
        if len(data) < limit:
            break
        offset += limit
        
    return all_sparse

def main():
    print("=" * 60)
    print("STARTING DEEP DIVE EXTRACTION TASK")
    print("=" * 60)
    
    sparse_materials = get_sparse_materials()
    print(f"Found {len(sparse_materials)} materials with unstructured web sources missing key properties.")
    
    success = 0
    failed = 0
    
    with open("deep_dive_report.txt", "w", encoding="utf-8") as report:
        report.write(f"Targets for Deep Dive Extraction: {len(sparse_materials)}\n\n")
        
        for i, mat in enumerate(sparse_materials):
            url = mat["source_url"]
            name = mat["name"]
            print(f"\n[{i+1}/{len(sparse_materials)}] Deep diving into {name} at {url}...")
            
            try:
                # auto_crawler handles the Firecrawl + LLM + Supabase update
                process_single_material(url, max_retries=2)
                success += 1
                report.write(f"[SUCCESS] Re-extracted {name} from {url}\n")
            except Exception as e:
                failed += 1
                print(f"❌ Failed to process {name}: {e}")
                report.write(f"[FAILED] {name} from {url} - Error: {e}\n")
                
            # Rate limit Firecrawl and LLM
            time.sleep(5)
            
    print("\n" + "=" * 60)
    print("DEEP DIVE EXTRACTION COMPLETE")
    print("=" * 60)
    print(f"  Successfully processed: {success}")
    print(f"  Failed: {failed}")
    
if __name__ == "__main__":
    main()
