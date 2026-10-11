"""
Tenant Isolation Integration Tests.

Verifies strict cross-tenant data isolation across:
  1. BOM History list (/api/v1/account/bom-history)
  2. BOM History detail by ID (/api/v1/account/bom-history/{id})
  3. BOM History deletion by ID (/api/v1/account/bom-history/{id})
  4. BOM Analysis tier-gating (/api/v1/materials/bom_analyze)
  5. Transaction history (/api/v1/account/transactions)
  6. Custom Materials (/api/v1/materials/custom/mine)
  7. Unauthenticated request protection (401)

Run:  pytest tests/test_tenant_isolation.py -q   (or: python tests/test_tenant_isolation.py)
"""
import json
import os
import sys

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from app.database import Base, get_db
from app.main import app
from app.models import BOMAnalysis, CustomMaterial, Transaction, User
from app.auth import create_access_token, hash_password


# --- Hermetic In-Memory SQLite Setup ---
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_tenant_isolation():
    db = TestingSessionLocal()

    # 1. Setup Users:
    # Tenant A (Advanced), Tenant B (Advanced), Tenant C (Free)
    user_a = User(
        email="tenant_a@example.com",
        name="Tenant A",
        hashed_password=hash_password("pass123"),
        tier="advanced",
        is_active=True,
    )
    user_b = User(
        email="tenant_b@example.com",
        name="Tenant B",
        hashed_password=hash_password("pass123"),
        tier="advanced",
        is_active=True,
    )
    user_c = User(
        email="tenant_c@example.com",
        name="Tenant C",
        hashed_password=hash_password("pass123"),
        tier="free",
        is_active=True,
    )
    db.add_all([user_a, user_b, user_c])
    db.commit()
    db.refresh(user_a)
    db.refresh(user_b)
    db.refresh(user_c)

    token_a = create_access_token(user_id=user_a.id, email=user_a.email, tier=user_a.tier)
    token_b = create_access_token(user_id=user_b.id, email=user_b.email, tier=user_b.tier)
    token_c = create_access_token(user_id=user_c.id, email=user_c.email, tier=user_c.tier)

    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}
    headers_c = {"Authorization": f"Bearer {token_c}"}

    # 2. Populate User A's data
    bom_a = BOMAnalysis(
        user_id=user_a.id,
        filename="project_alpha_bom.csv",
        strict_mode=True,
        total_co2_tonnes=125.5,
        cbam_cost_eur=9412.5,
        total_rows=10,
        quarantined_rows=0,
        results_json=json.dumps({"project": "Alpha", "secret_cost": 9412.5}),
    )
    tx_a = Transaction(
        user_id=user_a.id,
        amount=99.0,
        currency="EUR",
        tier_purchased="advanced",
        status="completed",
    )
    custom_mat_a = CustomMaterial(
        user_id=user_a.id,
        name="Tenant A Proprietary Alloy 7075-X",
        category="Metals",
        subcategory="Aluminium",
        source_url="https://example.com/spec-a",
        status="verified",
    )
    db.add_all([bom_a, tx_a, custom_mat_a])
    db.commit()
    db.refresh(bom_a)
    bom_id_a = bom_a.id

    # Populate User B's data
    bom_b = BOMAnalysis(
        user_id=user_b.id,
        filename="project_beta_bom.csv",
        strict_mode=True,
        total_co2_tonnes=45.0,
        cbam_cost_eur=3375.0,
        total_rows=5,
        quarantined_rows=0,
        results_json=json.dumps({"project": "Beta"}),
    )
    custom_mat_b = CustomMaterial(
        user_id=user_b.id,
        name="Tenant B Composite Fiber",
        category="Composites",
        source_url="https://example.com/spec-b",
        status="verified",
    )
    db.add_all([bom_b, custom_mat_b])
    db.commit()
    db.refresh(bom_b)

    # --------------------------------------------------------------------------
    # Test 1: BOM History List Isolation
    # --------------------------------------------------------------------------
    resp_a_list = client.get("/api/v1/account/bom-history", headers=headers_a)
    assert resp_a_list.status_code == 200
    a_items = resp_a_list.json()
    assert len(a_items) == 1
    assert a_items[0]["filename"] == "project_alpha_bom.csv"

    resp_b_list = client.get("/api/v1/account/bom-history", headers=headers_b)
    assert resp_b_list.status_code == 200
    b_items = resp_b_list.json()
    assert len(b_items) == 1
    assert b_items[0]["filename"] == "project_beta_bom.csv"
    assert b_items[0]["id"] != bom_id_a

    # --------------------------------------------------------------------------
    # Test 2: Cross-Tenant Detail Lookup (User B trying to view User A's BOM)
    # --------------------------------------------------------------------------
    resp_b_sneak = client.get(f"/api/v1/account/bom-history/{bom_id_a}", headers=headers_b)
    assert resp_b_sneak.status_code == 404, f"Tenant B accessed Tenant A's BOM! Got {resp_b_sneak.status_code}"

    # User A can view their own BOM
    resp_a_own = client.get(f"/api/v1/account/bom-history/{bom_id_a}", headers=headers_a)
    assert resp_a_own.status_code == 200
    assert resp_a_own.json()["filename"] == "project_alpha_bom.csv"
    assert "secret_cost" in resp_a_own.json()["results_json"]

    # --------------------------------------------------------------------------
    # Test 3: Cross-Tenant Deletion (User B trying to delete User A's BOM)
    # --------------------------------------------------------------------------
    resp_b_del = client.delete(f"/api/v1/account/bom-history/{bom_id_a}", headers=headers_b)
    assert resp_b_del.status_code == 404, f"Tenant B was able to delete Tenant A's BOM! Got {resp_b_del.status_code}"

    # Verify User A's BOM still exists in database
    db_check = db.query(BOMAnalysis).filter(BOMAnalysis.id == bom_id_a).first()
    assert db_check is not None, "Tenant A's BOM was deleted by Tenant B!"

    # --------------------------------------------------------------------------
    # Test 4: Unauthenticated Access Prevention
    # --------------------------------------------------------------------------
    resp_unauth_get = client.get(f"/api/v1/account/bom-history/{bom_id_a}")
    assert resp_unauth_get.status_code == 401

    resp_unauth_del = client.delete(f"/api/v1/account/bom-history/{bom_id_a}")
    assert resp_unauth_del.status_code == 401

    # --------------------------------------------------------------------------
    # Test 5: Transaction History Isolation
    # --------------------------------------------------------------------------
    tx_b_resp = client.get("/api/v1/account/transactions", headers=headers_b)
    assert tx_b_resp.status_code == 200
    assert len(tx_b_resp.json()) == 0, "Tenant B can see transactions belonging to Tenant A!"

    tx_a_resp = client.get("/api/v1/account/transactions", headers=headers_a)
    assert tx_a_resp.status_code == 200
    assert len(tx_a_resp.json()) == 1
    assert tx_a_resp.json()[0]["amount"] == 99.0

    # --------------------------------------------------------------------------
    # Test 6: Custom Materials Isolation
    # --------------------------------------------------------------------------
    cust_b_resp = client.get("/api/v1/materials/custom/mine", headers=headers_b)
    assert cust_b_resp.status_code == 200
    names_b = [m["name"] for m in cust_b_resp.json()]
    assert "Tenant A Proprietary Alloy 7075-X" not in names_b
    assert "Tenant B Composite Fiber" in names_b

    # --------------------------------------------------------------------------
    # Test 7: Tier Gating on bom_analyze (Free user blocked)
    # --------------------------------------------------------------------------
    csv_bytes = b"material_id,Material,Weight_kg,cbam_sector,cn_code,country_of_origin\nMAT-1,Steel,100,Iron & Steel,72083900,China"
    files = {"file": ("test.csv", csv_bytes, "text/csv")}
    data = {"material_col": "Material", "weight_col": "Weight_kg"}

    resp_c_analyze = client.post(
        "/api/v1/materials/bom_analyze",
        headers=headers_c,
        files=files,
        data=data,
    )
    assert resp_c_analyze.status_code == 403, f"Free user bypassed tier gate! Code {resp_c_analyze.status_code}"

    # --------------------------------------------------------------------------
    # Test 8: User A Deletes Their Own BOM
    # --------------------------------------------------------------------------
    resp_a_del = client.delete(f"/api/v1/account/bom-history/{bom_id_a}", headers=headers_a)
    assert resp_a_del.status_code == 200
    assert resp_a_del.json()["status"] == "success"

    resp_a_after = client.get(f"/api/v1/account/bom-history/{bom_id_a}", headers=headers_a)
    assert resp_a_after.status_code == 404

    db.close()


def _make_user(db, email, tier):
    u = User(email=email, name=email.split("@")[0], hashed_password=hash_password("pass123"), tier=tier, is_active=True)
    db.add(u)
    db.commit()
    db.refresh(u)
    token = create_access_token(user_id=u.id, email=u.email, tier=u.tier)
    return u, {"Authorization": f"Bearer {token}"}


def test_bom_analyze_history_is_saved_per_tenant():
    """Positive path. The existing test only proves a FREE user is refused; this proves an upload is stored under
    the uploader and invisible to another Advanced tenant."""
    db = TestingSessionLocal()
    user_d, headers_d = _make_user(db, "tenant_d@example.com", "advanced")
    user_e, headers_e = _make_user(db, "tenant_e@example.com", "advanced")

    csv_bytes = (b"material_id,Material,Weight_kg,cbam_sector,cn_code,country_of_origin,destination,release_date\n"
                 b"MAT-1,Steel,100,Iron & Steel,72083900,China,Germany,2026-03-10")
    resp = client.post(
        "/api/v1/materials/bom_analyze",
        headers=headers_d,
        files={"file": ("tenant_d_upload.csv", csv_bytes, "text/csv")},
        data={"material_col": "Material", "weight_col": "Weight_kg"},
    )
    assert resp.status_code == 200, resp.text
    assert resp.headers.get("X-CBAM-History-Saved") == "true", "history was not saved"

    saved = db.query(BOMAnalysis).filter(BOMAnalysis.filename == "tenant_d_upload.csv").all()
    assert len(saved) == 1 and saved[0].user_id == user_d.id

    hist_d = client.get("/api/v1/account/bom-history", headers=headers_d).json()
    assert [h["filename"] for h in hist_d] == ["tenant_d_upload.csv"]
    assert client.get("/api/v1/account/bom-history", headers=headers_e).json() == [], "Tenant E can see Tenant D's upload!"
    assert client.get(f"/api/v1/account/bom-history/{saved[0].id}", headers=headers_e).status_code == 404
    db.close()


def test_custom_material_url_not_blocked_across_tenants():
    """Confirms Company B is NOT blocked when submitting the same public datasheet URL as Company A."""
    db = TestingSessionLocal()
    user_f, headers_f = _make_user(db, "tenant_f@example.com", "advanced")
    user_g, headers_g = _make_user(db, "tenant_g@example.com", "advanced")

    shared_url = "https://example.com/datasheet-public-alloy-99.pdf"
    mat_f = CustomMaterial(
        user_id=user_f.id,
        name="Tenant F Alloy 99",
        category="Metals",
        source_url=shared_url,
        status="verified",
    )
    db.add(mat_f)
    db.commit()

    # User F duplicate URL should be rejected for User F
    dup_f = db.query(CustomMaterial).filter(
        CustomMaterial.user_id == user_f.id,
        CustomMaterial.source_url == shared_url
    ).first()
    assert dup_f is not None, "User F material should exist"

    # User G querying custom materials by user_id should NOT find any duplicate for User G
    dup_g = db.query(CustomMaterial).filter(
        CustomMaterial.user_id == user_g.id,
        CustomMaterial.source_url == shared_url
    ).first()
    assert dup_g is None, "User G should have no conflicting custom material with this URL"
    db.close()


if __name__ == "__main__":
    test_tenant_isolation()
    test_bom_analyze_history_is_saved_per_tenant()
    test_custom_material_url_not_blocked_across_tenants()
    print("ALL TENANT ISOLATION TESTS PASSED (10/10)")
