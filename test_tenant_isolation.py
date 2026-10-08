import os
import httpx

API = "http://localhost:8000/api/v1"

def create_user_and_get_token(email, password):
    # Try to register
    httpx.post(f"{API}/auth/register", json={"email": email, "password": password, "full_name": email})
    # Login
    resp = httpx.post(f"{API}/auth/login", json={"email": email, "password": password})
    if resp.status_code == 200:
        return resp.json()["access_token"]
    raise Exception(f"Failed to login {email}: {resp.text}")

def run_tests():
    print("Setting up users...")
    token_a = create_user_and_get_token("tenant_x@example.com", "password123")
    token_b = create_user_and_get_token("tenant_y@example.com", "password123")
    
    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}
    
    # 1. User A creates a BOM history item
    csv_content = "material_id,Material,Weight_kg,cbam_sector,cn_code,country_of_origin\\nMAT-1,Steel,100,Iron & Steel,72083900,China"
    files = {"file": ("test.csv", csv_content.encode('utf-8'), "text/csv")}
    data = {"material_col": "Material", "weight_col": "Weight_kg"}
    
    print("User A analyzing BOM...")
    resp = httpx.post(f"{API}/materials/bom_analyze", headers=headers_a, files=files, data=data)
    if resp.status_code != 200:
        print("Failed to analyze BOM:", resp.text)
        return
        
    # Get A's history
    resp_hist = httpx.get(f"{API}/account/bom-history", headers=headers_a)
    history_a = resp_hist.json()
    if not history_a:
        print("No history for A found")
        return
    bom_id = history_a[0]['id']
    print(f"User A created BOM {bom_id}")
    
    # 2. A requests B's history item by ID (User B requesting A's item)
    print("\\nTest 1: User B requesting A's item by ID")
    resp_b_get = httpx.get(f"{API}/account/bom-history/{bom_id}", headers=headers_b)
    print(f"Response: {resp_b_get.status_code}")
    assert resp_b_get.status_code in (403, 404), f"Tenant isolation failed for GET! Code: {resp_b_get.status_code}"
    
    # 3. User B attempts to delete A's item
    print("\\nTest 2: User B attempting to delete A's item")
    resp_b_delete = httpx.delete(f"{API}/account/bom-history/{bom_id}", headers=headers_b)
    print(f"Response: {resp_b_delete.status_code}")
    assert resp_b_delete.status_code in (403, 404), f"Tenant isolation failed for DELETE! Code: {resp_b_delete.status_code}"
    
    # 4. Unauthenticated requests
    print("\\nTest 3: Unauthenticated GET")
    resp_unauth = httpx.get(f"{API}/account/bom-history/{bom_id}")
    print(f"Response: {resp_unauth.status_code}")
    assert resp_unauth.status_code == 401, "Auth failed for GET"
    
    # 5. List endpoints return only caller's rows
    print("\\nTest 4: User B listing history")
    resp_b_list = httpx.get(f"{API}/account/bom-history", headers=headers_b)
    history_b = resp_b_list.json()
    print(f"User B has {len(history_b)} items. (Expected 0)")
    assert len(history_b) == 0, "User B can see A's history in list!"
    
    print("\\nAll tenant isolation tests PASSED.")

if __name__ == "__main__":
    run_tests()
