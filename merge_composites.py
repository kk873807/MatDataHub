import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

merge_pairs = [
    # duplicate_id, keeper_id, keeper_url_update
    (246, 562, "https://www.wood-database.com/oak/"), # Oak Wood -> Oak Wood (Dry)
    (247, 580, None) # Pine Wood -> Pine Wood (Dry)
]

for dup_id, keep_id, url_update in merge_pairs:
    print(f"Merging {dup_id} into {keep_id}...")
    
    # 1. Update project_items foreign keys
    try:
        supabase.table("project_items").update({"material_id": keep_id}).eq("material_id", dup_id).execute()
        print(f"  - Remapped project_items for {dup_id}")
    except Exception as e:
        print(f"  - Error remapping project_items: {e}")
        
    # 2. Optionally update keeper source_url
    if url_update:
        try:
            # fetch existing
            res = supabase.table("materials").select("source_url").eq("id", keep_id).execute()
            existing_url = res.data[0].get("source_url") or ""
            if url_update not in existing_url:
                new_url = f"{existing_url}, {url_update}".strip(", ")
                supabase.table("materials").update({"source_url": new_url}).eq("id", keep_id).execute()
                print(f"  - Updated source URL for {keep_id}")
        except Exception as e:
            print(f"  - Error updating URL: {e}")
            
    # 3. Delete duplicate material
    try:
        supabase.table("materials").delete().eq("id", dup_id).execute()
        print(f"  - Deleted duplicate material {dup_id}")
    except Exception as e:
        print(f"  - Error deleting duplicate: {e}")

print("Merge completed successfully!")
