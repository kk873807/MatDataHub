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
import plotly.express as px


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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Typography & Background */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    .block-container { padding-top: 3rem !important; }

    /* Modern Hero Title with animated gradient */
    .hero-title {
        font-size: 4.5rem;
        font-weight: 800;
        background: linear-gradient(270deg, #1E3A5F, #2E86AB, #4FC3A1, #1E3A5F);
        background-size: 300% 300%;
        animation: gradient-shift 8s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        margin-top: 0;
        letter-spacing: -2px;
        line-height: 1.1;
        text-align: center;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .hero-sub {
        font-size: 1.25rem;
        color: var(--text-color);
        opacity: 0.7;
        margin-bottom: 2rem;
        font-weight: 400;
        text-align: center;
        width: 100%;
        
        
    }

        /* Glassmorphism Stat Cards */
    .stat-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 24px 15px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease;
    }
    .stat-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px 0 rgba(31, 38, 135, 0.15);
        border-color: rgba(79, 195, 161, 0.4);
    }
    .stat-num { font-size: 2.2rem; font-weight: 800; color: var(--primary-color, #4FC3A1); margin-bottom: 5px; }
    .stat-label { font-size: 0.9rem; color: var(--text-color); opacity: 0.7; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; }

    /* Feature Cards */
    .feature-card {
        background: var(--secondary-background-color);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        height: 100%;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        border-color: var(--primary-color);
    }
    .feature-card h4 { margin-bottom: 10px; color: var(--text-color); font-weight: 700; }
    .feature-card p { color: var(--text-color); opacity: 0.8; font-size: 0.95rem; margin: 0; line-height: 1.6; }

    /* Review Cards */
    .review-card {
        background: var(--secondary-background-color);
        border-left: 4px solid var(--primary-color);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        transition: transform 0.2s ease;
    }
    .review-card:hover {
        transform: translateX(5px);
    }
    .review-name { font-weight: 700; font-size: 1.1rem; color: var(--text-color); }
    .review-stars { color: #FFD700; font-size: 1.1rem; letter-spacing: 2px; }
    .review-text { color: var(--text-color); opacity: 0.8; font-style: italic; margin-top: 8px; }

    /* Customizing Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: var(--secondary-background-color);
        border-radius: 8px;
        color: var(--text-color);
        opacity: 0.8;
        padding: 0 20px;
        border: 1px solid transparent;
        transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(79, 195, 161, 0.1) !important;
        color: #4FC3A1 !important;
        border: 1px solid rgba(79, 195, 161, 0.3) !important;
        font-weight: 600;
        opacity: 1;
    }
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
        try:
            payload = r.json()
        except Exception:
            return {"ok": False, "error": f"Server Error ({r.status_code}): {r.text[:200]}"}
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

    # Modern vibrant colors
    hex_colors = ["#4FC3A1", "#2E86AB", "#FFCA28", "#FF6B6B"]
    fill_colors = ["rgba(79, 195, 161, 0.3)", "rgba(46, 134, 171, 0.3)", "rgba(255, 202, 40, 0.3)", "rgba(255, 107, 107, 0.3)"]

    for i, name in enumerate(selections):
        values = [radar_data[cat][i] for cat in categories]
        values += values[:1]  # close the shape
        c_idx = i % len(hex_colors)
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill="toself",
            name=name,
            line=dict(color=hex_colors[c_idx], width=3, shape='linear'),
            fillcolor=fill_colors[c_idx],
            marker=dict(size=8, symbol='circle', color=hex_colors[c_idx], line=dict(width=1, color='white'))
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor="rgba(128,128,128,0.15)"),
            angularaxis=dict(gridcolor="rgba(128,128,128,0.15)", tickfont=dict(size=12, color="gray"))
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
        height=500,
        margin=dict(l=40, r=40, t=60, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif")
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
                        st.caption(f"{item.get('email','—')} • {item['created_at']} • {item['status']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("🗑️ Delete", key=f"del_fb_{item['id']}"):
                                dr = requests.delete(f"{API_BASE}/feedback/{item['id']}", headers=admin_headers)
                                if dr.status_code == 200:
                                    st.success("Deleted!")
                                    st.rerun()
                        with col2:
                            if item.get("user_id"):
                                if st.button("🚫 Block User", key=f"block_user_{item['id']}"):
                                    br = requests.post(f"{API_BASE}/admin/users/{item['user_id']}/block", headers=admin_headers)
                                    if br.status_code == 200:
                                        st.success("Blocked!")
                                        st.rerun()
                        st.divider()
            except Exception as e:
                st.caption(f"Error loading feedback: {e}")
                

# ══════════════════════════════════════════════
#  PAGE HEADER
# ══════════════════════════════════════════════
st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 class="hero-title">MatDataHub</h1>
        <p class="hero-sub">The ultimate engineering material data-as-a-service platform. Discover, compare, and analyze over 500+ industrial materials instantly.</p>
    </div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TABS: Home | Browse | Compare | Feedback
# ══════════════════════════════════════════════
tab_home, tab_browse, tab_compare, tab_projects, tab_ai, tab_feedback = st.tabs(
    ["🏠 Home", "🔍 Browse", "⚖️ Compare", "📁 My Projects (BOM)", "🧠 AI Advisor (Pro)", "💬 Feedback"]
)


# ══════════════════════════════════════════════
#  TAB 0: HOME
# ══════════════════════════════════════════════
with tab_home:


    if st.session_state.get("user"):
        st.markdown(f"""
            <div style="background: rgba(79, 195, 161, 0.1); border: 1px solid rgba(79, 195, 161, 0.3); border-radius: 8px; padding: 12px 20px; color: #4FC3A1; margin-bottom: 2rem; font-weight: 500; text-align: center;">
                ✨ Welcome back, {st.session_state.user.get('name') or st.session_state.user['email']}! Jump into Browse Materials or Compare Materials using the tabs above.
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background: rgba(46, 134, 171, 0.1); border: 1px solid rgba(46, 134, 171, 0.3); border-radius: 8px; padding: 12px 20px; color: #2E86AB; margin-bottom: 2rem; font-weight: 500; text-align: center;">
                👋 New here? Browse materials freely — sign in from the sidebar to unlock intelligent comparisons and the AI Advisor.
            </div>
        """, unsafe_allow_html=True)

    st.markdown("#### At a glance")
    s1, s2, s3, s4 = st.columns(4)
    for col, num, label in [
        (s1, "500+", "Materials"),
        (s2, "4", "Categories"),
        (s3, "20+", "Properties Tracked"),
        (s4, "ASTM / ISO", "Global Standards"),
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

    # ══════════════════════════════════════════════
    # COMMUNITY REVIEWS SECTION
    # ══════════════════════════════════════════════
    st.divider()
    st.markdown("## 💬 Community Reviews & Discussion")
    st.markdown("See what other engineers are saying about MatDataHub, reply to their feedback, and join the discussion!")

    try:
        rev_resp = api_get("/feedback/public")
        if rev_resp["ok"] and rev_resp["data"]:
            reviews = rev_resp["data"]
            total_stars = sum(r.get("rating") or 0 for r in reviews if r.get("rating"))
            rated_reviews = [r for r in reviews if r.get("rating")]
            avg_rating = total_stars / len(rated_reviews) if rated_reviews else 0
            
            c1, c2 = st.columns([1, 3])
            with c1:
                st.metric("Average Rating", f"{avg_rating:.1f} ⭐")
                st.caption(f"Based on {len(rated_reviews)} rated reviews")
            
            with c2:
                # Build tree
                fb_map = {item["id"]: {**item, "children": []} for item in reviews}
                tree = []
                for item in reviews:
                    pid = item.get("parent_id")
                    if pid and pid in fb_map:
                        fb_map[pid]["children"].append(fb_map[item["id"]])
                    else:
                        tree.append(fb_map[item["id"]])
                
                # Recursive render function
                def render_comments(comments, depth=0):
                    for c in comments:
                        with st.container():
                            if depth > 0:
                                col_spacer, col_content = st.columns([0.05 * depth, 1 - (0.05 * depth)])
                            else:
                                col_spacer = None
                                col_content = st.container()
                                
                            with col_content:
                                stars = "⭐" * (c.get("rating") or 0)
                                name = c.get("name") or "Anonymous Engineer"
                                st.markdown(f"**{name}** {stars}")
                                st.write(c["message"])
                                
                                # Buttons
                                btn_cols = st.columns([1.5, 1.5, 2, 4])
                                with btn_cols[0]:
                                    votes = c.get("helpful_votes") or 0
                                    if st.button(f"👍 Helpful ({votes})", key=f"help_{c['id']}"):
                                        requests.post(f"{API_BASE}/feedback/{c['id']}/helpful")
                                        st.rerun()
                                with btn_cols[1]:
                                    if st.button("💬 Reply", key=f"reply_btn_{c['id']}"):
                                        st.session_state[f"show_reply_{c['id']}"] = not st.session_state.get(f"show_reply_{c['id']}", False)
                                        
                                # Admin
                                if st.session_state.get("user") and st.session_state.user.get("role") == "admin":
                                    with btn_cols[2]:
                                        with st.popover("🛡️ Admin"):
                                            if st.button("Hide", key=f"hide_{c['id']}"):
                                                h_headers = {"X-Admin-Secret": os.getenv("ADMIN_SECRET", "sk_test_admin_key")}
                                                requests.patch(f"{API_BASE}/feedback/{c['id']}/visibility", headers=h_headers)
                                                st.rerun()
                                            if st.button("Delete", key=f"del_fb_{c['id']}"):
                                                h_headers = {"X-Admin-Secret": os.getenv("ADMIN_SECRET", "sk_test_admin_key")}
                                                requests.delete(f"{API_BASE}/feedback/{c['id']}", headers=h_headers)
                                                st.rerun()
                                                
                                if st.session_state.get(f"show_reply_{c['id']}", False):
                                    with st.form(f"form_reply_{c['id']}", clear_on_submit=True):
                                        reply_msg = st.text_area("Your reply...")
                                        if st.form_submit_button("Submit Reply"):
                                            if reply_msg and len(reply_msg.strip()) >= 3:
                                                u = st.session_state.get("user", {})
                                                payload = {
                                                    "name": u.get("name", "Anonymous Reply"),
                                                    "email": u.get("email", ""),
                                                    "category": "Reply",
                                                    "message": reply_msg.strip(),
                                                    "page_context": "Community Thread",
                                                    "parent_id": c["id"]
                                                }
                                                resp = requests.post(f"{API_BASE}/feedback/", json=payload)
                                                if resp.status_code == 200:
                                                    st.session_state[f"show_reply_{c['id']}"] = False
                                                    st.success("Reply posted!")
                                                    st.rerun()
                                                else:
                                                    st.error(resp.json().get("detail", "Error"))
                                                    
                        if c["children"]:
                            render_comments(c["children"], depth + 1)
                        if depth == 0:
                            st.divider()

                render_comments(tree[:20]) # Limit top-level to 20 for perf
        else:
            st.info("No reviews yet. Be the first to leave feedback in the Feedback tab!")
    except Exception as e:
        st.error(f"Failed to load community feedback: {e}")

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
            st.dataframe(
                df, 
                width='stretch', 
                hide_index=True,
                column_config={
                    "Name": st.column_config.TextColumn("Material Name", width="medium"),
                    "Category": st.column_config.TextColumn("Category", width="small"),
                    "Tensile (MPa)": st.column_config.TextColumn("Tensile Strength (MPa)", width="medium"),
                    "Cost (Rs./kg)": st.column_config.TextColumn("Cost (Rs./kg)", width="medium"),
                    "Applications": st.column_config.TextColumn("Applications", width="large"),
                }
            )

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
                    fig_bar = px.bar(
                        chart_df, 
                        x="Value", 
                        y="Material", 
                        orientation='h',
                        text_auto='.2s',
                        color="Material",
                        color_discrete_sequence=["#4FC3A1", "#2E86AB", "#FFCA28", "#FF6B6B"]
                    )
                    fig_bar.update_traces(
                        textfont_size=13, 
                        textangle=0, 
                        textposition="outside", 
                        cliponaxis=False,
                        marker_line_width=0
                    )
                    fig_bar.update_layout(
                        showlegend=False,
                        height=180,
                        margin=dict(l=0, r=60, t=10, b=10),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Inter, sans-serif"),
                        xaxis=dict(visible=False, showgrid=False),
                        yaxis=dict(title=None, showgrid=False, tickfont=dict(size=13, color="gray"))
                    )
                    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

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

# ══════════════════════════════════════════════
#  TAB: MY PROJECTS (BOM)
# ══════════════════════════════════════════════
with tab_projects:
    st.markdown("### 📁 Engineering Workspaces & BOM Optimizer")
    
    if not st.session_state.get("user"):
        st.info("You must be logged in to create and manage engineering projects.")
    else:
        tier = st.session_state.user.get("tier", "free")
        if tier == "free":
            st.info("✨ **Premium Feature Locked**")
            st.markdown("Engineering Workspaces allow you to build custom Bill of Materials (BOM) for your products, instantly calculating **Total Mass** and **Total Estimated Cost** based on real-time material data.")
            st.markdown("Upgrade to **Pro** or **Advanced** to unlock this active workspace feature.")
            if st.button("🚀 Upgrade to Pro (Rs. 499/mo)", key="proj_upgrade"):
                upgrade_tier("pro")
        else:
            if tier == "pro":
                st.warning("⚡ **Pro Tier**: You can create up to 3 active projects. Upgrade to **Advanced** for unlimited workspaces and CSV data exports.")
            else:
                st.success("💎 **Advanced Tier**: You have unlimited workspaces and full export capabilities.")
                
            pcol1, pcol2 = st.columns([1, 3])
            
            # Fetch Projects
            projects = []
            proj_resp = requests.get(f"{API_BASE}/projects/", headers=get_auth_headers())
            if proj_resp.status_code == 200:
                projects = proj_resp.json()
                
            with pcol1:
                # Initialize session state for selected project if not present
                if "selected_proj_id" not in st.session_state:
                    st.session_state.selected_proj_id = projects[0]["id"] if projects else None

                # Ensure the selected ID actually exists (in case it was deleted)
                if projects and st.session_state.selected_proj_id not in [p["id"] for p in projects]:
                    st.session_state.selected_proj_id = projects[0]["id"]

                selected_proj_id = st.session_state.get("selected_proj_id")

                # --- 1. CREATE NEW SECTION ---
                st.markdown("##### Create New")
                at_limit = (tier == "pro" and len(projects) >= 3)
                
                if at_limit:
                    st.error("Pro limit reached (3/3). Delete a project or upgrade.")
                    if st.button("🚀 Upgrade to Advanced"):
                        upgrade_tier("advanced")
                else:
                    with st.form("new_proj"):
                        new_name = st.text_input("Project Name")
                        new_desc = st.text_area("Description (optional)", height=60)
                        if st.form_submit_button("Create Project"):
                            if new_name:
                                res = api_post("/projects/", {"name": new_name, "description": new_desc})
                                if res["ok"]:
                                    st.success("Created!")
                                    st.session_state.selected_proj_id = res["data"]["id"]
                                    st.rerun()
                                else:
                                    st.error(res["error"])
                                    
                st.divider()

                # --- 2. YOUR PROJECTS SECTION ---
                st.markdown("#### Your Projects")
                if not projects:
                    st.caption("No projects yet.")
                else:
                    for p in projects:
                        # Highlight the selected project
                        is_selected = (p["id"] == selected_proj_id)
                        
                        # Use a border container for each project to look like a list of cards
                        with st.container(border=True):
                            if is_selected:
                                st.markdown(f"#### 📂 **{p['name']}**")
                            else:
                                st.markdown(f"**{p['name']}**")
                                
                            if not is_selected:
                                if st.button(f"Open Workspace", key=f"open_proj_{p['id']}", use_container_width=True):
                                    st.session_state.selected_proj_id = p["id"]
                                    st.rerun()
                                
            with pcol2:
                if selected_proj_id:
                    curr_proj = next((p for p in projects if p["id"] == selected_proj_id), None)
                    if curr_proj:
                        col_title, col_del = st.columns([4, 1])
                        with col_title:
                            st.markdown(f"### {curr_proj['name']}")
                            if curr_proj['description']:
                                st.caption(curr_proj['description'])
                        with col_del:
                            if st.button("🗑️ Delete", key="del_proj"):
                                requests.delete(f"{API_BASE}/projects/{selected_proj_id}", headers=get_auth_headers())
                                st.rerun()
                                
                        items = curr_proj.get("items", [])
                        
                        # Calculate totals
                        total_weight = 0.0
                        total_cost_min = 0.0
                        total_cost_max = 0.0
                        
                        for item in items:
                            mat = item["material"]
                            vol = item["volume_cm3"]
                            den = mat.get("density") or 0.0
                            mass_kg = (vol * den) / 1000.0  # density is g/cm3, volume is cm3 -> mass in g -> kg
                            total_weight += mass_kg
                            
                            c_min = mat.get("cost_per_kg_min") or 0.0
                            c_max = mat.get("cost_per_kg_max") or 0.0
                            total_cost_min += (mass_kg * c_min)
                            total_cost_max += (mass_kg * c_max)
                        
                        # Dashboard Metrics
                        m1, m2 = st.columns(2)
                        with m1:
                            st.markdown(f'<div class="stat-card" style="padding: 15px;"><div class="stat-label">Total Assembly Mass</div><div class="stat-num">{total_weight:.2f} kg</div></div>', unsafe_allow_html=True)
                        with m2:
                            cost_display = f"Rs. {total_cost_min:,.0f} - {total_cost_max:,.0f}" if total_cost_min > 0 else "Rs. 0"
                            st.markdown(f'<div class="stat-card" style="padding: 15px;"><div class="stat-label">Total Estimated Cost</div><div class="stat-num" style="font-size:1.8rem;">{cost_display}</div></div>', unsafe_allow_html=True)
                        
                        st.write("") # spacing
                        # Define the tabs
                        tab_blueprint, tab_bom, tab_add, tab_import, tab_tools = st.tabs(["📐 Project Blueprint", "📋 Bill of Materials (BOM)", "➕ Add Part to Assembly", "⚡ Smart Import", "🛠️ Advanced Engineering Tools"])
                        
                        with tab_bom:
                            if items:
                                table_data = []
                                for item in items:
                                    mat = item["material"]
                                    vol = item["volume_cm3"]
                                    den = mat.get("density") or 0.0
                                    mass_kg = (vol * den) / 1000.0
                                    table_data.append({
                                        "Part Name": item["part_name"],
                                        "Material": mat["name"],
                                        "Volume (cm³)": f"{vol:,.2f}",
                                        "Mass (kg)": f"{mass_kg:,.3f}",
                                        "Remove": item["id"]
                                    })
                                
                                df = pd.DataFrame(table_data)
                                # Force left-alignment by treating formatted numbers as text
                                st.dataframe(
                                    df.drop(columns=["Remove"]), 
                                    width="stretch", 
                                    hide_index=True
                                )
                                
                                # Advanced Tier: CSV Export
                                if tier == "advanced":
                                    csv_data = df.drop(columns=["Remove"]).to_csv(index=False).encode('utf-8')
                                    st.download_button(
                                        label="📥 Export BOM to CSV",
                                        data=csv_data,
                                        file_name=f"{curr_proj['name'].replace(' ', '_')}_BOM.csv",
                                        mime="text/csv"
                                    )
                                elif tier == "pro":
                                    st.caption("🔒 *Upgrade to Advanced to export this BOM to CSV.*")
                                
                                st.divider()
                                # Simple remove selector
                                rem_id = st.selectbox("Remove a part", options=[0] + [i["Remove"] for i in table_data], format_func=lambda x: "Select to remove..." if x == 0 else next(i["Part Name"] for i in table_data if i["Remove"] == x))
                                if rem_id != 0:
                                    if st.button("Confirm Remove"):
                                        requests.delete(f"{API_BASE}/projects/{selected_proj_id}/items/{rem_id}", headers=get_auth_headers())
                                        st.rerun()
                            else:
                                st.info("No parts added yet. Use the 'Add Part' or 'Smart Import' tabs!")
                        
                        with tab_blueprint:
                            b64 = curr_proj.get("blueprint_data")
                            if b64:
                                st.image(f"data:image/png;base64,{b64}", use_container_width=True)
                                if st.button("Remove Blueprint"):
                                    requests.patch(f"{API_BASE}/projects/{selected_proj_id}/blueprint", json={"blueprint_data": ""}, headers=get_auth_headers())
                                    st.rerun()
                            else:
                                bp_file = st.file_uploader("Upload CAD/Sketch (.png, .jpg)", type=["png", "jpg", "jpeg"])
                                if bp_file:
                                    import base64
                                    b64_str = base64.b64encode(bp_file.read()).decode()
                                    res = requests.patch(f"{API_BASE}/projects/{selected_proj_id}/blueprint", json={"blueprint_data": b64_str}, headers=get_auth_headers())
                                    if res.status_code == 200:
                                        st.rerun()
                                        
                        with tab_add:
                            with st.form("add_part_form"):
                                c1, c2, c3 = st.columns(3)
                                
                                with st.spinner("Loading materials..."):
                                    all_mats = fetch_all_materials()
                                
                                bom_mat_options = {m["id"]: m["name"] for m in all_mats["data"].get("materials", [])} if all_mats["ok"] else {}
                                
                                with c1:
                                    part_name = st.text_input("Part Name", placeholder="e.g. Engine Block")
                                with c2:
                                    sel_mat_id = st.selectbox("Select Material", options=list(bom_mat_options.keys()), format_func=lambda x: bom_mat_options[x])
                                with c3:
                                    vol_cm3 = st.number_input("Volume (cm3)", min_value=0.1, value=100.0, step=10.0)
                                    
                                if st.form_submit_button("Add to BOM"):
                                    if not part_name:
                                        st.error("Part Name is required.")
                                    else:
                                        res = api_post(f"/projects/{selected_proj_id}/items", {"material_id": sel_mat_id, "part_name": part_name, "volume_cm3": vol_cm3})
                                        if res["ok"]:
                                            st.success("Added!")
                                            st.rerun()
                                        else:
                                            st.error(res["error"])
                                            
                        with tab_import:
                            st.caption("Upload a file with columns: Part Name, Material ID, Volume (cm3)")
                            bom_file = st.file_uploader("Upload BOM File", type=["csv", "xlsx"], label_visibility="collapsed")
                            if bom_file and st.button("Auto-Build Project"):
                                try:
                                    import pandas as pd
                                    df_bom = pd.read_csv(bom_file) if bom_file.name.endswith(".csv") else pd.read_excel(bom_file)
                                    if "Part Name" in df_bom.columns and "Material ID" in df_bom.columns and "Volume (cm3)" in df_bom.columns:
                                        with st.spinner("Importing parts..."):
                                            for _, row in df_bom.iterrows():
                                                api_post(f"/projects/{selected_proj_id}/items", {"material_id": int(row["Material ID"]), "part_name": str(row["Part Name"]), "volume_cm3": float(row["Volume (cm3)"])})
                                        st.success("BOM Imported Successfully!")
                                        st.rerun()
                                    else:
                                        st.error("Missing required columns: Part Name, Material ID, Volume (cm3)")
                                except Exception as e:
                                    st.error(f"Failed to parse file: {e}")
                                    
                        with tab_tools:
                            st.info("💡 **Engineer's Note:** All calculations below utilize strict mathematical formulas and dynamically pull empirical properties directly from the materials database. Approximations (such as uncorrected endurance limits) are explicitly stated.")
                            t_synthesizer, t_safety, t_fatigue, t_thermal, t_deflect, t_shock, t_cost = st.tabs(["🧪 Synthesizer", "🛡️ Safety", "🔄 Fatigue", "🌡️ Thermal", "📐 Deflection", "⚡ Shock", "📉 Cost"])
                            
                            with t_synthesizer:
                                st.markdown("#### Rule of Mixtures Synthesizer")
                                st.caption("Estimate the properties of a composite or alloy by blending two materials.")
                                st.latex(r"P_{composite} = P_{matrix} \cdot V_{matrix} + P_{reinforcement} \cdot V_{reinforcement}")
                                
                                with st.spinner("Loading material database..."):
                                    all_mats = fetch_all_materials()
                                    synth_mat_options = {m["id"]: m for m in all_mats["data"].get("materials", [])} if all_mats["ok"] else {}
                                    
                                c_syn1, c_syn2 = st.columns(2)
                                with c_syn1:
                                    m1_id = st.selectbox("Base Material (Matrix)", options=list(synth_mat_options.keys()), format_func=lambda x: synth_mat_options[x]["name"], key="m1")
                                    vol_m1 = st.slider("Volume %", 0, 100, 70)
                                with c_syn2:
                                    m2_id = st.selectbox("Secondary Material (Reinforcement)", options=list(synth_mat_options.keys()), format_func=lambda x: synth_mat_options[x]["name"], key="m2")
                                    vol_m2 = 100 - vol_m1
                                    st.metric("Secondary Volume %", f"{vol_m2}%")
                                    
                                if m1_id and m2_id:
                                    mat1 = synth_mat_options[m1_id]
                                    mat2 = synth_mat_options[m2_id]
                                    
                                    den1 = mat1.get("density") or 0.0
                                    den2 = mat2.get("density") or 0.0
                                    blend_density = (den1 * (vol_m1/100.0)) + (den2 * (vol_m2/100.0))
                                    
                                    ts1 = mat1.get("tensile_strength_max") or mat1.get("tensile_strength_min") or 0.0
                                    ts2 = mat2.get("tensile_strength_max") or mat2.get("tensile_strength_min") or 0.0
                                    blend_ts = (ts1 * (vol_m1/100.0)) + (ts2 * (vol_m2/100.0))
                                    
                                    c_min1 = mat1.get("cost_per_kg_min") or 0.0
                                    c_min2 = mat2.get("cost_per_kg_min") or 0.0
                                    blend_cost = (c_min1 * (vol_m1/100.0)) + (c_min2 * (vol_m2/100.0))
                                    
                                    st.markdown("##### Estimated Composite Properties")
                                    sc1, sc2, sc3 = st.columns(3)
                                    sc1.metric("Blend Density", f"{blend_density:.2f} g/cm³")
                                    sc2.metric("Blend Tensile Strength", f"{blend_ts:.0f} MPa")
                                    sc3.metric("Est. Base Cost", f"Rs. {blend_cost:.0f} /kg")
                                    
                            with t_safety:
                                st.markdown("#### Structural Yield Analyzer")
                                st.caption("Calculate the Safety Factor for a specific part under mechanical load.")
                                st.latex(r"\text{Stress } (\sigma) = \frac{F}{A} \quad \Rightarrow \quad \text{Safety Factor } (SF) = \frac{S_y}{\sigma}")
                                
                                if not items:
                                    st.warning("Add parts to your BOM first.")
                                else:
                                    safe_part_idx = st.selectbox("Select Part to Analyze", options=range(len(items)), format_func=lambda i: f"{items[i]['part_name']} ({items[i]['material']['name']})", key="safety_part")
                                    p_item = items[safe_part_idx]
                                    y_str = p_item["material"].get("yield_strength_min")
                                    
                                    if not y_str:
                                        st.error(f"Material '{p_item['material']['name']}' lacks Yield Strength data.")
                                    else:
                                        f_col1, f_col2 = st.columns(2)
                                        with f_col1:
                                            load_n = st.number_input("Max Applied Force (Newtons)", min_value=1.0, value=5000.0, step=500.0, key="sf_load")
                                        with f_col2:
                                            area_cm2 = st.number_input("Cross-Sectional Area (cm²)", min_value=0.1, value=10.0, step=0.5, key="sf_area")
                                            
                                        stress_mpa = load_n / (area_cm2 * 100.0)
                                        sf = y_str / stress_mpa if stress_mpa > 0 else float('inf')
                                        sf_display = f"{sf:.2f}" if sf < 100 else "100+ (Infinite)"
                                        
                                        st.markdown(f"**Applied Stress:** {stress_mpa:.2f} MPa")
                                        st.markdown(f"**Material Yield Strength ($S_y$):** {y_str:.2f} MPa")
                                        
                                        if sf >= 2.0:
                                            st.success(f"🟢 **Safety Factor: {sf_display}** (Highly Safe)")
                                        elif sf >= 1.0:
                                            st.warning(f"🟡 **Safety Factor: {sf_display}** (Marginal/Warning)")
                                        else:
                                            st.error(f"🔴 **Safety Factor: {sf_display}** (Critical Failure Expected!)")
                                            
                            with t_fatigue:
                                st.markdown("#### Cyclic Fatigue Life Estimator")
                                st.caption("Estimate if a part will survive infinite cycles under alternating stress.")
                                st.latex(r"S_e \approx k_a k_b k_c k_d k_e k_f \cdot S_e'")
                                st.info("Note: The baseline endurance limit (Se') is uncorrected. You can apply standard Marin modification factors below to calculate the true Corrected Endurance Limit (Se).")
                                
                                if not items:
                                    st.warning("Add parts to your BOM first.")
                                else:
                                    fat_part_idx = st.selectbox("Select Part to Analyze", options=range(len(items)), format_func=lambda i: f"{items[i]['part_name']} ({items[i]['material']['name']})", key="fatigue_part")
                                    p_item = items[fat_part_idx]
                                    mat = p_item["material"]
                                    ts_val = mat.get("tensile_strength_max") or mat.get("tensile_strength_min")
                                    
                                    if not ts_val:
                                        st.error(f"Material '{mat['name']}' lacks Tensile Strength data required for Fatigue Estimation.")
                                    else:
                                        cat = str(mat.get("category", "")).lower()
                                        if "metal" in cat and "aluminum" not in mat["name"].lower():
                                            endurance_limit = ts_val * 0.50 # Steel approx
                                            note = r"Estimated Uncorrected Endurance Limit ($S_e' \approx 0.5 \cdot S_{ut}$)"
                                        elif "aluminum" in mat["name"].lower() or "polymer" in cat:
                                            endurance_limit = ts_val * 0.35 # Al/Polymer approx
                                            note = r"Estimated Fatigue Strength at $5\cdot 10^8$ cycles ($S_f \approx 0.35 \cdot S_{ut}$)"
                                        else:
                                            endurance_limit = ts_val * 0.40
                                            note = r"Estimated Endurance Limit ($S_e' \approx 0.4 \cdot S_{ut}$)"
                                            
                                        st.markdown(f"**Material Tensile Strength ($S_{{ut}}$):** {ts_val:.2f} MPa")
                                        st.markdown(f"**{note}:** {endurance_limit:.2f} MPa")
                                        
                                        with st.expander("⚙️ Apply Marin Modification Factors", expanded=True):
                                            st.caption("Adjust these empirical factors based on manufacturing and environmental conditions.")
                                            mk1, mk2, mk3 = st.columns(3)
                                            with mk1:
                                                k_a = st.number_input("Surface ($k_a$)", min_value=0.1, max_value=2.0, value=1.0, step=0.05, help="Depends on surface finish (e.g. Polished = 1.0, Machined = 0.7, Forged = 0.5)")
                                                k_d = st.number_input("Temperature ($k_d$)", min_value=0.1, max_value=2.0, value=1.0, step=0.05, help="Room temp = 1.0")
                                            with mk2:
                                                k_b = st.number_input("Size ($k_b$)", min_value=0.1, max_value=2.0, value=1.0, step=0.05, help="Depends on part diameter (e.g. d < 8mm = 1.0)")
                                                k_e = st.number_input("Reliability ($k_e$)", min_value=0.1, max_value=1.0, value=1.0, step=0.01, help="e.g. 50% rel = 1.0, 99.9% = 0.753")
                                            with mk3:
                                                k_c = st.number_input("Load ($k_c$)", min_value=0.1, max_value=2.0, value=1.0, step=0.05, help="Bending = 1.0, Axial = 0.85, Torsion = 0.59")
                                                k_f = st.number_input("Misc ($k_f$)", min_value=0.1, max_value=2.0, value=1.0, step=0.05, help="Corrosion, residual stress, etc.")
                                                
                                            k_total = k_a * k_b * k_c * k_d * k_e * k_f
                                            corrected_se = endurance_limit * k_total
                                            
                                            st.info(rf"**Corrected Endurance Limit ($S_e = k_{{total}} \cdot S_e'$): {corrected_se:.2f} MPa**")
                                        
                                        alt_stress = st.number_input("Applied Alternating Stress Amplitude (MPa)", min_value=1.0, value=max(1.0, float(corrected_se*0.8)), step=10.0, key="alt_stress")
                                        
                                        if alt_stress < corrected_se:
                                            st.success("🟢 **Infinite Life Expected** - Alternating stress is below the corrected endurance limit.")
                                        else:
                                            st.error("🔴 **Finite Life (Fatigue Failure)** - The part will eventually crack under cyclic loading.")
                                            
                            with t_thermal:
                                st.markdown("#### Thermal Expansion Simulator")
                                st.caption("Calculate exact dimensional change based on operating temperatures.")
                                st.latex(r"\Delta L = L \cdot \alpha \cdot \Delta T")
                                
                                if not items:
                                    st.warning("Add parts to your BOM first.")
                                else:
                                    therm_part_idx = st.selectbox("Select Part to Analyze", options=range(len(items)), format_func=lambda i: f"{items[i]['part_name']} ({items[i]['material']['name']})", key="therm_part")
                                    p_item = items[therm_part_idx]
                                    mat = p_item["material"]
                                    
                                    cat = str(mat.get("category", "")).lower()
                                    if "polymer" in cat:
                                        cte = 100.0
                                    elif "ceramic" in cat:
                                        cte = 5.0
                                    elif "aluminum" in mat["name"].lower():
                                        cte = 23.0
                                    else:
                                        cte = 12.0
                                        
                                    f1, f2, f3 = st.columns(3)
                                    with f1:
                                        part_length = st.number_input("Part Length (mm)", min_value=1.0, value=500.0, step=10.0)
                                    with f2:
                                        t_initial = st.number_input("Initial Temp (°C)", value=25.0, step=5.0)
                                    with f3:
                                        t_final = st.number_input("Operating Temp (°C)", value=150.0, step=5.0)
                                        
                                    st.caption(rf"Estimated Coefficient of Thermal Expansion ($\alpha$): {cte} µm/m·°C")
                                    delta_t = t_final - t_initial
                                    
                                    expansion_mm = part_length * (cte * 1e-6) * delta_t
                                    
                                    if delta_t > 1500:
                                        st.error("⚠️ **Warning:** Operating temperature is dangerously high and may exceed the melting point of standard alloys.")
                                    elif expansion_mm > 0:
                                        st.warning(f"🔥 The part will **EXPAND** by **{expansion_mm:.4f} mm**")
                                    elif expansion_mm < 0:
                                        st.info(f"❄️ The part will **CONTRACT** by **{abs(expansion_mm):.4f} mm**")
                                    else:
                                        st.success("No dimensional change.")

                            with t_deflect:
                                st.markdown("#### Beam Deflection & Stiffness (Young's Modulus)")
                                st.caption("Calculate how much a part will physically bend under a cantilever load.")
                                st.latex(r"I = \frac{\pi d^4}{64} \quad \Rightarrow \quad \delta_{max} = \frac{F L^3}{3 E I}")
                                
                                if not items:
                                    st.warning("Add parts to your BOM first.")
                                else:
                                    deflect_part_idx = st.selectbox("Select Part to Analyze", options=range(len(items)), format_func=lambda i: f"{items[i]['part_name']} ({items[i]['material']['name']})", key="deflect_part")
                                    p_item = items[deflect_part_idx]
                                    mat = p_item["material"]
                                    
                                    # Try to fetch Elastic Modulus from API (or estimate if not available)
                                    E_gpa = mat.get("elastic_modulus")
                                    if not E_gpa:
                                        cat = str(mat.get("category", "")).lower()
                                        if "polymer" in cat:
                                            E_gpa = 3.0
                                        elif "aluminum" in mat["name"].lower():
                                            E_gpa = 69.0
                                        elif "titanium" in mat["name"].lower():
                                            E_gpa = 110.0
                                        else:
                                            E_gpa = 200.0 # Standard Steel
                                        st.info(f"Elastic Modulus not explicitly in DB. Using estimated value for {cat}: **{E_gpa} GPa**")
                                    else:
                                        st.success(f"**Elastic Modulus ($E$):** {E_gpa} GPa")
                                        
                                    f1, f2, f3 = st.columns(3)
                                    with f1:
                                        force_n = st.number_input("Point Load ($F$) in Newtons", min_value=1.0, value=1000.0, step=100.0)
                                    with f2:
                                        length_mm = st.number_input("Beam Length ($L$) in mm", min_value=10.0, value=300.0, step=10.0)
                                    with f3:
                                        diameter_mm = st.number_input("Shaft Diameter ($d$) in mm", min_value=1.0, value=25.0, step=1.0)
                                        
                                    # Convert to standard units (meters and Pascals)
                                    E_pa = E_gpa * 1e9
                                    L_m = length_mm / 1000.0
                                    d_m = diameter_mm / 1000.0
                                    
                                    import math
                                    I_m4 = (math.pi * (d_m ** 4)) / 64.0
                                    
                                    deflection_m = (force_n * (L_m ** 3)) / (3.0 * E_pa * I_m4)
                                    deflection_mm = deflection_m * 1000.0
                                    
                                    st.markdown(f"**Area Moment of Inertia ($I$):** {I_m4:.2e} m⁴")
                                    st.warning(rf"📐 **Maximum Tip Deflection ($\delta_{{max}}$): {deflection_mm:.4f} mm**")
                                    
                                    if deflection_mm > (length_mm / 100):
                                        st.error("⚠️ **Warning:** Deflection exceeds 1% of beam length. The part lacks sufficient stiffness and may fail due to excessive bending.")

                            with t_shock:
                                st.markdown("#### Thermal Shock & Fracture Estimator")
                                st.caption("Determine a part's resistance to fracturing when quenched or rapidly cooled.")
                                st.latex(r"R_s = \frac{\sigma_f \cdot k}{E \cdot \alpha}")
                                st.info("Higher $R_s$ values indicate better resistance to thermal shock. Commonly used to evaluate machinability and quenching limits.")
                                
                                if not items:
                                    st.warning("Add parts to your BOM first.")
                                else:
                                    shock_part_idx = st.selectbox("Select Part to Analyze", options=range(len(items)), format_func=lambda i: f"{items[i]['part_name']} ({items[i]['material']['name']})", key="shock_part")
                                    p_item = items[shock_part_idx]
                                    mat = p_item["material"]
                                    
                                    sigma_f = mat.get("tensile_strength_max") or mat.get("tensile_strength_min")
                                    E_gpa = mat.get("elastic_modulus")
                                    if not E_gpa:
                                        E_gpa = 200.0 # fallback
                                        
                                    k_cond = mat.get("thermal_conductivity")
                                    if not k_cond:
                                        k_cond = 45.0 # fallback steel
                                        
                                    if not sigma_f:
                                        st.error("Missing Tensile Strength required for calculation.")
                                    else:
                                        cat = str(mat.get("category", "")).lower()
                                        cte = 12.0 # Standard Steel approx
                                        if "polymer" in cat: cte = 100.0
                                        elif "ceramic" in cat: cte = 5.0
                                        elif "aluminum" in mat["name"].lower(): cte = 23.0
                                        
                                        Rs = (sigma_f * k_cond) / (E_gpa * cte)
                                        
                                        sc1, sc2, sc3 = st.columns(3)
                                        sc1.metric(r"Strength ($\sigma_f$)", f"{sigma_f:.1f} MPa")
                                        sc2.metric("Conductivity ($k$)", f"{k_cond:.1f} W/m·K")
                                        sc3.metric(r"Expansion ($\alpha$)", f"{cte:.1f} µm/m·°C")
                                        
                                        st.success(f"⚡ **Thermal Shock Resistance ($R_s$): {Rs:.2f} W/m**")

                            with t_cost:
                                st.markdown("#### 📉 BOM Cost Optimization Engine")
                                st.caption("Scans your Bill of Materials for cheaper materials that maintain or exceed the current Yield Strength.")
                                if not items:
                                    st.warning("Add parts to your BOM first.")
                                else:
                                    if st.button("Run Optimization Engine", type="primary"):
                                        with st.spinner("Scanning database for cost-effective equivalents..."):
                                            all_mats = fetch_all_materials()
                                            db_mats = all_mats["data"].get("materials", []) if all_mats["ok"] else []
                                            
                                            optimization_found = False
                                            for item in items:
                                                curr_mat = item["material"]
                                                curr_ys = curr_mat.get("yield_strength_min")
                                                curr_cost = curr_mat.get("cost_per_kg_min")
                                                
                                                if curr_ys and curr_cost:
                                                    # Find cheaper alternatives in same category
                                                    alts = [m for m in db_mats 
                                                            if m["category"] == curr_mat["category"] 
                                                            and m["id"] != curr_mat["id"]
                                                            and (m.get("yield_strength_min") or 0) >= curr_ys 
                                                            and (m.get("cost_per_kg_min") or float('inf')) < curr_cost]
                                                    
                                                    if alts:
                                                        optimization_found = True
                                                        alts.sort(key=lambda x: x.get("cost_per_kg_min", 0))
                                                        best_alt = alts[0]
                                                        savings_per_kg = curr_cost - best_alt["cost_per_kg_min"]
                                                        
                                                        with st.container(border=True):
                                                            st.markdown(f"💡 **Part:** {item['part_name']}")
                                                            st.markdown(f"**Current Material:** {curr_mat['name']} (Yield: {curr_ys} MPa, Cost: Rs. {curr_cost}/kg)")
                                                            st.success(f"**Suggested Alternative:** {best_alt['name']} (Yield: {best_alt.get('yield_strength_min')} MPa, Cost: Rs. {best_alt.get('cost_per_kg_min')}/kg)")
                                                            st.metric(f"Potential Savings per kg", f"Rs. {savings_per_kg:.2f}")
                                            if not optimization_found:
                                                st.info("Your BOM is fully optimized! No cheaper equivalents found with equal or better yield strength.")

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
        
        agree_tc = st.checkbox("I agree to the Terms & Conditions (No abuse, profanity, pornography, or hate speech).")
        
        fb_submit = st.form_submit_button("Send Feedback", use_container_width=True)

        if fb_submit:
            if not fb_message or len(fb_message.strip()) < 3:
                st.error("Please write a bit more detail before submitting.")
            elif not agree_tc:
                st.error("You must agree to the Terms & Conditions before submitting.")
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
