"""
MatDataHub — Streamlit Frontend MVP

A searchable, filterable engineering material database.
Connects to the FastAPI backend running at http://127.0.0.1:8000

Run with:
    streamlit run frontend/app.py
"""
import streamlit as st
import requests
import pandas as pd
import os

# ── Config ──
# Locally: defaults to localhost. In production: set API_BASE_URL env var to your Render URL.
API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api/v1")

st.set_page_config(
    page_title="MatDataHub",
    page_icon=":hammer_and_wrench:",
    layout="wide",
)

# ── Custom CSS for a cleaner look ──
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
    .metric-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 12px 16px;
        border-left: 4px solid #1E3A5F;
    }
    .stDataFrame { font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════
st.markdown('<p class="main-header">MatDataHub</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Engineering Material Properties Database  |  Search, Filter & Compare</p>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  SIDEBAR — Filters
# ══════════════════════════════════════════════
with st.sidebar:
    st.header("Filters")

    # Category filter
    category = st.selectbox(
        "Material Category",
        ["All", "Metal", "Polymer", "Ceramic", "Composite"],
        index=0,
    )

    st.divider()
    st.subheader("Mechanical Properties")

    # Tensile strength range
    min_tensile = st.number_input(
        "Min Tensile Strength (MPa)", min_value=0, max_value=5000, value=0, step=50,
    )

    st.subheader("Cost")

    # Max cost filter
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


# ══════════════════════════════════════════════
#  MAIN AREA — Search + Results
# ══════════════════════════════════════════════

# Search bar
search_query = st.text_input(
    "Search materials by name, grade, standard, or application...",
    placeholder="e.g. stainless, 6061, aerospace, corrosion",
)

# ── Build API call ──
try:
    if search_query:
        # Use search endpoint
        params = {"q": search_query, "per_page": per_page}
        response = requests.get(f"{API_BASE}/materials/search", params=params, timeout=5)
    else:
        # Use list endpoint with filters
        params = {"per_page": per_page}
        if category != "All":
            params["category"] = category
        if min_tensile > 0:
            params["min_tensile"] = min_tensile
        if max_cost > 0:
            params["max_cost"] = max_cost
        if min_thermal > 0:
            params["min_thermal_conductivity"] = min_thermal
        response = requests.get(f"{API_BASE}/materials/", params=params, timeout=5)

    data = response.json()

except requests.exceptions.ConnectionError:
    st.error("Cannot connect to the API server. Make sure it's running:")
    st.code("cd MatDataHub\n.\\venv\\Scripts\\activate\nuvicorn app.main:app --reload", language="powershell")
    st.stop()


# ── Summary metrics ──
total = data["total"]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Materials Found", total)
with col2:
    active_filters = sum([
        category != "All",
        min_tensile > 0,
        max_cost > 0,
        min_thermal > 0,
        bool(search_query),
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

    # Build a clean DataFrame for the table
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
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ── Detail View ──
    st.divider()
    st.subheader("Material Detail View")

    material_names = {m["name"]: m["id"] for m in materials}
    selected_name = st.selectbox("Select a material to view full details:", list(material_names.keys()))

    if selected_name:
        mat_id = material_names[selected_name]
        detail_resp = requests.get(f"{API_BASE}/materials/{mat_id}", timeout=5)
        m = detail_resp.json()

        # Two-column detail layout
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
                mech_data["Density (g/cm3)"] = m["density"]
            if m.get("tensile_strength_min") is not None:
                mech_data["Tensile Strength (MPa)"] = f"{m['tensile_strength_min']} - {m['tensile_strength_max']}"
            if m.get("yield_strength_min") is not None:
                mech_data["Yield Strength (MPa)"] = f"{m['yield_strength_min']} - {m['yield_strength_max']}"
            if m.get("elongation") is not None:
                mech_data["Elongation (%)"] = m["elongation"]
            if m.get("hardness"):
                mech_data["Hardness"] = m["hardness"]
            if m.get("elastic_modulus") is not None:
                mech_data["Elastic Modulus (GPa)"] = m["elastic_modulus"]
            if mech_data:
                st.table(pd.DataFrame(mech_data.items(), columns=["Property", "Value"]))

        with right:
            st.markdown("#### Thermal Properties")
            therm_data = {}
            if m.get("thermal_conductivity") is not None:
                therm_data["Thermal Conductivity W/(m*K)"] = m["thermal_conductivity"]
            if m.get("specific_heat") is not None:
                therm_data["Specific Heat J/(kg*K)"] = m["specific_heat"]
            if m.get("melting_point_min") is not None:
                therm_data["Melting Point (C)"] = f"{m['melting_point_min']} - {m['melting_point_max']}"
            if m.get("max_service_temp") is not None:
                therm_data["Max Service Temp (C)"] = m["max_service_temp"]
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


# ── Footer ──
st.divider()
st.caption("MatDataHub v0.1 | Engineering Material Data-as-a-Service | Data from public references (MatWeb, MakeItFrom, BIS, ASM)")
