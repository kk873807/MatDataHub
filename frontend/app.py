"""
MatDataHub — Streamlit Frontend MVP

A searchable, filterable engineering material database with side-by-side comparison.
Connects to the FastAPI backend.

Run with:
    streamlit run frontend/app.py
"""
import os
import time
from urllib.parse import urlparse

import pandas as pd
import requests
import streamlit as st
import plotly.graph_objects as go


# ── Config ──
# Priority: st.secrets > env var > hardcoded Render URL
RENDER_API = "https://matdatahub-api.onrender.com/api/v1"

def get_api_base():
    # 1. Streamlit Cloud secrets (highest priority)
    try:
        url = st.secrets["API_BASE_URL"]
        if url:
            return url
    except Exception:
        pass
    # 2. Environment variable (for local dev)
    env_url = os.getenv("API_BASE_URL")
    if env_url:
        return env_url
    # 3. Default to Render production URL
    return RENDER_API

API_BASE = get_api_base()
print(f"[MatDataHub] Using API_BASE = {API_BASE}")  # visible in Streamlit Cloud logs

st.set_page_config(
    page_title="MatDataHub",
    page_icon=":hammer_and_wrench:",
    layout="wide",
)


def upgrade_tier(tier: str):
    """
    Requests a Razorpay Payment Link for the selected tier and renders a checkout button.
    """
    token = st.session_state.get("token")
    if not token:
        st.sidebar.error("Please log in first.")
        return
    try:
        resp = requests.post(
            f"{API_BASE}/payments/create-link",
            json={"tier": tier},
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        if resp.status_code == 200:
            data = resp.json()
            payment_url = data.get("payment_url")
            if payment_url:
                st.sidebar.markdown(f'**[🚀 Click here to Pay Securely via Razorpay]({payment_url})**')
                st.sidebar.info("After payment, please refresh your profile to see the upgraded tier.")
            else:
                st.sidebar.error("Failed to generate payment URL.")
        else:
            st.sidebar.error(f"Payment request failed: {resp.json().get('detail', 'Unknown error')}")
    except Exception as e:
        st.sidebar.error(f"Couldn't reach the server: {e}")


# ── Custom CSS ──
st.markdown("""
<style>
    .block-container { padding-top: 4rem !important; }
    .hero-title {
        font-size: 7.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1E3A5F 0%, #2E86AB 50%, #4FC3A1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.1rem;
        margin-top: 0;
        letter-spacing: -1.5px;
        line-height: 1.1;
    }
    .hero-sub {
        font-size: 1.25rem;
        color: #555;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    .stat-card {
        background: linear-gradient(135deg, #f8f9fb 0%, #eef2f7 100%);
        border-radius: 14px;
        padding: 18px 10px;
        text-align: center;
        border: 1px solid #e3e8ef;
    }
    .stat-num { font-size: 1.8rem; font-weight: 700; color: #1E3A5F; }
    .stat-label { font-size: 0.85rem; color: #777; }
    .feature-card {
        background: white;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #e8ecf1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        height: 100%;
    }
    .feature-card h4 { margin-bottom: 6px; color: #1E3A5F; }
    .feature-card p { color: #666; font-size: 0.92rem; margin: 0; }
    .compare-better { color: #28a745; font-weight: 600; }
    .compare-worse  { color: #dc3545; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  Auth helpers
# ══════════════════════════════════════════════

def get_auth_headers():
    """Return auth headers if user is logged in."""
    token = st.session_state.get("token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def api_post(path, json_data=None, timeout=30):
    """Make an API POST request. Returns {"ok": True, "data": ...} or {"ok": False, ...}."""
    url = f"{API_BASE}{path}"
    try:
        r = requests.post(url, json=json_data, headers=get_auth_headers(), timeout=timeout)
        payload = r.json()
        if r.status_code >= 400:
            return {"ok": False, "error": payload.get("detail", str(payload)), "status_code": r.status_code}
        return {"ok": True, "data": payload}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


def api_get_auth(path, timeout=30):
    """Make an authenticated API GET request (no retry — for profile etc.)."""
    url = f"{API_BASE}{path}"
    try:
        r = requests.get(url, headers=get_auth_headers(), timeout=timeout)
        payload = r.json()
        if r.status_code >= 400:
            return {"ok": False, "error": payload.get("detail", str(payload)), "status_code": r.status_code}
        return {"ok": True, "data": payload}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


# ══════════════════════════════════════════════
#  Helper: API calls with retry for Render cold starts
# ══════════════════════════════════════════════

def api_get(path, params=None, retries=3, timeout=60):
    """Make an AUTHENTICATED API GET request with automatic retries for cold starts."""
    url = f"{API_BASE}{path}"
    last_err = None
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, headers=get_auth_headers(), timeout=timeout)
            try:
                payload = r.json()
            except ValueError:
                payload = None

            if r.status_code == 401:
                return {
                    "ok": False,
                    "error": "You need to be logged in to do this. Please sign in from the sidebar.",
                    "url": url,
                    "status_code": 401,
                }

            if r.status_code == 403:
                detail = payload.get("detail") if isinstance(payload, dict) else "Not allowed on your current tier."
                return {"ok": False, "error": detail, "url": url, "status_code": 403}

            if r.status_code == 429:
                detail = payload.get("detail") if isinstance(payload, dict) else "Rate limit exceeded."
                return {"ok": False, "error": detail, "url": url, "status_code": 429}

            if r.status_code >= 400:
                last_err = f"HTTP {r.status_code}: {payload if payload is not None else r.text[:200]}"
                if r.status_code < 500:
                    return {"ok": False, "error": last_err, "url": url, "status_code": r.status_code}
                if attempt < retries - 1:
                    time.sleep(5)
                continue

            return {"ok": True, "data": payload}
        except Exception as e:
            last_err = f"Attempt {attempt+1}: {type(e).__name__}: {e}"
            if attempt < retries - 1:
                time.sleep(5)
    return {"ok": False, "error": last_err, "url": url}


def wake_api():
    """Ping the API root to trigger Render cold start."""
    try:
        parsed = urlparse(API_BASE)
        root_url = f"{parsed.scheme}://{parsed.netloc}/"
        requests.get(root_url, timeout=10)
    except Exception:
        pass


@st.cache_data(ttl=600)
def fetch_all_materials():
    """Fetch all materials from the API with retry. Cached for 10 minutes to improve performance."""
    return api_get("/materials/", params={"per_page": 1000})


@st.cache_data(ttl=300)
def fetch_material_detail(mat_id):
    """Fetch a single material's full details."""
    result = api_get(f"/materials/{mat_id}")
    if result["ok"]:
        return result["data"]
    return None


def submit_feedback(name, email, category, message, rating, page_context):
    """Submit user feedback to the backend. Works for anonymous or logged-in users."""
    body = {
        "name": name or None,
        "email": email or None,
        "category": category,
        "message": message,
        "rating": rating,
        "page_context": page_context,
    }
    return api_post("/feedback/", body)


def show_api_error(result, retry_key):
    """Render a friendly error, with special handling for 401/403/429."""
    status = result.get("status_code")
    if status == 401:
        st.warning(f"🔒 {result.get('error')}")
    elif status == 403:
        st.warning(f"⭐ {result.get('error')}")
    elif status == 429:
        st.warning(f"🚦 {result.get('error')}")
    else:
        st.error("❌ Could not reach the API server.")
        st.code(f"URL: {result.get('url', 'N/A')}\nError: {result.get('error', 'Unknown')}", language="text")
        if st.button("🔄 Retry", key=retry_key):
            st.rerun()


# Mirrors backend TIER_LIMITS[tier]["compare_max"] (app/auth.py) — used here
# only to shape the UI (hide/disable selectors). The backend's /materials/compare
# endpoint is the actual enforcement point; this is a courtesy, not security.
FRONTEND_COMPARE_MAX = {"free": 2, "pro": 5, "advanced": 99}

# ══════════════════════════════════════════════
#  Radar Chart helpers (8e)
# ══════════════════════════════════════════════

RADAR_PROPS = [
    ("Tensile Strength", "tensile_strength_max"),
    ("Yield Strength", "yield_strength_max"),
    ("Elastic Modulus", "elastic_modulus"),
    ("Thermal Conductivity", "thermal_conductivity"),
    ("Density", "density"),
    ("Cost", "cost_per_kg_max"),
]


def _normalize(val, min_v, max_v):
    """Scale a value to 0-100 based on the min/max seen across all materials."""
    if val is None or min_v is None or max_v is None or max_v == min_v:
        return 0
    return round((val - min_v) / (max_v - min_v) * 100, 1)


def _compute_radar_data(mat_details, all_materials):
    """Build {property_label: [normalized_value_per_selected_material]}."""
    radar_data = {}
    for label, key in RADAR_PROPS:
        all_vals = [m.get(key) for m in all_materials if m.get(key) is not None]
        if not all_vals:
            continue
        min_v, max_v = min(all_vals), max(all_vals)
        radar_data[label] = [_normalize(m.get(key), min_v, max_v) for m in mat_details]
    return radar_data


def render_radar_chart(selections, mat_details, all_materials, tier):
    """Render a Plotly radar chart. Free tier = static preview, Pro+ = interactive."""
    radar_data = _compute_radar_data(mat_details, all_materials)
    if not radar_data:
        st.info("Not enough numeric data on these materials to draw a radar chart.")
        return

    categories = list(radar_data.keys())
    fig = go.Figure()

    for i, name in enumerate(selections):
        values = [radar_data[cat][i] for cat in categories]
        values += values[:1]  # close the shape
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill="toself",
            name=name,
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=450,
        margin=dict(l=40, r=40, t=30, b=30),
    )

    if tier == "free":
        st.plotly_chart(fig, config={"staticPlot": True}, width="stretch")
        st.caption("🔒 Static preview — ⭐ upgrade to Pro for an interactive chart (hover values, toggle materials on/off).")
    else:
        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False,
                "scrollZoom": False,
            },
        )
        st.caption("Hover over the shape for exact values. Click a material's name in the legend to toggle it on/off. Note: for Density and Cost, *lower* is usually better.")

# ══════════════════════════════════════════════
#  SIDEBAR: Account (Login / Register / Profile)
# ══════════════════════════════════════════════

saved_token = st.query_params.get("t")

if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None

if saved_token and not st.session_state.token:
    st.session_state.token = saved_token
    try:
        r = requests.get(f"{API_BASE}/auth/me", headers={"Authorization": f"Bearer {saved_token}"}, timeout=5)
        if r.status_code == 200:
            st.session_state.user = r.json()
        else:
            st.session_state.token = None
            if "t" in st.query_params:
                del st.query_params["t"]
    except:
        pass



TIER_BADGES = {"free": "🆓 Free", "pro": "⭐ Pro", "advanced": "🚀 Advanced"}

with st.sidebar:
    st.markdown("### 🔐 Account")

    if st.session_state.token and st.session_state.user:
        user = st.session_state.user
        current_tier = user.get("tier", "free")
        tier_badge = TIER_BADGES.get(current_tier, "🆓 Free")
        upgrade_status = user.get("upgrade_status")
        requested_tier = user.get("requested_tier")

        st.success(f"Welcome, **{user.get('name') or user['email']}**!")
        st.caption(f"Tier: {tier_badge}")

        st.markdown("---")
        if upgrade_status == "pending":
            st.info(f"⏳ Your request to upgrade to **{requested_tier}** is pending approval.")
            if st.button("🔄 Check status"):
                profile = api_get_auth("/auth/me")
                if profile["ok"]:
                    st.session_state.user = profile["data"]
                    st.rerun()
                else:
                    st.error(profile.get("error", "Could not refresh status."))
        elif current_tier == "free":
            st.caption("Upgrades are reviewed manually — you'll see a pending badge after requesting.")
            if st.button("⭐ Request Upgrade to Pro — ₹499/mo"):
                upgrade_tier("pro")
            if st.button("🚀 Request Upgrade to Advanced — ₹1499/mo"):
                upgrade_tier("advanced")
        elif current_tier == "pro":
            st.caption("Upgrades are reviewed manually — you'll see a pending badge after requesting.")
            if st.button("🚀 Request Upgrade to Advanced — ₹1499/mo"):
                upgrade_tier("advanced")
        else:
            st.success("You're on the Advanced plan 🚀")



        if st.button("Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            if "t" in st.query_params:
                del st.query_params["t"]
            st.rerun()

    else:
        auth_tab = st.radio("Auth mode", ["Login", "Register"], horizontal=True, label_visibility="collapsed")

        if auth_tab == "Login":
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login", use_container_width=True)

                if submitted and email and password:
                    result = api_post("/auth/login", {"email": email, "password": password})
                    if result["ok"]:
                        st.session_state.token = result["data"]["access_token"]
                        st.query_params["t"] = result["data"]["access_token"]
                        profile = api_get_auth("/auth/me")
                        if profile["ok"]:
                            st.session_state.user = profile["data"]
                        else:
                            st.session_state.user = {"email": email, "tier": result["data"]["tier"], "name": result["data"].get("name")}
                        st.rerun()
                    else:
                        st.error(result.get("error", "Login failed"))

        else:  # Register
            with st.form("register_form"):
                name = st.text_input("Name (optional)")
                email = st.text_input("Email")
                password = st.text_input("Password (min 6 chars)", type="password")
                submitted = st.form_submit_button("Create Account", use_container_width=True)

                if submitted and email and password:
                    body = {"email": email, "password": password}
                    if name:
                        body["name"] = name
                    result = api_post("/auth/register", body)
                    if result["ok"]:
                        st.session_state.token = result["data"]["access_token"]
                        st.query_params["t"] = result["data"]["access_token"]
                        profile = api_get_auth("/auth/me")
                        if profile["ok"]:
                            st.session_state.user = profile["data"]
                        else:
                            st.session_state.user = {"email": email, "tier": "free", "name": name}
                        st.rerun()
                    else:
                        st.error(result.get("error", "Registration failed"))

    st.divider()

    # ── Admin panel: approve/reject pending upgrade requests + view feedback ──
    with st.expander("🛠️ Admin"):
        admin_pw = st.text_input("Admin password", type="password", key="admin_pw")
        if admin_pw:
            admin_headers = {"X-Admin-Secret": admin_pw}
            try:
                r = requests.get(f"{API_BASE}/admin/upgrade-requests", headers=admin_headers, timeout=15)
                if r.status_code == 403:
                    st.error("Wrong password.")
                elif r.status_code != 200:
                    st.error(f"Error: {r.status_code}")
                else:
                    pending = r.json()
                    st.markdown("**⏳ Pending Upgrade Requests**")
                    if not pending:
                        st.caption("No pending requests.")
                    for req in pending:
                        st.markdown(f"**{req['email']}** ({req.get('name') or '—'})")
                        st.caption(f"{req['current_tier']} → {req['requested_tier']}  ·  {req['requested_at']}")
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("✅ Approve", key=f"approve_{req['id']}"):
                                ar = requests.post(
                                    f"{API_BASE}/admin/upgrade-requests/{req['id']}/approve",
                                    headers=admin_headers, timeout=15,
                                )
                                if ar.status_code == 200:
                                    st.success(ar.json()["message"])
                                else:
                                    st.error(ar.json().get("detail", "Approve failed"))
                                st.rerun()
                        with c2:
                            if st.button("❌ Reject", key=f"reject_{req['id']}"):
                                rr = requests.post(
                                    f"{API_BASE}/admin/upgrade-requests/{req['id']}/reject",
                                    headers=admin_headers, timeout=15,
                                )
                                if rr.status_code == 200:
                                    st.success(rr.json()["message"])
                                else:
                                    st.error(rr.json().get("detail", "Reject failed"))
                                st.rerun()
                        st.divider()
            except Exception as e:
                st.error(f"Couldn't reach server: {e}")

            # ── Recent Feedback ──
            st.markdown("**📬 Recent Feedback**")
            try:
                fr = requests.get(f"{API_BASE}/feedback/", headers=admin_headers, timeout=15)
                if fr.status_code == 403:
                    st.error("Wrong password.")
                elif fr.status_code != 200:
                    st.caption(f"Could not load feedback ({fr.status_code}).")
                else:
                    fb_list = fr.json()
                    if not fb_list:
                        st.caption("No feedback yet.")
                    for item in fb_list[:20]:
                        stars = "⭐" * (item.get("rating") or 0)
                        st.markdown(f"**{item['category']}** {stars} — *{item.get('name') or 'Anonymous'}*")
                        st.caption(item["message"])
                        st.caption(f"{item.get('email','—')} · {item['created_at']} · {item['status']}")
                        st.divider()
            except Exception as e:
                st.caption(f"Error loading feedback: {e}")
                
# ══════════════════════════════════════════════
#  PAGE HEADER — always visible above all tabs
# ══════════════════════════════════════════════
st.markdown('<p class="hero-title">🔧 MatDataHub</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">The engineering material database that gets you to the right material, faster — '
    'search, filter, and compare 500+ metals, polymers, ceramics & composites side by side.</p>',
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════
#  TABS: Home | Browse | Compare | Feedback
# ══════════════════════════════════════════════
tab_home, tab_browse, tab_compare, tab_ai, tab_feedback = st.tabs(
    ["🏠 Home", "🔍 Browse Materials", "⚖️ Compare Materials", "🤖 AI Advisor (Pro)", "💬 Feedback"]
)


# ══════════════════════════════════════════════
#  TAB 0: HOME
# ══════════════════════════════════════════════
with tab_home:

    if st.session_state.get("user"):
        st.info(f"👋 Welcome back, **{st.session_state.user.get('name') or st.session_state.user['email']}**! "
                f"Jump into **Browse Materials** or **Compare Materials** using the tabs above.")
    else:
        st.info("👋 New here? Browse materials freely — sign in from the sidebar to unlock comparisons, "
                "similarity search, and saved history.")

    st.markdown("#### At a glance")
    s1, s2, s3, s4 = st.columns(4)
    for col, num, label in [
        (s1, "500+", "Materials"),
        (s2, "4", "Categories"),
        (s3, "20+", "Properties Tracked"),
        (s4, "ASTM · ASM · ISO", "Data Sources"),
    ]:
        with col:
            st.markdown(
                f'<div class="stat-card"><div class="stat-num">{num}</div><div class="stat-label">{label}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("####  ")
    st.markdown("#### Why MatDataHub")
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown(
            '<div class="feature-card"><h4>🔍 Smart Search & Filters</h4>'
            '<p>Search by name, grade, standard, or application — then narrow by strength, cost, or thermal conductivity.</p></div>',
            unsafe_allow_html=True,
        )
    with f2:
        st.markdown(
            '<div class="feature-card"><h4>⚖️ Side-by-Side Compare</h4>'
            '<p>Put up to 5 materials head-to-head with auto-generated insights and radar charts.</p></div>',
            unsafe_allow_html=True,
        )
    with f3:
        st.markdown(
            '<div class="feature-card"><h4>🎯 Find Similar Materials</h4>'
            '<p>Discover close alternatives to any material based on real property data — great for substitutions.</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown("####  ")
    st.markdown("#### Data Sources & Authenticity 📚")
    st.info("""
    **MatDataHub aggregates material property data strictly from highly trusted engineering standards and industry handbooks.** 
    We do not rely on unverified sources. All properties are derived from:
    
    * **ASTM International** (American Society for Testing and Materials)
    * **ASM International** (Metals Handbooks & Aerospace Materials)
    * **BIS** (Bureau of Indian Standards codes)
    * **MMPDS** (Metallic Materials Properties Development and Standardization)
    * **ISO & EN** (European standards for polymers and composites)
    
    *Note: Mechanical properties are typical minimums. Cost data (₹/kg) represents approximate market ranges.*
    """)

    st.markdown("####  ")
    st.markdown("#### Get started")
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("**🔍 Browse Materials** — head to the *Browse Materials* tab above to search and filter the full database.")
    with g2:
        st.markdown("**⚖️ Compare Materials** — head to the *Compare Materials* tab to pick 2+ materials and see them side by side.")

    st.markdown("####  ")
    st.caption("Have an idea or spotted an issue? Use the **💬 Feedback** tab — we read every submission.")


# ══════════════════════════════════════════════
#  TAB 1: BROWSE
# ══════════════════════════════════════════════
with tab_browse:

    search_query = st.text_input(
        "Search materials by name, grade, standard, or application...",
        placeholder="e.g. stainless, 6061, aerospace, corrosion",
    )

    with st.expander("🔍 Filters", expanded=True):
        fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns(5)

        with fcol1:
            category = st.selectbox(
                "Material Category",
                ["All", "Metal", "Polymer", "Ceramic", "Composite"],
                index=0,
            )

        with fcol2:
            min_tensile = st.number_input(
                "Min Tensile Strength (MPa)", min_value=0, max_value=5000, value=0, step=50,
            )

        with fcol3:
            max_cost = st.number_input(
                "Max Cost (Rs./kg)", min_value=0, max_value=10000, value=0, step=50,
                help="Set to 0 for no limit",
            )

        with fcol4:
            min_thermal = st.number_input(
                "Min Thermal Conductivity W/(m*K)", min_value=0.0, max_value=500.0, value=0.0, step=5.0,
                help="Set to 0 for no limit",
            )

        with fcol5:
            per_page = st.selectbox("Results per page", [10, 20, 50], index=1)

    with st.spinner("Loading materials (API may take ~30s on first load)..."):
        wake_api()
        if search_query:
            params = {"q": search_query, "per_page": per_page}
            result = api_get("/materials/search", params=params)
        else:
            params = {"per_page": per_page}
            if category != "All":
                params["category"] = category
            if min_tensile > 0:
                params["min_tensile"] = min_tensile
            if max_cost > 0:
                params["max_cost"] = max_cost
            if min_thermal > 0:
                params["min_thermal_conductivity"] = min_thermal
            result = api_get("/materials/", params=params)

    if not result["ok"]:
        show_api_error(result, retry_key="retry_browse")
    elif "total" not in result["data"]:
        st.warning("⏳ API returned unexpected data. Please refresh.")
    else:
        data = result["data"]
        total = data["total"]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Materials Found", total)
        with col2:
            active_filters = sum([
                category != "All", min_tensile > 0, max_cost > 0,
                min_thermal > 0, bool(search_query),
            ])
            st.metric("Active Filters", active_filters)
        with col3:
            st.metric("Page", f"{data['page']} of {max(1, (total + per_page - 1) // per_page)}")

        st.divider()

        if total == 0:
            st.info("No materials match your search/filter criteria. Try adjusting your filters.")
        else:
            materials = data["materials"]

            table_data = []
            for m in materials:
                tensile = ""
                if m.get("tensile_strength_min") is not None:
                    if m["tensile_strength_min"] == m.get("tensile_strength_max"):
                        tensile = f"{m['tensile_strength_min']:.0f}"
                    else:
                        tensile = f"{m['tensile_strength_min']:.0f}-{m['tensile_strength_max']:.0f}"

                cost = ""
                if m.get("cost_per_kg_min") is not None:
                    cost = f"{m['cost_per_kg_min']:.0f}-{m['cost_per_kg_max']:.0f}"

                table_data.append({
                    "ID": m["id"],
                    "Name": m["name"],
                    "Category": m["category"],
                    "Grade": m.get("grade", ""),
                    "Standard": m.get("standard", ""),
                    "Density (g/cm3)": m.get("density", ""),
                    "Tensile (MPa)": tensile,
                    "Cost (Rs./kg)": cost,
                    "Applications": (m.get("applications", "") or "")[:80],
                })

            df = pd.DataFrame(table_data)
            st.dataframe(df, width='stretch', hide_index=True)

            st.divider()
            st.subheader("Material Detail View")

            material_names = {m["name"]: m["id"] for m in materials}
            selected_name = st.selectbox("Select a material to view full details:", list(material_names.keys()))

            if selected_name:
                mat_id = material_names[selected_name]
                m = fetch_material_detail(mat_id)

                if m is None:
                    st.warning("Could not load material details. Please refresh.")
                else:
                    left, right = st.columns(2)

                    with left:
                        st.markdown("#### Identity")
                        st.write(f"**Name:** {m['name']}")
                        st.write(f"**Category:** {m['category']} / {m.get('subcategory', 'N/A')}")
                        st.write(f"**Grade:** {m.get('grade', 'N/A')}")
                        st.write(f"**Standard:** {m.get('standard', 'N/A')}")
                        if m.get("equivalent_grades"):
                            st.write(f"**Equivalent Grades:** {m['equivalent_grades']}")
                        if m.get("composition"):
                            st.write(f"**Composition:** {m['composition']}")

                        st.markdown("#### Mechanical Properties")
                        mech_data = {}
                        if m.get("density") is not None:
                            mech_data["Density (g/cm3)"] = str(m["density"])
                        if m.get("tensile_strength_min") is not None:
                            mech_data["Tensile Strength (MPa)"] = f"{m['tensile_strength_min']} - {m['tensile_strength_max']}"
                        if m.get("yield_strength_min") is not None:
                            mech_data["Yield Strength (MPa)"] = f"{m['yield_strength_min']} - {m['yield_strength_max']}"
                        if m.get("elongation") is not None:
                            mech_data["Elongation (%)"] = str(m["elongation"])
                        if m.get("hardness"):
                            mech_data["Hardness"] = m["hardness"]
                        if m.get("elastic_modulus") is not None:
                            mech_data["Elastic Modulus (GPa)"] = str(m["elastic_modulus"])
                        if mech_data:
                            st.table(pd.DataFrame(mech_data.items(), columns=["Property", "Value"]))

                    with right:
                        st.markdown("#### Thermal Properties")
                        therm_data = {}
                        if m.get("thermal_conductivity") is not None:
                            therm_data["Thermal Conductivity W/(m*K)"] = str(m["thermal_conductivity"])
                        if m.get("specific_heat") is not None:
                            therm_data["Specific Heat J/(kg*K)"] = str(m["specific_heat"])
                        if m.get("melting_point_min") is not None:
                            therm_data["Melting Point (C)"] = f"{m['melting_point_min']} - {m['melting_point_max']}"
                        if m.get("max_service_temp") is not None:
                            therm_data["Max Service Temp (C)"] = str(m["max_service_temp"])
                        if therm_data:
                            st.table(pd.DataFrame(therm_data.items(), columns=["Property", "Value"]))

                        st.markdown("#### Cost & Sourcing")
                        if m.get("cost_per_kg_min") is not None:
                            st.write(f"**Price Range:** Rs. {m['cost_per_kg_min']} - {m['cost_per_kg_max']} /kg")
                        if m.get("source_name"):
                            st.write(f"**Data Source:** {m['source_name']}")
                        verified = "Yes" if m.get("is_verified") else "No"
                        st.write(f"**Verified:** {verified}")

                        if m.get("applications"):
                            st.markdown("#### Applications")
                            st.write(m["applications"])

                    st.divider()
                    user_tier = (st.session_state.user or {}).get("tier", "free")

                    if user_tier in ("pro", "advanced"):
                        if st.button(f"🔍 Find Materials Similar to {m['name']}", key=f"similar_{mat_id}"):
                            with st.spinner("Finding similar materials..."):
                                sim_result = api_get(f"/materials/{mat_id}/similar", params={"limit": 5})
                            if sim_result["ok"]:
                                st.markdown(f"#### Top 5 Materials Similar to **{m['name']}**")
                                sim_data = []
                                for s in sim_result["data"]:
                                    sim_data.append({
                                        "Name": s["name"],
                                        "Category": s["category"],
                                        "Grade": s.get("grade", "-"),
                                        "Density": s.get("density", "-"),
                                        "Tensile Max (MPa)": s.get("tensile_strength_max", "-"),
                                        "Cost Max (₹/kg)": s.get("cost_per_kg_max", "-"),
                                    })
                                st.dataframe(pd.DataFrame(sim_data), width="stretch", hide_index=True)
                            else:
                                show_api_error(sim_result, retry_key=f"retry_similar_{mat_id}")
                    else:
                        st.info("🔍 **Find Similar Materials** — Discover alternatives you never knew about! ⭐ Upgrade to Pro to unlock.")


# ══════════════════════════════════════════════
#  TAB 2: COMPARE MATERIALS
# ══════════════════════════════════════════════
with tab_compare:

    st.subheader("Side-by-Side Material Comparison")
    st.caption("Select 2 or 3 materials to compare their properties head-to-head.")

    with st.spinner("Loading material list (API may take ~30s on first load)..."):
        wake_api()
        all_result = fetch_all_materials()

    if not all_result["ok"]:
        show_api_error(all_result, retry_key="retry_compare")
        st.stop()

    if "materials" not in all_result.get("data", {}):
        st.warning("⏳ API returned unexpected data. Please refresh.")
        if st.button("🔄 Retry", key="retry_compare_data"):
            st.rerun()
        st.stop()

    all_materials = all_result["data"].get("materials", [])
    name_to_id = {m["name"]: m["id"] for m in all_materials}
    sorted_names = sorted(name_to_id.keys())

    user_tier = (st.session_state.user or {}).get("tier", "free")
    compare_max = FRONTEND_COMPARE_MAX.get(user_tier, 2)

    UI_MAX_SELECTORS = min(compare_max, 8)

    st.caption(f"Your **{TIER_BADGES.get(user_tier, user_tier)}** tier allows comparing up to **{compare_max}** materials at once.")

    selections = []
    SELECTORS_PER_ROW = 4
    for row_start in range(0, UI_MAX_SELECTORS, SELECTORS_PER_ROW):
        row_count = min(SELECTORS_PER_ROW, UI_MAX_SELECTORS - row_start)
        row_cols = st.columns(row_count)
        for i in range(row_count):
            slot_num = row_start + i + 1
            with row_cols[i]:
                label = f"Material {slot_num}" + (" (optional)" if slot_num > 2 else "")
                choice = st.selectbox(label, ["-- Select --"] + sorted_names, key=f"cmp{slot_num}")
                if choice != "-- Select --":
                    selections.append(choice)

    if compare_max > UI_MAX_SELECTORS:
        st.caption(f"Showing {UI_MAX_SELECTORS} slots. Your tier technically allows up to {compare_max} — let us know if you need more at once.")
    elif user_tier == "free":
        st.caption("⭐ Upgrade to Pro to compare up to 5 materials at once.")

    if len(selections) < 2:
        st.info("Select at least 2 materials above to start comparing.")
    else:
        ids = [name_to_id[name] for name in selections]
        with st.spinner("Loading comparison..."):
            compare_result = api_get("/materials/compare", params={"ids": ids})

        if not compare_result["ok"]:
            show_api_error(compare_result, retry_key="retry_compare_fetch")
            st.stop()

        mat_details = compare_result["data"]

        st.divider()

        COMPARE_PROPS = [
            ("Category",               "category",              None),
            ("Subcategory",             "subcategory",           None),
            ("Grade",                   "grade",                 None),
            ("Standard",               "standard",              None),
            ("Density (g/cm3)",         "density",               "lower"),
            ("Tensile Strength (MPa)",  "tensile_strength_max",  "higher"),
            ("Yield Strength (MPa)",    "yield_strength_max",    "higher"),
            ("Elongation (%)",          "elongation",            "higher"),
            ("Hardness",                "hardness",              None),
            ("Elastic Modulus (GPa)",   "elastic_modulus",       "higher"),
            ("Thermal Conductivity W/(m*K)", "thermal_conductivity", "higher"),
            ("Specific Heat J/(kg*K)",  "specific_heat",         None),
            ("Melting Point Max (C)",   "melting_point_max",     "higher"),
            ("Max Service Temp (C)",    "max_service_temp",      "higher"),
            ("Cost Min (Rs./kg)",       "cost_per_kg_min",       "lower"),
            ("Cost Max (Rs./kg)",       "cost_per_kg_max",       "lower"),
            ("Composition",             "composition",           None),
            ("Applications",            "applications",          None),
            ("Equivalent Grades",       "equivalent_grades",     None),
            ("Data Source",             "source_name",           None),
        ]

        rows = []
        for label, key, best_dir in COMPARE_PROPS:
            row = {"Property": label}
            values = []
            for i, m in enumerate(mat_details):
                val = m.get(key)
                row[selections[i]] = val if val is not None else "-"
                if best_dir and val is not None and isinstance(val, (int, float)):
                    values.append((i, val))
            rows.append(row)

        compare_df = pd.DataFrame(rows)
        for col in compare_df.columns:
            compare_df[col] = compare_df[col].astype(str)

        st.markdown("#### Properties Comparison")
        st.dataframe(compare_df, width='stretch', hide_index=True, height=735)

        st.divider()
        st.markdown("#### 🕸️ Radar Chart — Property Fingerprint")
        render_radar_chart(selections, mat_details, all_materials, user_tier)
        st.markdown("#### Visual Comparison")

        CHART_PROPS = [
            ("Tensile Strength (MPa)", "tensile_strength_max"),
            ("Yield Strength (MPa)", "yield_strength_max"),
            ("Density (g/cm3)", "density"),
            ("Elastic Modulus (GPa)", "elastic_modulus"),
            ("Thermal Conductivity W/(m*K)", "thermal_conductivity"),
            ("Cost (Rs./kg)", "cost_per_kg_max"),
        ]

        chart_col1, chart_col2 = st.columns(2)

        for idx, (chart_label, chart_key) in enumerate(CHART_PROPS):
            chart_data = {}
            for name, m in zip(selections, mat_details):
                val = m.get(chart_key)
                if val is not None and isinstance(val, (int, float)):
                    short_name = name[:25] + "..." if len(name) > 28 else name
                    chart_data[short_name] = val

            if len(chart_data) >= 2:
                target_col = chart_col1 if idx % 2 == 0 else chart_col2
                with target_col:
                    st.markdown(f"**{chart_label}**")
                    chart_df = pd.DataFrame(
                        {"Material": list(chart_data.keys()), "Value": list(chart_data.values())}
                    )
                    st.bar_chart(chart_df, x="Material", y="Value", horizontal=False)

        st.divider()
        st.markdown("#### Key Takeaways")

        insights = []
        m0, m1 = mat_details[0], mat_details[1]

        t0 = m0.get("tensile_strength_max")
        t1 = m1.get("tensile_strength_max")
        if t0 is not None and t1 is not None and min(t0, t1) > 0:
            stronger = selections[0] if t0 > t1 else selections[1]
            pct = abs(t0 - t1) / min(t0, t1) * 100
            insights.append(f"**{stronger}** is **{pct:.0f}% stronger** in tensile strength")

        d0 = m0.get("density")
        d1 = m1.get("density")
        if d0 is not None and d1 is not None and max(d0, d1) > 0:
            lighter = selections[0] if d0 < d1 else selections[1]
            pct = abs(d0 - d1) / max(d0, d1) * 100
            insights.append(f"**{lighter}** is **{pct:.0f}% lighter**")

        c0 = m0.get("cost_per_kg_min")
        c1 = m1.get("cost_per_kg_min")
        if c0 is not None and c1 is not None and max(c0, c1) > 0:
            cheaper = selections[0] if c0 < c1 else selections[1]
            pct = abs(c0 - c1) / max(c0, c1) * 100
            insights.append(f"**{cheaper}** is **{pct:.0f}% cheaper**")

        th0 = m0.get("thermal_conductivity")
        th1 = m1.get("thermal_conductivity")
        if th0 is not None and th1 is not None:
            better_cond = selections[0] if th0 > th1 else selections[1]
            factor = max(th0, th1) / max(min(th0, th1), 0.01)
            insights.append(f"**{better_cond}** conducts heat **{factor:.1f}x better**")

        if insights:
            for insight in insights:
                st.markdown(f"- {insight}")
        else:
            st.write("Select materials with more numeric properties for auto-generated insights.")


# ══════════════════════════════════════════════
#  TAB: AI ADVISOR
# ══════════════════════════════════════════════
with tab_ai:
    st.markdown("### 🤖 Engineering AI Advisor")
    
    if not st.session_state.get("user"):
        st.warning("You must be logged in to access the AI Advisor.")
    else:
        tier = st.session_state.user.get("tier", "free")
        if tier == "free":
            st.info("🔒 **Premium Feature Locked**")
            st.markdown("The AI Advisor analyzes your natural language requirements (e.g. *'Need a lightweight, high-strength metal for a drone under Rs. 1000/kg'*), intelligently queries the database, and provides engineering recommendations.")
            st.markdown("Upgrade to **Pro** or **Advanced** to unlock this feature.")
            if st.button("🚀 Upgrade to Pro (Rs. 499/mo)", key="ai_upgrade"):
                upgrade_tier("pro")
        else:
            st.markdown("Describe your material requirements and let the AI find the best matches from our 600+ materials.")
            
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # React to user input
            if prompt := st.chat_input("E.g., I need a corrosion-resistant metal that can withstand 500°C..."):
                # Display user message in chat message container
                st.chat_message("user").markdown(prompt)
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing constraints and querying database..."):
                        resp = api_post("/ai/advise", {"prompt": prompt})
                        if resp["ok"]:
                            response_text = resp["data"]["response"]
                            st.markdown(response_text)
                            st.session_state.messages.append({"role": "assistant", "content": response_text})
                        else:
                            err = resp.get("error", "Unknown error")
                            if resp.get("status_code") == 403:
                                st.error("Access denied. Please ensure you are on a paid tier.")
                            else:
                                st.error(f"AI Error: {err}")

# ══════════════════════════════════════════════
#  TAB: FEEDBACK
# ══════════════════════════════════════════════
with tab_feedback:
    st.markdown("## 💬 We'd love your feedback")
    st.caption("Found a bug? Want a new feature? Just want to say hi? Tell us below.")

    user = st.session_state.get("user")
    default_name = user.get("name", "") if user else ""
    default_email = user.get("email", "") if user else ""

    with st.form("feedback_form", clear_on_submit=True):
        fcol1, fcol2 = st.columns(2)
        with fcol1:
            fb_name = st.text_input("Name (optional)", value=default_name)
        with fcol2:
            fb_email = st.text_input("Email (optional)", value=default_email)

        fb_category = st.selectbox(
            "What's this about?",
            ["General Feedback", "Bug Report", "Feature Request", "Data Correction", "Other"],
        )
        fb_rating = st.slider("How's your experience so far?", 1, 5, 4, help="1 = Poor, 5 = Excellent")
        fb_message = st.text_area(
            "Your message",
            placeholder="Tell us what's working, what's not, or what you'd love to see next...",
            height=140,
        )
        fb_submit = st.form_submit_button("📤 Send Feedback", use_container_width=True)

        if fb_submit:
            if not fb_message or len(fb_message.strip()) < 3:
                st.error("Please write a bit more detail before submitting.")
            else:
                result = submit_feedback(
                    fb_name, fb_email, fb_category, fb_message.strip(), fb_rating, "Feedback Tab"
                )
                if result["ok"]:
                    st.success("Thanks! Your feedback has been recorded. 🙌")
                    st.balloons()
                else:
                    st.error(result.get("error", "Couldn't submit feedback. Try again later."))


# ── Footer ──
st.divider()
st.caption("MatDataHub v0.3 | Engineering Material Data-as-a-Service | 500+ materials | Data from ASTM, ASM, MMPDS, ISO, ACI")
