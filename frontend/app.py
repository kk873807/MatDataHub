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

# ── Custom CSS ──
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    .compare-better { color: #28a745; font-weight: 600; }
    .compare-worse  { color: #dc3545; }
</style>
""", unsafe_allow_html=True)


# ── Header ──
st.markdown('<p class="main-header">MatDataHub</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Engineering Material Properties Database  |  Search, Filter & Compare</p>', unsafe_allow_html=True)


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
    """Make an AUTHENTICATED API GET request with automatic retries for cold starts.

    Sends the logged-in user's token (if any) via get_auth_headers(), so the
    backend can identify the caller and apply per-tier rate limiting.

    Returns {"ok": True, "data": <json>} on success, or
    {"ok": False, "error": <message>, "url": <url>, "status_code": <int>} on failure.
    A non-2xx HTTP response (e.g. 401/403/404/422/429/500) is treated as a failure,
    not silently wrapped as "ok" data.
    """
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
                # Client errors (4xx) won't fix themselves on retry.
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


def fetch_all_materials():
    """Fetch all materials from the API with retry."""
    return api_get("/materials/", params={"per_page": 200})


@st.cache_data(ttl=300)
def fetch_material_detail(mat_id):
    """Fetch a single material's full details."""
    result = api_get(f"/materials/{mat_id}")
    if result["ok"]:
        return result["data"]
    return None


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
        st.plotly_chart(fig, config={"staticPlot": True}, use_container_width=True)
        st.caption("🔒 Static preview — ⭐ upgrade to Pro for an interactive chart (hover values, toggle materials on/off).")
    else:
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,  # hide the whole toolbar (no zoom, pan, etc.)
                "scrollZoom": False,
            },
        )
        st.caption("Hover over the shape for exact values. Click a material's name in the legend to toggle it on/off. Note: for Density and Cost, *lower* is usually better.")

# ══════════════════════════════════════════════
#  SIDEBAR: Account (Login / Register / Profile)
# ══════════════════════════════════════════════

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None

TIER_BADGES = {"free": "🆓 Free", "pro": "⭐ Pro", "advanced": "🚀 Advanced"}

with st.sidebar:
    st.markdown("### 🔐 Account")

    if st.session_state.token and st.session_state.user:
        # ── Logged in view ──
        user = st.session_state.user
        tier_badge = TIER_BADGES.get(user.get("tier", "free"), "🆓 Free")
        st.success(f"Welcome, **{user.get('name') or user['email']}**!")
        st.caption(f"Tier: {tier_badge}")

        if user.get("api_key"):
            with st.expander("🔑 API Key"):
                st.code(user["api_key"], language="text")

        if st.button("Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()

    else:
        # ── Login / Register tabs ──
        auth_tab = st.radio("", ["Login", "Register"], horizontal=True, label_visibility="collapsed")

        if auth_tab == "Login":
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login", use_container_width=True)

                if submitted and email and password:
                    result = api_post("/auth/login", {"email": email, "password": password})
                    if result["ok"]:
                        st.session_state.token = result["data"]["access_token"]
                        # Fetch full profile
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
                        # Fetch full profile
                        profile = api_get_auth("/auth/me")
                        if profile["ok"]:
                            st.session_state.user = profile["data"]
                        else:
                            st.session_state.user = {"email": email, "tier": "free", "name": name}
                        st.rerun()
                    else:
                        st.error(result.get("error", "Registration failed"))

    st.divider()


# ══════════════════════════════════════════════
#  TABS: Browse | Compare
# ══════════════════════════════════════════════
tab_browse, tab_compare = st.tabs(["Browse Materials", "Compare Materials"])


# ══════════════════════════════════════════════
#  TAB 1: BROWSE (existing functionality)
# ══════════════════════════════════════════════
with tab_browse:

    # ── Sidebar Filters ──
    with st.sidebar:
        st.header("Filters")

        category = st.selectbox(
            "Material Category",
            ["All", "Metal", "Polymer", "Ceramic", "Composite"],
            index=0,
        )

        st.divider()
        st.subheader("Mechanical Properties")

        min_tensile = st.number_input(
            "Min Tensile Strength (MPa)", min_value=0, max_value=5000, value=0, step=50,
        )

        st.subheader("Cost")
        max_cost = st.number_input(
            "Max Cost (Rs./kg)", min_value=0, max_value=10000, value=0, step=50,
            help="Set to 0 for no limit",
        )

        st.subheader("Thermal")
        min_thermal = st.number_input(
            "Min Thermal Conductivity W/(m*K)", min_value=0.0, max_value=500.0, value=0.0, step=5.0,
            help="Set to 0 for no limit",
        )

        st.divider()
        per_page = st.selectbox("Results per page", [10, 20, 50], index=1)

    # ── Search bar ──
    search_query = st.text_input(
        "Search materials by name, grade, standard, or application...",
        placeholder="e.g. stainless, 6061, aerospace, corrosion",
    )

    # ── Build API call ──
    with st.spinner("Loading materials (API may take ~30s on first load)..."):
        wake_api()  # ping root to trigger cold start
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
        # ── Summary metrics ──
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

        # ── Results Table ──
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

            # ── Detail View ──
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

    # Tier-based cap on how many materials this user can select (UI courtesy —
    # the backend /materials/compare endpoint enforces this for real).
    user_tier = (st.session_state.user or {}).get("tier", "free")
    compare_max = FRONTEND_COMPARE_MAX.get(user_tier, 2)

    # Even "unlimited" (advanced, compare_max=99) shouldn't render 99 dropdowns —
    # cap the number of *slots shown* at a sane UI limit. The backend is the
    # real source of truth for what's actually allowed.
    UI_MAX_SELECTORS = min(compare_max, 8)

    st.caption(f"Your **{TIER_BADGES.get(user_tier, user_tier)}** tier allows comparing up to **{compare_max}** materials at once.")

    # ── Material selectors — rendered dynamically, up to UI_MAX_SELECTORS ──
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
        # Single backend call — server validates & enforces compare_max for real.
        ids = [name_to_id[name] for name in selections]
        with st.spinner("Loading comparison..."):
            compare_result = api_get("/materials/compare", params={"ids": ids})

        if not compare_result["ok"]:
            show_api_error(compare_result, retry_key="retry_compare_fetch")
            st.stop()

        mat_details = compare_result["data"]

        st.divider()

        # ── Comparison Table ──
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

        # Build comparison data
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
        # Ensure all columns are strings for clean display
        for col in compare_df.columns:
            compare_df[col] = compare_df[col].astype(str)

        st.markdown("#### Properties Comparison")
        st.dataframe(compare_df, width='stretch', hide_index=True, height=735)

        # ── Bar Charts ──
        st.divider()
        # ── Radar Chart ──
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
                    # Truncate long names for chart readability
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

        # ── Key Differences Summary ──
        st.divider()
        st.markdown("#### Key Takeaways")

        # Auto-generate comparison insights (based on the first two selected materials)
        insights = []
        m0, m1 = mat_details[0], mat_details[1]

        # Strength comparison
        t0 = m0.get("tensile_strength_max")
        t1 = m1.get("tensile_strength_max")
        if t0 is not None and t1 is not None and min(t0, t1) > 0:
            stronger = selections[0] if t0 > t1 else selections[1]
            pct = abs(t0 - t1) / min(t0, t1) * 100
            insights.append(f"**{stronger}** is **{pct:.0f}% stronger** in tensile strength")

        # Weight comparison
        d0 = m0.get("density")
        d1 = m1.get("density")
        if d0 is not None and d1 is not None and max(d0, d1) > 0:
            lighter = selections[0] if d0 < d1 else selections[1]
            pct = abs(d0 - d1) / max(d0, d1) * 100
            insights.append(f"**{lighter}** is **{pct:.0f}% lighter**")

        # Cost comparison
        c0 = m0.get("cost_per_kg_min")
        c1 = m1.get("cost_per_kg_min")
        if c0 is not None and c1 is not None and max(c0, c1) > 0:
            cheaper = selections[0] if c0 < c1 else selections[1]
            pct = abs(c0 - c1) / max(c0, c1) * 100
            insights.append(f"**{cheaper}** is **{pct:.0f}% cheaper**")

        # Thermal comparison
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


# ── Footer ──
st.divider()
st.caption("MatDataHub v0.2 | Engineering Material Data-as-a-Service | 75 materials | Data from MatWeb, MakeItFrom, BIS, ASM")
