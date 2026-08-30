"""
MatDataHub — Streamlit Frontend MVP

A searchable, filterable engineering material database with side-by-side comparison.
Connects to the FastAPI backend.

Run with:
    streamlit run frontend/app.py
"""
import streamlit as st
import requests
import pandas as pd
import os

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
#  Helper: API calls with retry for Render cold starts
# ══════════════════════════════════════════════
import time

def api_get(path, params=None, retries=3, timeout=60):
    """Make an API GET request with automatic retries for cold starts."""
    url = f"{API_BASE}{path}"
    last_err = None
    for attempt in range(retries):
        try:
            print(f"[MatDataHub] api_get attempt {attempt+1}/{retries}: {url}")
            r = requests.get(url, params=params, timeout=timeout)
            print(f"[MatDataHub] api_get success: status={r.status_code}")
            return r.json()
        except Exception as e:
            last_err = e
            print(f"[MatDataHub] api_get attempt {attempt+1} FAILED: {type(e).__name__}: {e}")
            if attempt < retries - 1:
                time.sleep(5)
    print(f"[MatDataHub] api_get all retries exhausted for {url}")
    return None


def fetch_all_materials():
    """Fetch all materials from the API with retry."""
    data = api_get("/materials/", params={"per_page": 200})
    if data and "materials" in data:
        return data
    return None


@st.cache_data(ttl=300)
def fetch_material_detail(mat_id):
    """Fetch a single material's full details."""
    return api_get(f"/materials/{mat_id}")


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
        if search_query:
            params = {"q": search_query, "per_page": per_page}
            data = api_get("/materials/search", params=params)
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
            data = api_get("/materials/", params=params)

    if data is None or "total" not in data:
        st.warning("⏳ The API server is waking up (Render free tier sleeps after inactivity). Please wait 30-60 seconds and refresh the page.")
    else:
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
        all_data = fetch_all_materials()
    if all_data is None:
        st.warning("The API server is waking up (Render free tier sleeps after inactivity). Please wait 30-60 seconds and refresh the page.")
        st.stop()

    all_materials = all_data.get("materials", [])
    name_to_id = {m["name"]: m["id"] for m in all_materials}
    sorted_names = sorted(name_to_id.keys())

    # ── Material selectors ──
    sel_cols = st.columns(3)
    selections = []

    with sel_cols[0]:
        mat1 = st.selectbox("Material 1", ["-- Select --"] + sorted_names, key="cmp1")
        if mat1 != "-- Select --":
            selections.append(mat1)

    with sel_cols[1]:
        mat2 = st.selectbox("Material 2", ["-- Select --"] + sorted_names, key="cmp2")
        if mat2 != "-- Select --":
            selections.append(mat2)

    with sel_cols[2]:
        mat3 = st.selectbox("Material 3 (optional)", ["-- Select --"] + sorted_names, key="cmp3")
        if mat3 != "-- Select --":
            selections.append(mat3)

    if len(selections) < 2:
        st.info("Select at least 2 materials above to start comparing.")
    else:
        # Fetch full details for each
        mat_details = []
        for name in selections:
            mid = name_to_id[name]
            detail = fetch_material_detail(mid)
            mat_details.append(detail)

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

        # Auto-generate comparison insights
        insights = []
        m0, m1 = mat_details[0], mat_details[1]

        # Strength comparison
        t0 = m0.get("tensile_strength_max")
        t1 = m1.get("tensile_strength_max")
        if t0 and t1:
            stronger = selections[0] if t0 > t1 else selections[1]
            pct = abs(t0 - t1) / min(t0, t1) * 100
            insights.append(f"**{stronger}** is **{pct:.0f}% stronger** in tensile strength")

        # Weight comparison
        d0 = m0.get("density")
        d1 = m1.get("density")
        if d0 and d1:
            lighter = selections[0] if d0 < d1 else selections[1]
            pct = abs(d0 - d1) / max(d0, d1) * 100
            insights.append(f"**{lighter}** is **{pct:.0f}% lighter**")

        # Cost comparison
        c0 = m0.get("cost_per_kg_min")
        c1 = m1.get("cost_per_kg_min")
        if c0 and c1:
            cheaper = selections[0] if c0 < c1 else selections[1]
            pct = abs(c0 - c1) / max(c0, c1) * 100
            insights.append(f"**{cheaper}** is **{pct:.0f}% cheaper**")

        # Thermal comparison
        th0 = m0.get("thermal_conductivity")
        th1 = m1.get("thermal_conductivity")
        if th0 and th1:
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
