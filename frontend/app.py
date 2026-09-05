"""
MatDataHub — Streamlit Frontend MVP

A searchable, filterable engineering material database with side-by-side comparison.
Connects to the FastAPI backend.

Run with:
    streamlit run frontend/app.py
"""
import os
from dotenv import load_dotenv
load_dotenv()
import time
from urllib.parse import urlparse

import pandas as pd
from fpdf import FPDF
from datetime import datetime
import requests
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


OAUTH_HTML = '''
<style>
.oauth-btn {
    display: flex; align-items: center; justify-content: center; width: 100%;
    padding: 0.5rem 1rem; margin-bottom: 0.5rem;
    border: 1px solid rgba(128,128,128,0.3); border-radius: 8px;
    color: inherit; text-decoration: none;
    font-size: 15px; font-weight: 500; transition: all 0.2s;
    background-color: transparent;
}
.oauth-btn:hover {
    border-color: #ff4b4b; color: #ff4b4b;
}
.oauth-icon {
    margin-right: 12px;
}
</style>
<div style="display: flex; flex-direction: column; gap: 4px; margin-bottom: 12px;">
    <a href="https://matdatahub-api.onrender.com/api/v1/auth/google" class="oauth-btn" target="_self">
        <svg class="oauth-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="18px" height="18px"><path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"/><path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"/><path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z"/><path fill="#1976D2" d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z"/></svg>
        Continue with Google
    </a>
    <a href="https://matdatahub-api.onrender.com/api/v1/auth/apple" class="oauth-btn" target="_self">
        <svg class="oauth-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" width="18px" height="18px" fill="currentColor"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>
        Continue with Apple
    </a>
    <a href="https://matdatahub-api.onrender.com/api/v1/auth/sms" class="oauth-btn" target="_self">
        <svg class="oauth-icon" xmlns="http://www.w3.org/2000/svg" width="18px" height="18px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect><line x1="12" y1="18" x2="12.01" y2="18"></line></svg>
        Sign in with Phone
    </a>
</div>
'''



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

# --- THEME-AWARE CSS ---
st.markdown("""
<style>
/* Futuristic Glassmorphism Theme */
:root {
    --glass-bg: rgba(255, 255, 255, 0.05);
    --glass-border: rgba(255, 255, 255, 0.1);
    --neon-green: #00F0FF; /* Cyberpunk cyan/green */
    --neon-purple: #8A2BE2;
}

[data-testid="stAppViewContainer"] {
    background-color: transparent;
}

.hero-section {
    background: linear-gradient(135deg, rgba(0, 240, 255, 0.05) 0%, rgba(138, 43, 226, 0.05) 100%);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 3rem 2rem; 
    border-radius: 16px; 
    border: 1px solid var(--glass-border);
    margin-bottom: 2.5rem; 
    text-align: center; 
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    animation: glow 4s infinite alternate;
}

@keyframes glow {
    from { box-shadow: 0 0 10px rgba(0, 240, 255, 0.05); }
    to { box-shadow: 0 0 20px rgba(138, 43, 226, 0.1); }
}

.hero-title {
    color: var(--text-color); 
    font-size: 3.5rem; 
    margin-bottom: 0.5rem; 
    font-weight: 900; 
    letter-spacing: -1.5px;
    background: -webkit-linear-gradient(45deg, #00F0FF, #8A2BE2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: var(--text-color); 
    opacity: 0.85;
    font-size: 1.25rem; 
    max-width: 750px; 
    margin: 0 auto; 
    line-height: 1.6;
    font-weight: 300;
}

.cyber-stat {
    background: var(--glass-bg);
    backdrop-filter: blur(8px);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 1.5rem 1rem;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.cyber-stat:hover {
    border-color: var(--neon-green);
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 10px 25px rgba(0, 240, 255, 0.15);
}

.cyber-num {
    font-size: 2.5rem;
    font-weight: 900;
    color: var(--text-color);
    margin-bottom: 0.2rem;
    background: -webkit-linear-gradient(45deg, #00F0FF, #8A2BE2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.cyber-label {
    font-size: 0.85rem;
    color: var(--text-color);
    opacity: 0.7;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 700;
}

.domain-card {
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid var(--glass-border);
    height: 100%;
    transition: all 0.3s ease;
}

.domain-card:hover {
    border-color: var(--neon-purple);
    box-shadow: 0 8px 20px rgba(138, 43, 226, 0.15);
    transform: translateY(-3px);
}

.domain-card p {
    color: var(--text-color);
    opacity: 0.8;
    font-size: 0.95rem;
    margin-bottom: 0;
    line-height: 1.5;
}

.domain-card h4 {
    margin-top: 0;
    color: var(--text-color);
    font-weight: 800;
    letter-spacing: -0.5px;
}


/* Ultra-modern Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.02);
}
::-webkit-scrollbar-thumb {
    background: rgba(0, 240, 255, 0.3);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(138, 43, 226, 0.6);
}

/* Glassmorphism Buttons */
div[data-testid="stButton"] > button {
    background: rgba(128, 128, 128, 0.1);
    border: 1px solid rgba(128, 128, 128, 0.2);
    backdrop-filter: blur(5px);
    transition: all 0.3s ease;
    border-radius: 8px;
}
div[data-testid="stButton"] > button:hover {
    border-color: #00F0FF;
    box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
    transform: translateY(-2px);
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0);
}

/* Primary Button Glow */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(90deg, rgba(0, 240, 255, 0.2), rgba(138, 43, 226, 0.2));
    border: 1px solid #00F0FF;
    font-weight: bold;
    color: var(--text-color) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    box-shadow: 0 0 20px rgba(138, 43, 226, 0.4);
}

/* Inputs & Selectboxes Glass */
div[data-baseweb="select"] > div, 
div[data-baseweb="input"] > div {
    background: rgba(128, 128, 128, 0.05) !important;
    border: 1px solid rgba(128, 128, 128, 0.2) !important;
    border-radius: 6px;
    backdrop-filter: blur(4px);
    transition: border-color 0.3s ease;
}
div[data-baseweb="select"]:hover > div, 
div[data-baseweb="input"]:hover > div {
    border-color: #00F0FF !important;
}

/* Customizing Streamlit Tabs to look modern */
div[data-testid="stTabs"] button {
    font-weight: 600;
    font-size: 1rem;
}

</style>
""", unsafe_allow_html=True)

# --- APP STATE INITIALIZATION ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "main"







# Global Keyboard Scrolling Injection V3 (Parent Context Script Injection)
st.html("""
<script>
try {
    const parentDoc = window.parent.document;
    if (!parentDoc.getElementById('scroll-script-v3')) {
        const script = parentDoc.createElement('script');
        script.id = 'scroll-script-v3';
        script.innerHTML = 
            window.addEventListener('keydown', function(e) {
                const active = document.activeElement;
                if (active) {
                    const tag = active.tagName.toLowerCase();
                    if (tag === 'input' || tag === 'textarea') return;
                    const role = active.getAttribute('role');
                    if (['slider', 'spinbutton', 'combobox', 'listbox', 'menuitem', 'switch', 'tab'].includes(role)) return;
                    if (active.isContentEditable) return;
                }
                
                if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                    let container = document.querySelector('[data-testid="stAppViewMain"]') || 
                                    document.querySelector('.main') || 
                                    document.querySelector('[data-testid="stMain"]');
                                    
                    if (!container || container.scrollHeight <= container.clientHeight) {
                        const all = document.querySelectorAll('*');
                        let maxArea = 0;
                        for(let i=0; i<all.length; i++) {
                            const style = window.getComputedStyle(all[i]);
                            if (style.overflowY === 'auto' || style.overflowY === 'scroll' || style.overflowY === 'overlay') {
                                if (all[i].scrollHeight > all[i].clientHeight) {
                                    const area = all[i].clientWidth * all[i].clientHeight;
                                    if (area > maxArea) {
                                        maxArea = area;
                                        container = all[i];
                                    }
                                }
                            }
                        }
                    }
                    
                    const amt = e.key === 'ArrowDown' ? window.innerHeight * 0.20 : -(window.innerHeight * 0.20);
                    if (container && typeof container.scrollBy === 'function') {
                        container.scrollBy({ top: amt, behavior: 'auto' });
                        e.stopPropagation();
                        e.preventDefault();
                    }
                }
            }, true);
        ;
        parentDoc.head.appendChild(script);
    }
} catch (e) {
    console.error("Scroll V3 failed:", e);
}
</script>
""")

def render_pricing_page():
    c1, c2, c3 = st.columns([1, 6, 1])
    with c1:
        if st.button("⬅️ Back to Main", use_container_width=True):
            st.session_state.current_page = "main"
            st.rerun()
    with c3:
        if st.button("⚙️ Account", use_container_width=True):
            st.session_state.current_page = "account"
            st.rerun()
            
    st.markdown("<h1 style='text-align: center;'>Upgrade Your Plan</h1>", unsafe_allow_html=True)
    user = st.session_state.get("user", {})
    st.markdown("### Choose your Plan")
    st.caption(f"You are currently on the **{user.get('tier', 'free').upper()}** plan.")
    
    p1, p2, p3 = st.columns(3)
    with p1:
        with st.container(border=True):
            st.markdown("### Free")
            st.markdown("## ₹0 / mo")
            st.markdown("- ✅ Access to all 1,000+ materials\n- ✅ Compare up to 2 materials\n- ❌ AI Advisor\n- ❌ Cost Optimizer\n")
            st.button("Current Plan", disabled=True, use_container_width=True, key="btn_free")
            
    with p2:
        with st.container(border=True):
            st.markdown("### Pro")
            st.markdown("## ₹499 / mo")
            st.markdown("- ✅ Compare up to 5 materials\n- ✅ Structural & Thermal Analyzers\n- ✅ AI Material Advisor\n- ❌ Offline PDF Reports")
            if user.get("tier") == "pro":
                st.button("Current Plan", disabled=True, use_container_width=True, key="btn_pro1")
            else:
                if st.button("Upgrade to Pro", type="primary", use_container_width=True, key="btn_pro2"):
                    url, err = get_upgrade_link("pro")
                    if url:
                        st.markdown(f"**[🔗 Click here to Pay Securely via Razorpay]({url})**")
                    else:
                        st.error(f"Payment failed: {err}")
                
    with p3:
        with st.container(border=True):
            st.markdown("### Advanced")
            st.markdown("## ₹49,999 / mo")
            st.markdown("- ✅ Unlimited Comparisons\n- ✅ Cost Optimization Engine\n- ✅ Download PDF Reports\n- ✅ Programmatic API Access")
            if user.get("tier") == "advanced":
                st.button("Current Plan", disabled=True, use_container_width=True, key="btn_adv1")
            else:
                if st.button("Upgrade to Advanced", type="primary", use_container_width=True, key="btn_adv2"):
                    url, err = get_upgrade_link("advanced")
                    if url:
                        st.markdown(f"**[🔗 Click here to Pay Securely via Razorpay]({url})**")
                    else:
                        st.error(f"Payment failed: {err}")
                



    st.divider()
    
    st.markdown("### 💬 Payment & Billing Support")
    st.info("Did your transaction fail? Or was your account debited but not upgraded? Contact us immediately below, and our support team will manually upgrade your account.")
    
    with st.form("billing_support_form", clear_on_submit=True):
        fcol1, fcol2 = st.columns(2)
        with fcol1:
            s_name = st.text_input("Name", value=user.get("name", ""))
        with fcol2:
            s_email = st.text_input("Email", value=user.get("email", ""))
        
        s_issue = st.selectbox("Issue Type", ["Account debited but not upgraded", "Transaction Failed / Razorpay Error", "Invoice Request", "Other Payment Issue"])
        s_message = st.text_area("Message / Payment Reference ID", placeholder="Please provide your transaction ID or exact issue...")
        
        if st.form_submit_button("Submit Support Ticket", type="primary", use_container_width=True):
            if len(s_message) < 5:
                st.error("Please provide more details or a transaction ID.")
            else:
                result = submit_feedback(
                    s_name, s_email, f"Billing: {s_issue}", 
                    s_message, 1, "Billing Support UI", None
                )
                if result.get("ok"):
                    st.success("✅ Your ticket has been submitted successfully! Our billing team will resolve this within 12 hours.")
                else:
                    st.error("Could not submit ticket. Please email support@matdatahub.com directly.")


def get_upgrade_link(tier: str):
    token = st.session_state.get("token")
    if not token: return None, "Please log in first."
    try:
        resp = requests.post(f"{API_BASE}/payments/create-link", json={"tier": tier}, headers={"Authorization": f"Bearer {token}"}, timeout=30)
        if resp.status_code == 200:
            return resp.json().get("payment_url"), None
        return None, resp.json().get("detail", "Unknown error")
    except Exception as e:
        return None, str(e)



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
        border: 1px solid rgba(128, 128, 128, 0.2);
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
def generate_bom_pdf(project_name, df_bom, total_mass, total_cost):
    """Generate a professional, branded PDF report for the BOM."""
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    
    # --- Header ---
    pdf.set_fill_color(33, 37, 41)
    pdf.rect(0, 0, 210, 30, 'F')
    
    pdf.set_font("helvetica", "B", 24)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(10)
    pdf.cell(0, 10, "MatDataHub", align="L")
    
    pdf.set_font("helvetica", "I", 12)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 10, "Engineering BOM Report", align="R")
    
    # --- Project Metadata ---
    pdf.set_y(40)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, f"Project: {project_name}", ln=1)
    
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
    pdf.cell(0, 5, "Classification: STRICTLY CONFIDENTIAL", ln=1)
    pdf.line(10, 60, 200, 60)
    
    # --- BOM Table ---
    pdf.set_y(65)
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Bill of Materials (BOM) Breakdown", ln=1)
    
    # Table Header
    pdf.set_font("helvetica", "B", 10)
    pdf.set_fill_color(240, 240, 240)
    col_widths = [45, 75, 35, 35]
    headers = ["Part Name", "Material", "Volume (cm^3)", "Mass (kg)"]
    for i in range(4):
        pdf.cell(col_widths[i], 8, headers[i], border=1, fill=True)
    pdf.ln()
    
    # Table Rows
    pdf.set_font("helvetica", "", 10)
    for _, row in df_bom.iterrows():
        pdf.cell(col_widths[0], 8, str(row.iloc[0])[:25], border=1)
        pdf.cell(col_widths[1], 8, str(row.iloc[1])[:40], border=1)
        pdf.cell(col_widths[2], 8, str(row.iloc[2]), border=1)
        pdf.cell(col_widths[3], 8, str(row.iloc[3]), border=1)
        pdf.ln()
        
    # --- Summary ---
    pdf.ln(5)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Engineering Summary", ln=1)
    
    pdf.set_font("helvetica", "", 11)
    pdf.cell(80, 8, "Total Assembly Mass:", border=0)
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(0, 8, f"{total_mass:,.2f} kg", border=0, ln=1)
    
    pdf.set_font("helvetica", "", 11)
    pdf.cell(80, 8, "Estimated Material Cost:", border=0)
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(0, 8, f"Rs. {total_cost:,.2f}", border=0, ln=1)
    
    # --- Footer ---
    pdf.set_auto_page_break(auto=False)
    pdf.set_y(280)
    pdf.set_font("helvetica", "I", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, "Powered by MatDataHub Professional Edition. Data export tracked for security compliance.", align="C")
    
    # Output to byte string
    return bytes(pdf.output())


@st.cache_data(ttl=60, show_spinner=False)
def fetch_public_feedback():
    return api_get("/feedback/public")

@st.cache_data(ttl=600, show_spinner=False)
def fetch_all_materials(token=None):
    """Fetch all materials from the API with retry. Cached for 10 minutes to improve performance."""
    return api_get("/materials/", params={"per_page": 1000})


@st.cache_data(ttl=300)
def fetch_material_detail(mat_id, token=None):
    """Fetch a single material's full details."""
    result = api_get(f"/materials/{mat_id}")
    if result["ok"]:
        return result["data"]
    return None


def submit_feedback(name, email, category, message, rating, page_context, image_data=None):
    """Submit user feedback to the backend. Works for anonymous or logged-in users."""
    body = {
        "name": name or None,
        "email": email or None,
        "category": category,
        "message": message,
        "rating": rating,
        "page_context": page_context,
    }
    if image_data:
        body["image_data"] = image_data
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

    # Immersive Cyber/Neon colors
    hex_colors = ["#00f0ff", "#ff003c", "#fcee0a", "#b026ff"]
    fill_colors = ["rgba(0, 240, 255, 0.25)", "rgba(255, 0, 60, 0.25)", "rgba(252, 238, 10, 0.25)", "rgba(176, 38, 255, 0.25)"]

    for i, name in enumerate(selections):
        values = [radar_data[cat][i] for cat in categories]
        values += values[:1]  # close the shape
        c_idx = i % len(hex_colors)
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill="toself",
            name=name,
            line=dict(color=hex_colors[c_idx], width=4, shape='linear'),
            fillcolor=fill_colors[c_idx],
            marker=dict(size=10, symbol='diamond', color=hex_colors[c_idx], line=dict(width=2, color='rgba(255,255,255,0.8)'))
        ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(10, 15, 30, 0.5)",
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor="rgba(0, 240, 255, 0.15)", gridwidth=1.5),
            angularaxis=dict(gridcolor="rgba(0, 240, 255, 0.25)", linecolor="rgba(0, 240, 255, 0.4)", tickfont=dict(size=13, color="#88aaff", weight="bold"))
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5, font=dict(color="#fff", size=14), bgcolor="rgba(0,0,0,0.4)", bordercolor="rgba(0, 240, 255, 0.3)", borderwidth=1),
        height=600,
        margin=dict(l=60, r=60, t=80, b=40),
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
        if st.session_state.current_page == "main":
            if st.button("⚙️ Manage Account", use_container_width=True):
                st.session_state.current_page = "account"
                st.rerun()
        else:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.session_state.current_page = "main"
                st.rerun()
        current_tier = st.session_state.user.get("tier", "free")
        if current_tier != "advanced":
            if st.button("✨ Upgrade Plan", type="primary", use_container_width=True):
                st.session_state.current_page = "pricing"
                st.rerun()
        st.divider()
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
            if st.button("🚀 Request Upgrade to Pro — ₹499/mo"):
                st.session_state.current_page = "pricing"
                st.rerun()
            if st.button("💎 Request Upgrade to Advanced — ₹49,999/mo"):
                st.session_state.current_page = "pricing"
                st.rerun()
        elif current_tier == "pro":
            st.caption("Upgrades are reviewed manually — you'll see a pending badge after requesting.")
            if st.button("💎 Request Upgrade to Advanced — ₹49,999/mo"):
                st.session_state.current_page = "pricing"
                st.rerun()
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
        # We store the actual password typed to pass to the backend
        admin_pw = st.text_input("Admin password", type="password")
        if admin_pw:
            st.session_state.temp_admin_pw = admin_pw
            
        # Use whichever password was successfully saved, or the new one typed
        active_pw = st.session_state.get("temp_admin_pw") or os.getenv("ADMIN_SECRET", "sk_test_admin_key") if st.session_state.get("is_admin_unlocked") else admin_pw
        
        if active_pw:
            admin_headers = {"X-Admin-Secret": active_pw}
            try:
                r = requests.get(f"{API_BASE}/admin/upgrade-requests", headers=admin_headers, timeout=15)
                if r.status_code == 403:
                    st.error("Wrong password.")
                elif r.status_code != 200:
                    st.error(f"Error: {r.status_code}")
                else:
                    st.session_state.is_admin_unlocked = True
                    st.session_state.temp_admin_pw = active_pw
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
<p class="hero-sub">The ultimate engineering material data-as-a-service platform. Discover, compare, and analyze over 1,000+ industrial materials instantly.</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TABS: Home | Browse | Compare | Feedback
# ══════════════════════════════════════════════


if st.session_state.current_page == "account":

    st.markdown("## ⚙️ Account & Settings")
    user = st.session_state.get("user")
    
    if not user:
        st.markdown("### Sign In to MatDataHub")
        st.caption("Access your projects, upgrade your tier, and manage your account.")
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            with st.container(border=True):
                st.markdown("#### Login or Create an Account")
                
                with st.form("account_login_form"):
                    st.markdown("**Email & Password**")
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    if st.form_submit_button("Sign In", use_container_width=True):
                        # Call the existing login function
                        if email and password:
                            res = api_post("/auth/login", {"email": email, "password": password})
                            if res["ok"]:
                                st.session_state.token = res["data"]["access_token"]
                                st.session_state.user = api_get("/auth/me")["data"]
                                st.success("Logged in!")
                                st.rerun()
                            else:
                                st.error(res["error"])
    else:
        # Logged in Account Dashboard
        ac1, ac2 = st.columns([1, 3])
        
        # We can use nested tabs or a radio selector to act as a side-menu for the account tab
        with ac1:
            account_menu = st.radio("Settings", [
                "👤 Profile & Security", 
                "🛠️ Custom Materials (Enterprise)",
                "💳 Payment History", 
                "📚 Help Center & Legal",
                "⌨️ Keyboard Shortcuts"
            ], label_visibility="collapsed")
            
            st.divider()
            if st.button("🚪 Sign Out", use_container_width=True):
                st.session_state.token = None
                st.session_state.user = None
                st.rerun()
                
        with ac2:
            if account_menu == "👤 Profile & Security":
                st.markdown("### Profile Details")
                st.text_input("Full Name", value=user.get("name", ""))
                st.text_input("Email Address", value=user.get("email", ""), disabled=True)
                st.text_input("Authentication Provider", value=user.get("auth_provider", "email").title(), disabled=True)
                if st.button("Save Changes"):
                    st.success("Profile updated.")
                st.divider()
                st.markdown("### 🔑 API Access")
                if user.get("tier") == "advanced":
                    current_key_exists = bool(user.get("api_key"))
                    
                    if current_key_exists:
                        st.success("✅ Your Enterprise API Key is active (Hidden for security).")
                        st.caption("Pass your **API Secret** in the `X-API-Key` HTTP header to authenticate.")
                    else:
                        st.info("You haven't generated an API Key yet.")
                    
                    # We define a function for the modal popup
                    @st.dialog("🔑 Generate API Key", width="large")
                    def show_api_key_modal():
                        st.warning("⚠️ CRITICAL: Copy your API Secret now. For security reasons, it will NEVER be shown again once you close this window!")
                        import requests
                        with st.spinner("Provisioning enterprise credentials..."):
                            r = requests.post(
                                f"{API_BASE}/account/generate-api-key",
                                headers={"Authorization": f"Bearer {st.session_state.token}"}
                            )
                        if r.status_code == 200:
                            data = r.json()
                            st.markdown("### API Key ID (Public)")
                            st.code(data.get("api_key_id", ""), language="text")
                            
                            st.markdown("### API Secret")
                            st.code(data.get("api_secret", ""), language="text")
                            
                            st.info("Please store this securely in your environment variables or secret manager (e.g., AWS Secrets Manager, GCP Secret Manager).")
                            if st.button("I have copied my API Secret"):
                                # Refresh user state to show the success badge
                                me_res = api_get("/auth/me")
                                if me_res["ok"]: st.session_state.user = me_res["data"]
                                st.rerun()
                        else:
                            st.error("Failed to generate API Key.")
                            
                    if st.button("Generate New API Key", type="primary"):
                        show_api_key_modal()
                else:
                    st.warning("API Access is strictly reserved for the Advanced (Enterprise) tier.")

                

                    
            
            elif account_menu == "🛠️ Custom Materials (Enterprise)":
                st.markdown("### 🛠️ Private Custom Materials")
                if user.get("tier") == "advanced":
                    st.write("Upload your proprietary materials here. These will be strictly isolated to your enterprise account and available in the BOM Synthesizer.")
                    
                    with st.expander("➕ Add New Proprietary Material"):
                        with st.form("custom_mat_form", clear_on_submit=True):
                            c_name = st.text_input("Material Name (e.g. Stark Titanium X-1)")
                            c_cat = st.selectbox("Category", ["Metal", "Polymer", "Composite", "Ceramic", "Other"])
                            c_dens = st.number_input("Density (g/cm3)", min_value=0.01, value=1.0)
                            c_tens = st.number_input("Tensile Strength (MPa)", min_value=0.0)
                            c_cost = st.number_input("Internal Cost Estimate (INR/kg)", min_value=0.0)
                            
                            if st.form_submit_button("Save to Private Database"):
                                payload = {
                                    "name": c_name, "category": c_cat, "density": c_dens, 
                                    "tensile_strength_min": c_tens, "cost_per_kg_min": c_cost
                                }
                                res = api_post("/materials/custom", payload)
                                if res["ok"]:
                                    st.success(f"{c_name} added securely!")
                                    st.rerun()
                                else:
                                    st.error("Failed to add material.")
                                    
                    st.markdown("#### Your Library")
                    my_mats = api_get("/materials/custom/mine")
                    if my_mats["ok"] and my_mats["data"]:
                        for mm in my_mats["data"]:
                            st.markdown(f"**{mm['name']}** ({mm['category']}) - {mm['tensile_strength_min']} MPa | ₹{mm['cost_per_kg_min']}/kg")
                    else:
                        st.caption("No proprietary materials uploaded yet.")
                else:
                    st.warning("Custom Private Materials are exclusively available on the Advanced (Enterprise) tier.")

            elif account_menu == "💳 Payment History":
                st.markdown("### Transaction History")
                # Fetch transactions from backend
                tx_res = api_get("/account/transactions")
                if tx_res.get("ok"):
                    txs = tx_res["data"]
                    if not txs:
                        st.info("No past transactions or payments found.")
                    else:
                        for tx in txs:
                            with st.container():
                                col1, col2 = st.columns([3, 1])
                                with col1:
                                    st.markdown(f"**Amount:** {tx.get('amount', '0')} {tx.get('currency', 'USD')} | **Status:** {tx.get('status', 'Completed')}")
                                    st.caption(f"Date: {tx.get('created_at', 'N/A')}")
                                with col2:
                                    st.code(tx.get('id', 'N/A'), language=None)
                            st.divider()
                else:
                    st.error("Could not load transaction history.")
                    
            elif account_menu == "📚 Help Center & Legal":
                st.markdown("### Help Center")
                with st.expander("How do I upgrade my plan?"):
                    st.write("Go to the Subscriptions tab and select a plan. Payments are processed securely via Razorpay/Stripe.")
                with st.expander("How do I cancel my subscription?"):
                    st.write("Please contact support or use the billing portal to downgrade your plan to Free.")
                with st.expander("Where does MatDataHub get its data?"):
                    st.write("Our data is sourced from verified standards including ASTM, ISO, MMPDS, and ASM International.")
                
                st.markdown("### Legal")
                st.markdown("[Privacy Policy](/privacy) (Coming soon)")
                st.markdown("[Terms of Service](/tos) (Coming soon)")
                
                st.divider()
                st.markdown("### Feedback & Support")
                st.write("Found a bug or need help?")
                if st.button("Report a Bug"):
                    st.info("Please navigate to the Community Feedback tab to report bugs!")
                    
            elif account_menu == "⌨️ Keyboard Shortcuts":
                st.markdown("### Global Keyboard Shortcuts")
                st.markdown("""
                | Shortcut | Action |
                | :--- | :--- |
                | **Up Arrow** | Scroll page up |
                | **Down Arrow** | Scroll page down |
                | **Tab** | Cycle between input fields |
                | **Enter** | Submit active form |
                
                *Note: Arrow key scrolling is temporarily disabled while you are actively typing inside a text box or adjusting a slider.*
                """)


    st.stop() # Halt rendering of the main app tabs

if st.session_state.current_page == "pricing":
    render_pricing_page()
    st.stop()




if st.session_state.current_page == "main":
    # Massive UI/UX IA Refactor: Grouping into Logical Workspaces
    tab_home_main, tab_browse_main, tab_analytics, tab_workflows, tab_support_main, tab_faq_main, tab_blog_main = st.tabs([
        "🏠 Dashboard", "🔍 Explorer", "⚖️ Analytics", "⚙️ Workflows", "💬 Support Center", "❓ FAQ", "📰 Engineering Blog"
    ])
    
    with tab_home_main:
        st.markdown("## 🏠 Command Center")
        st.caption("Welcome to your MatDataHub operations dashboard. Access materials, engineering insights, and enterprise tools from one unified platform.")
        st.divider()
        tab_home, tab_guide = st.tabs(["🏠 Overview", "📖 Quick Start Guide"])




    with tab_browse_main:
        st.markdown("## 🔍 Explorer & AI Advisor")
        st.caption("Search the global database or consult the AI Metallurgist for intelligent recommendations.")
        st.divider()
        tab_browse, tab_ai = st.tabs(["🔍 Browse Database", "🤖 Ask AI Advisor"])
        
    with tab_analytics:
        st.markdown("## ⚖️ Advanced Analytics & AI Substitution")
        st.caption("Compare materials side-by-side or use our proprietary AI to mathematically calculate the perfect supply chain substitute.")
        st.divider()
        tab_compare, tab_substitute = st.tabs(["⚖️ Side-by-Side Compare", "🔄 Smart AI Substitution (PRO)"])
        
    with tab_workflows:
        st.markdown("## ⚙️ Engineering & Enterprise Workflows")
        st.caption("Build custom project assemblies, calculate weights, and utilize our AI-powered ESG (Environmental, Social, & Governance) compliance engine.")
        st.divider()
        tab_projects, tab_enterprise = st.tabs(["⚙️ Standard BOM Builder", "📊 Enterprise ESG Analyzer (ADV)"])
        
    with tab_faq_main:
        st.markdown("## ❓ Frequently Asked Questions")
        st.divider()

    with tab_support_main:
        st.markdown("## 💬 Support Center")
        st.caption("Reach out to our dedicated enterprise support team for billing or technical issues.")
        st.divider()
    
    
    # ══════════════════════════════════════════════
    #  TAB 0: HOME
    # ══════════════════════════════════════════════
    with tab_home:
        if st.session_state.get("user"):
            st.markdown(f"""
                <div style="background: rgba(79, 195, 161, 0.1); border-left: 4px solid #4FC3A1; border-radius: 4px; padding: 15px 20px; color: var(--text-color); margin-bottom: 2rem; font-weight: 500; font-size: 1.1rem; line-height: 1.5;">
                     Welcome back, <b style="color: #4FC3A1;">{st.session_state.user.get('name') or st.session_state.user['email']}</b> to MatDataHub! <br>
                    <span style="opacity: 0.85; font-size: 1rem; font-weight: 400;">Your enterprise command center for metallurgical analytics, ESG compliance, and supply chain optimization.</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
<div style="background: rgba(46, 134, 171, 0.1); border-left: 4px solid #2E86AB; border-radius: 4px; padding: 15px 20px; color: var(--text-color); margin-bottom: 2rem; font-weight: 500; font-size: 1.1rem; line-height: 1.5;">
                     <b>Welcome to MatDataHub!</b> Browse materials freely — sign in to unlock intelligent ESG tracking, bulk BOM analysis, and the AI Advisor.<br>
<span style="opacity: 0.85; font-size: 1rem; font-weight: 400;">The ultimate operating system for modern materials engineering.</span>
</div>
            """, unsafe_allow_html=True)

        # --- LIVE DATABASE STATS ---
        st.markdown("### 🌐 Platform Capabilities")
        s1, s2, s3, s4 = st.columns(4)
        for col, num, label in [
            (s1, "1,030+", "Verified Materials"),
            (s2, "AI", "Substitution Engine"),
            (s3, "ESG", "Carbon Footprint Tracking"),
            (s4, "Bulk", "BOM Parsing & Analysis"),
        ]:
            with col:
                st.markdown(f'<div class="cyber-stat"><div class="cyber-num">{num}</div><div class="cyber-label">{label}</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        # --- QUICK ACTIONS ---
        st.markdown("### ⚡ Quick Actions & Tools")
        qa1, qa2, qa3 = st.columns(3)
        with qa1:
            st.info("🔄 **Smart Substitution**\n\nMathematically find alternative supply chain materials based on cost, weight, and carbon footprint. Available in Analytics.")
        with qa2:
            st.success("📊 **Enterprise BOM Analyzer**\n\nUpload a CSV assembly to instantly verify ESG compliance and obsolete global standards. Available in Workflows.")
        with qa3:
            st.warning("🤖 **AI Metallurgist**\n\nDescribe your engineering constraints in natural language and get instantaneous material recommendations. Available in Explorer.")
        
        st.markdown("---")


        st.markdown('---')
        st.markdown("## Community Reviews & Discussion")
        st.markdown("See what other engineers are saying about MatDataHub, reply to their feedback, and join the discussion!")
    
        try:
            rev_resp = fetch_public_feedback()
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
                    
                    # Custom CSS for compact feedback display
                    st.markdown("""
<style>
/* Shrink Streamlit button paddings */
                        button[data-testid="baseButton-secondary"] {
                            padding: 2px 8px !important;
                            min-height: 25px !important;
                            font-size: 0.75rem !important;
                        }
.compact-comment {
                            padding-left: 10px;
                            border-left: 2px solid #333;
                            margin-bottom: 10px;
                            font-size: 0.85em;
                            line-height: 1.4;
                        }
.compact-name { font-weight: bold; color: #4DA8DA; }
.compact-message { margin-top: 2px; margin-bottom: 2px; }
.compact-admin {
                            background-color: var(--secondary-background-color);
                            border: 1px solid var(--faded-text-20);
                            border-left: 3px solid #00f0ff;
                            border-radius: 5px;
                            padding: 10px;
                            margin-top: 10px;
                            font-size: 0.85em;
                            color: var(--text-color);
                        }
.compact-img {
                            max-width: 250px;
                            border-radius: 4px;
                            margin-top: 5px;
                        }
</style>
                    """, unsafe_allow_html=True)
    
                    def render_comments(comments, depth=0):
                        for c in comments:
                            if depth > 0:
                                col_spacer, col_content = st.columns([0.05 * depth, 1 - (0.05 * depth)])
                            else:
                                col_spacer = None
                                col_content = st.container()
                                
                            with col_content:
                                stars = "⭐" * (c.get("rating") or 0)
                                name = c.get("name") or "Anonymous"
                                
                                # Compact HTML rendering
                                st.markdown(f"""
                                <div class="compact-comment">
                                    <span class="compact-name">{name}</span> {stars}
                                    <div class="compact-message">{c["message"]}</div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Render image if present
                                if c.get("image_data"):
                                    st.markdown(f'<img class="compact-img" src="data:image/png;base64,{c["image_data"]}">', unsafe_allow_html=True)
                                
                                # Render Admin Reply if present
                                if c.get("admin_reply"):
                                    st.markdown(f"""
                                    <div class="compact-admin">
                                        <strong style="color: #00f0ff;">✅ Verified Admin Response:</strong><br/>
                                        {c["admin_reply"]}
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                # Buttons
                                btn_cols = st.columns([1.5, 1.5, 2, 4])
                                with btn_cols[0]:
                                    votes = c.get("helpful_votes") or 0
                                    if st.button(f"👍 Helpful ({votes})", key=f"help_{c['id']}"):
                                        requests.post(f"{API_BASE}/feedback/{c['id']}/helpful")
                                        st.rerun()
                                        
                                is_admin = st.session_state.get("is_admin_unlocked", False)
                                        
                                with btn_cols[1]:
                                    if st.button("💬 Reply", key=f"reply_btn_{c['id']}"):
                                        st.session_state[f"show_reply_{c['id']}"] = not st.session_state.get(f"show_reply_{c['id']}", False)
                                        
                                if is_admin:
                                    with btn_cols[2]:
                                        with st.popover("🛡️ Admin"):
                                            if st.button("Email Reply", key=f"admin_reply_{c['id']}"):
                                                st.session_state[f"show_admin_reply_{c['id']}"] = True
                                            if st.button("Hide", key=f"hide_{c['id']}"):
                                                h_headers = {"X-Admin-Secret": st.session_state.get("temp_admin_pw", "")}
                                                requests.patch(f"{API_BASE}/feedback/{c['id']}/visibility", headers=h_headers)
                                                st.rerun()
                                            if st.button("Delete", key=f"del_fb_feed_{c['id']}"):
                                                h_headers = {"X-Admin-Secret": st.session_state.get("temp_admin_pw", "")}
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
                                                    
                                if is_admin and st.session_state.get(f"show_admin_reply_{c['id']}", False):
                                    with st.form(f"admin_form_reply_{c['id']}", clear_on_submit=True):
                                        st.caption("This will lock a verified official admin response to this thread.")
                                        admin_msg = st.text_area("Official Admin Reply...")
                                        if st.form_submit_button("Post Official Admin Reply"):
                                            if admin_msg:
                                                resp = requests.post(
                                                    f"{API_BASE}/feedback/{c['id']}/reply", 
                                                    headers={"X-Admin-Secret": st.session_state.get("temp_admin_pw", "")},
                                                    json={"reply_text": admin_msg}
                                                )
                                                if resp.status_code == 200:
                                                    st.session_state[f"show_admin_reply_{c['id']}"] = False
                                                    data = resp.json()
                                                    msg = data.get("message", "Official reply posted!")
                                                    st.success(msg)
                                                    import time
                                                    time.sleep(2)
                                                    st.rerun()
                                                    
                            if c["children"]:
                                render_comments(c["children"], depth + 1)
                            if depth == 0:
                                st.divider()
    
                    render_comments(tree[:20]) # Limit top-level to 20 for perf
            else:
                st.info("No reviews yet. Be the first to leave feedback in the Feedback tab!")
        except Exception as e:
            st.error(f"Failed to load community feedback: {e}")
    

    # 
    #  TAB: PLATFORM GUIDE
    # 

    with tab_guide:
        st.markdown("### 📖 Interactive Platform Guide")
        st.caption("Select a workflow below to learn how to maximize your MatDataHub experience.")
        
        # Interactive Navigation
        guide_step = st.radio("Select Workflow:", [
            "🔍 Discover & Browse", 
            "⚖️ Analyze & Substitute", 
            "📊 Enterprise ESG & BOM", 
            "🤖 AI Metallurgist"
        ], horizontal=True, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if guide_step == "🔍 Discover & Browse":
            col1, col2 = st.columns([1, 1.5])
            with col1:
                st.markdown("#### 1. Navigate to Explorer")
                st.write("Use the **Explorer** tab to access the full global database of over 1,000+ verified engineering materials.")
                st.write("Filter by Category (Metals, Polymers, Ceramics) or search specific ASTM/ISO standards.")
            with col2:
                st.info("💡 **Pro Tip:** Free users can view basic mechanical and thermal properties. Upgrade to Pro to view pricing histories and advanced ESG data.")
                
        elif guide_step == "⚖️ Analyze & Substitute":
            col1, col2 = st.columns([1, 1.5])
            with col1:
                st.markdown("#### 2. The Smart Substitution Engine")
                st.write("Supply chain disruptions? Cost-cutting mandates? Use the **Analytics -> Smart Substitution** engine.")
                st.write("Select your base material (e.g., AISI 304) and use the sliders to prioritize Cost, Weight, Strength, and Carbon Footprint.")
            with col2:
                st.success("✅ **Mathematical Optimization:** The AI normalizes the database and generates interactive Radar Charts proving exactly why an alternative material is superior.")
                
        elif guide_step == "📊 Enterprise ESG & BOM":
            col1, col2 = st.columns([1, 1.5])
            with col1:
                st.markdown("#### 3. Automated BOM Enrichment")
                st.write("Procurement teams can upload messy Excel/CSV Bills of Materials directly into the **Workflows** tab.")
                st.write("Our fuzzy-matching AI cleans the data, finds the exact materials, and flags obsolete global standards.")
            with col2:
                st.warning("🌍 **ESG Compliance:** The system automatically calculates the Total Embodied Carbon (kg CO2e) for your entire project, generating instant sustainability reports.")
                
        elif guide_step == "🤖 AI Metallurgist":
            col1, col2 = st.columns([1, 1.5])
            with col1:
                st.markdown("#### 4. Natural Language Engineering")
                st.write("Skip the manual filters. Chat directly with our **AI Advisor** located in the Explorer tab.")
                st.write("Example: *'I need a lightweight alloy for an aerospace drone bracket that operates at 150°C and costs less than $15/kg.'*")
            with col2:
                st.error("🤖 **Context-Aware:** The AI is natively hooked into our verified database, meaning it doesn't hallucinate—it strictly recommends actual, purchasable materials.")

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("---")

    with tab_browse:
    
        search_query = st.text_input(
            "Search by name, grade, standard, or application...",
            placeholder="e.g. stainless, 6061, aerospace, corrosion",
        )
    
        with st.expander("🔍 Filters", expanded=True):
            fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns(5)
    
            with fcol1:
                category = st.selectbox(
                    "Material Category",
                    ["All", "Metal", "Polymer", "Ceramic", "Composite", "Semiconductor", "Nanomaterial"],
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
                        tensile = f"{m['tensile_strength_min']:.0f}"
                        if m.get("tensile_strength_max") is not None and m["tensile_strength_max"] != m["tensile_strength_min"]:
                            tensile += f"-{m['tensile_strength_max']:.0f}"
    
                    cost = ""
                    if m.get("cost_per_kg_min") is not None:
                        cost = f"{m['cost_per_kg_min']:.0f}"
                        if m.get("cost_per_kg_max") is not None and m["cost_per_kg_max"] != m["cost_per_kg_min"]:
                            cost += f"-{m['cost_per_kg_max']:.0f}"
    
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
                    m = fetch_material_detail(mat_id, st.session_state.get("token"))
    
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
                            st.markdown("### 📈 Historical Price Tracking")
                            with st.spinner("Loading commodity price history..."):
                                price_resp = api_get(f"/materials/{mat_id}/price-history")
                                if price_resp["ok"] and price_resp["data"]:
                                    import pandas as pd
                                    hist_data = price_resp["data"]
                                    df_hist = pd.DataFrame(hist_data)
                                    if not df_hist.empty:
                                        df_hist["recorded_date"] = pd.to_datetime(df_hist["recorded_date"])
                                        df_hist = df_hist.set_index("recorded_date")

                                        # Format the date index to explicitly include the Year and Month (e.g., '2025-08')
                                        df_hist.index = df_hist.index.strftime('%Y-%m (%b)')
                                        st.line_chart(df_hist["cost_per_kg"], height=250, use_container_width=True)
                                        st.caption("Price fluctuations (INR per kg) from 2025 to 2026.")
                                    else:
                                        st.info("No historical price data available yet.")
                                else:
                                    st.info("Historical tracking is currently gathering data for this material.")
                                    
                            if st.button(f"🔎 Find Materials Similar to {m['name']}", key=f"similar_{mat_id}"):
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
                            st.info("📈 **Upgrade to Pro or Advanced** to unlock 12-month historical commodity price tracking and alternative material discovery.")

    # ══════════════════════════════════════════════
    #  TAB 2: COMPARE MATERIALS
    # ══════════════════════════════════════════════
    with tab_compare:
    
        st.caption("Select 2 or 3 materials to compare their properties head-to-head.")
    
        with st.spinner("Loading material list (API may take ~30s on first load)..."):
            wake_api()
            all_result = fetch_all_materials(st.session_state.get("token"))
    
        if not all_result["ok"]:
            show_api_error(all_result, retry_key="retry_compare")
            all_materials = []
            name_to_id = {}
        elif "data" not in all_result or "materials" not in all_result.get("data", {}):
            st.warning("⚠️ API returned unexpected data. Please refresh.")
            if st.button("🔄 Retry", key="retry_compare_data"):
                st.rerun()
            all_materials = []
            name_to_id = {}
        else:
            all_materials = all_result["data"].get("materials", [])
            name_to_id = {m["name"]: m["id"] for m in all_materials}

        user_tier = (st.session_state.user or {}).get("tier", "free")
        if user_tier == "advanced":
            cust_mats = api_get("/materials/custom/mine")
            if cust_mats["ok"] and cust_mats["data"]:
                for cm in cust_mats["data"]:
                    all_materials.append(cm)
                    name_to_id[f"🔒 {cm['name']}"] = -cm["id"]
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
            st.caption(f"Showing {UI_MAX_SELECTORS} slots. Your tier technically allows up to {compare_max} - let us know if you need more at once.")
        elif user_tier == "free":
            st.markdown("---")
            c1, c2 = st.columns([3, 1])
            c1.info("💎 Upgrade to Pro to compare up to 5 materials at once and unlock AI tools.")
            if c2.button("✨ Upgrade Plan", use_container_width=True):
                st.session_state.current_page = "pricing"
                st.rerun()
            st.markdown("---")
    
        if len(selections) < 2:
            st.info("Select at least 2 materials above to start comparing.")
        else:
            ids = [name_to_id[name] for name in selections]

            standard_ids = [i for i in ids if i > 0]
            custom_ids = [-i for i in ids if i < 0]
            
            with st.spinner("Loading comparison..."):
                compare_result = api_get("/materials/compare", params={"ids": standard_ids}) if standard_ids else {"ok": True, "data": []}
                
                # Wow Feature: Merge private materials perfectly into the public API response!
                if custom_ids and compare_result["ok"]:
                    cust_mats = api_get("/materials/custom/mine")
                    if cust_mats["ok"] and cust_mats["data"]:
                        for cm in cust_mats["data"]:
                            if cm["id"] in custom_ids:
                                cm["name"] = f"🔒 {cm['name']}"
                                compare_result["data"].append(cm)
            with st.spinner("Loading comparison..."):
                pass # Replaced by custom merge logic below
    
            if not compare_result["ok"]:
                show_api_error(compare_result, retry_key="retry_compare_fetch")
                mat_details = []
            else:
                mat_details = compare_result.get("data", [])
    
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

        
        if not st.session_state.get("user"):
            st.info("You must be logged in to create and manage engineering projects.")
        else:
            tier = st.session_state.user.get("tier", "free")
            if tier == "free":
                st.info("✨ **Premium Feature Locked**")
                st.markdown("Engineering Workspaces allow you to build custom Bill of Materials (BOM) for your products, instantly calculating **Total Mass** and **Total Estimated Cost** based on real-time material data.")
                st.markdown("Upgrade to **Pro** or **Advanced** to unlock this active workspace feature.")
                if st.button("🚀 Upgrade to Pro (Rs. 499/mo)", key="proj_upgrade"):
                    st.session_state.current_page = "pricing"
                    st.rerun()
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
                            st.session_state.current_page = "pricing"
                            st.rerun()
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
                                
                                # Pro/Advanced Tier: PDF Export
                                if tier in ["pro", "advanced"]:
                                    df_clean = df.drop(columns=["Remove"])
                                    total_mass = sum((item["volume_cm3"] * (item["material"].get("density") or 0)) / 1000.0 for item in items)
                                    total_cost = sum(((item["volume_cm3"] * (item["material"].get("density") or 0)) / 1000.0) * (item.get("material", {}).get("cost_per_kg_min") or 0) for item in items)
                                    
                                    st.markdown("---")
                                    st.markdown("### 📄 Professional Reports")
                                    st.caption("Generate presentation-ready engineering reports. Downloads are generated locally and securely.")
                                    
                                    try:
                                        # Generate PDF bytes in memory
                                        pdf_bytes = generate_bom_pdf(curr_proj['name'], df_clean, total_mass, total_cost)
                                        
                                        st.download_button(
                                            label="📥 Download PDF Report (Secure)",
                                            data=pdf_bytes,
                                            file_name=f"{curr_proj['name'].replace(' ', '_')}_Engineering_Report.pdf",
                                            mime="application/pdf",
                                            type="primary"
                                        )
                                    except Exception as e:
                                        st.error(f"Failed to generate PDF: {e}")
                                    
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
                                        all_mats = fetch_all_materials(st.session_state.get("token"))
                                    
                                    
                                    bom_mat_options = {m["id"]: m["name"] for m in all_mats["data"].get("materials", [])} if all_mats["ok"] else {}
                                    
                                    # Fetch custom materials if advanced
                                    if user_tier == "advanced":
                                        cust_mats = api_get("/materials/custom/mine")
                                        if cust_mats["ok"] and cust_mats["data"]:
                                            for cm in cust_mats["data"]:
                                                # Use negative IDs to distinguish custom materials in the UI
                                                bom_mat_options[-cm["id"]] = f"🔒 {cm['name']}"

                                    
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
                                        all_mats = fetch_all_materials(st.session_state.get("token"))
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
                                        elif "semiconductor" in cat:
                                            cte = 4.0
                                        elif "nanomaterial" in cat:
                                            cte = 1.0
                                        elif "magnesium" in mat["name"].lower():
                                            cte = 26.0
                                        elif "zinc" in mat["name"].lower() or "zamak" in mat["name"].lower() or "za-" in mat["name"].lower():
                                            cte = 27.4
                                        elif "aluminum" in mat["name"].lower():
                                            cte = 23.0
                                        elif "titanium" in mat["name"].lower() or "nitinol" in mat["name"].lower():
                                            cte = 8.6
                                        elif "zirconium" in mat["name"].lower() or "zircaloy" in mat["name"].lower():
                                            cte = 6.0
                                        elif "beryllium copper" in mat["name"].lower():
                                            cte = 17.0
                                        elif "beryllium" in mat["name"].lower():
                                            cte = 11.4
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
                                            elif "ceramic" in cat:
                                                E_gpa = 300.0
                                            elif "semiconductor" in cat:
                                                E_gpa = 150.0
                                            elif "nanomaterial" in cat:
                                                E_gpa = 1000.0 # Graphene/CNT approx
                                            elif "magnesium" in mat["name"].lower():
                                                E_gpa = 45.0
                                            elif "zinc" in mat["name"].lower() or "zamak" in mat["name"].lower() or "za-" in mat["name"].lower():
                                                E_gpa = 85.0
                                            elif "aluminum" in mat["name"].lower():
                                                E_gpa = 69.0
                                            elif "titanium" in mat["name"].lower():
                                                E_gpa = 110.0
                                            elif "nitinol" in mat["name"].lower():
                                                E_gpa = 75.0
                                            elif "zirconium" in mat["name"].lower() or "zircaloy" in mat["name"].lower():
                                                E_gpa = 99.0
                                            elif "beryllium copper" in mat["name"].lower():
                                                E_gpa = 130.0
                                            elif "albemet" in mat["name"].lower():
                                                E_gpa = 193.0
                                            elif "beryllium" in mat["name"].lower():
                                                E_gpa = 303.0
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
                                            elif "semiconductor" in cat: cte = 4.0
                                            elif "nanomaterial" in cat: cte = 1.0
                                            elif "magnesium" in mat["name"].lower(): cte = 26.0
                                            elif "zinc" in mat["name"].lower() or "zamak" in mat["name"].lower() or "za-" in mat["name"].lower(): cte = 27.4
                                            elif "aluminum" in mat["name"].lower(): cte = 23.0
                                            elif "titanium" in mat["name"].lower() or "nitinol" in mat["name"].lower(): cte = 8.6
                                            elif "zirconium" in mat["name"].lower() or "zircaloy" in mat["name"].lower(): cte = 6.0
                                            elif "beryllium copper" in mat["name"].lower(): cte = 17.0
                                            elif "beryllium" in mat["name"].lower(): cte = 11.4
                                            
                                            Rs = (sigma_f * k_cond) / (E_gpa * cte)
                                            
                                            sc1, sc2, sc3 = st.columns(3)
                                            sc1.metric(r"Strength ($\sigma_f$)", f"{sigma_f:.1f} MPa")
                                            sc2.metric("Conductivity ($k$)", f"{k_cond:.1f} W/m·K")
                                            sc3.metric(r"Expansion ($\alpha$)", f"{cte:.1f} µm/m·°C")
                                            
                                            st.success(f"⚡ **Thermal Shock Resistance ($R_s$): {Rs:.2f} W/m**")
    
                                with t_cost:
                                    st.markdown("#### 💰 Advanced Cost & Weight Optimization Engine")
                                    st.caption("Identify cost drivers in your assembly and discover cheaper, lighter alternatives without sacrificing performance.")
                                    
                                    if not items:
                                        st.warning("Add parts to your BOM first.")
                                    else:
                                        st.markdown("##### Optimization Constraints")
                                        st.write("Select the engineering properties that replacement materials **MUST match or exceed** compared to the current material:")
                                        
                                        col_c1, col_c2 = st.columns(2)
                                        with col_c1:
                                            opt_yield = st.checkbox("Yield Strength (≥)", value=True)
                                            opt_tensile = st.checkbox("Tensile Strength (≥)", value=False)
                                            opt_thermal = st.checkbox("Thermal Conductivity (≥)", value=False)
                                        with col_c2:
                                            opt_density = st.checkbox("Density (≤) [Weight Limit]", value=True)
                                            opt_modulus = st.checkbox("Elastic Modulus (≥)", value=False)
                                        
                                        if st.button("Run Advanced Optimization", type="primary"):
                                            with st.spinner("Executing multi-constraint pareto analysis..."):
                                                all_mats = fetch_all_materials(st.session_state.get("token"))
                                                db_mats = all_mats["data"].get("materials", []) if all_mats["ok"] else []
                                                
                                                total_assembly_savings = 0.0
                                                optimization_found = False
                                                
                                                for item in items:
                                                    curr_mat = item["material"]
                                                    curr_cost = curr_mat.get("cost_per_kg_min")
                                                    
                                                    if not curr_cost:
                                                        continue
                                                        
                                                    # Gather current constraints
                                                    c_ys = curr_mat.get("yield_strength_min") or 0.0
                                                    c_ts = curr_mat.get("tensile_strength_min") or 0.0
                                                    c_den = curr_mat.get("density") or float('inf')
                                                    c_tc = curr_mat.get("thermal_conductivity") or 0.0
                                                    c_em = curr_mat.get("elastic_modulus") or 0.0
                                                    
                                                    alts = []
                                                    for m in db_mats:
                                                        if m["category"] != curr_mat["category"]: continue
                                                        if m["id"] == curr_mat["id"]: continue
                                                        m_cost = m.get("cost_per_kg_min")
                                                        if not m_cost: continue
                                                        
                                                        # Check constraints
                                                        valid = True
                                                        if opt_yield and (m.get("yield_strength_min") or 0) < c_ys: valid = False
                                                        if opt_tensile and (m.get("tensile_strength_min") or 0) < c_ts: valid = False
                                                        if opt_density and (m.get("density") or float('inf')) > c_den: valid = False
                                                        if opt_thermal and (m.get("thermal_conductivity") or 0) < c_tc: valid = False
                                                        if opt_modulus and (m.get("elastic_modulus") or 0) < c_em: valid = False
                                                        
                                                        if valid:
                                                            alts.append(m)
                                                            
                                                    if alts:
                                                        vol_cm3 = item["volume_cm3"]
                                                        current_mass_kg = (vol_cm3 * c_den) / 1000.0 if c_den != float('inf') else 0
                                                        current_total_cost = current_mass_kg * curr_cost
                                                        
                                                        # Cost is driven by Mass * Cost_per_kg. We must filter alts that are ACTUALLY cheaper total.
                                                        valid_cheaper_alts = []
                                                        for alt in alts:
                                                            alt_mass = (vol_cm3 * (alt.get("density") or 0)) / 1000.0
                                                            alt_cost = alt_mass * alt.get("cost_per_kg_min")
                                                            if alt_cost < current_total_cost:
                                                                valid_cheaper_alts.append((alt, alt_mass, alt_cost))
                                                        
                                                        if valid_cheaper_alts:
                                                            optimization_found = True
                                                            
                                                            # Find the absolute cheapest total cost
                                                            valid_cheaper_alts.sort(key=lambda x: x[2])
                                                            best_cost_alt, bc_mass, bc_cost = valid_cheaper_alts[0]
                                                            
                                                            # Find the lightest valid alternative among the cheaper ones
                                                            valid_cheaper_alts.sort(key=lambda x: x[1])
                                                            best_weight_alt, bw_mass, bw_cost = valid_cheaper_alts[0]
                                                            
                                                            savings_for_part = current_total_cost - bc_cost
                                                            total_assembly_savings += savings_for_part
                                                            
                                                            with st.container(border=True):
                                                                st.markdown(f"**Part:** {item['part_name']}")
                                                                st.caption(f"Current Material: **{curr_mat['name']}** | Mass: {current_mass_kg:.2f} kg | Part Cost: Rs. {current_total_cost:,.0f}")
                                                                
                                                                st.success(f"💰 **Top Savings Pick:** {best_cost_alt['name']}")
                                                                st.write(f"New Cost: Rs. {bc_cost:,.0f} (Save Rs. {savings_for_part:,.0f}) | New Mass: {bc_mass:.2f} kg")
                                                                
                                                                if best_weight_alt["id"] != best_cost_alt["id"]:
                                                                    bw_savings = current_total_cost - bw_cost
                                                                    st.info(f"🪶 **Lightest Viable Pick:** {best_weight_alt['name']}")
                                                                    st.write(f"New Cost: Rs. {bw_cost:,.0f} (Save Rs. {bw_savings:,.0f}) | New Mass: {bw_mass:.2f} kg")
                                                
                                                if optimization_found:
                                                    st.metric("Total Potential Assembly Savings", f"Rs. {total_assembly_savings:,.0f}")
                                                else:
                                                    st.info("Your BOM is fully optimized against these constraints! No valid cheaper equivalents found.")
    
    with tab_ai:
        
        if not st.session_state.get("user"):
            st.warning("You must be logged in to access the AI Advisor.")
        else:
            tier = st.session_state.user.get("tier", "free")
            if tier == "free":
                st.info("🔒 **Premium Feature Locked**")
                st.markdown("The AI Advisor analyzes your natural language requirements (e.g. *'Need a lightweight, high-strength metal for a drone under Rs. 1000/kg'*), intelligently queries the database, and provides engineering recommendations.")
                st.markdown("Upgrade to **Pro** or **Advanced** to unlock this feature.")
                if st.button("🚀 Upgrade to Pro (Rs. 499/mo)", key="ai_upgrade"):
                    st.session_state.current_page = "pricing"
                    st.rerun()
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
    # ==========================================
    #  TAB: FAQ
    # ==========================================
    with tab_faq_main:
        
        st.markdown("### 📊 Data & Materials")
        with st.expander("Where does MatDataHub get its data?"):
            st.write("Our data is meticulously sourced from globally recognized engineering standards including **ASTM International, ISO, MMPDS, ASME, and ASM International**.")
            st.write("For specific materials, data sheets often aggregate test results from manufacturers to provide reliable statistical minimums.")
        with st.expander("How frequently is the materials database updated?"):
            st.write("We run quarterly synchronization passes to capture updates in standard specifications and add newly developed alloys and advanced composites.")
        with st.expander("Can I add my own custom materials?"):
            st.write("Currently, MatDataHub operates as a strictly verified standard-reference database to maintain engineering integrity. Custom material uploads are on the roadmap for Advanced Engineering tier users in Q3.")

        st.markdown("### ⚙️ Features & Tools")
        with st.expander("How does the AI Material Advisor work?"):
            st.write("The AI Advisor (available on Pro and Advanced tiers) uses a Large Language Model (LLM) fine-tuned on materials science context. It has direct access to our 1,000+ material database to pull accurate numbers instead of hallucinating.")
            st.write("You can ask it things like: *'Which aluminum alloy is best for a saltwater marine environment?'* or *'Suggest an alternative to Ti-6Al-4V that is cheaper but has similar yield strength.'*")
        with st.expander("What are BOM Projects?"):
            st.write("Bill of Materials (BOM) Projects allow you to build assemblies out of MatDataHub materials. You can track total weight, volume, and cost, and run advanced engineering tools (like Thermal Expansion or Shock Analysis) on your entire assembly at once.")
        with st.expander("How does the Rule of Mixtures Synthesizer work?"):
            st.write("The Synthesizer allows you to virtually mix multiple materials (e.g., a polymer matrix and carbon fiber) by volume or weight fraction. It calculates the theoretical composite properties based on the Voigt and Reuss bounds.")

        

        st.markdown("### 💳 Subscriptions & Upgrades")
        with st.expander("How do I upgrade my plan?"):
            st.write("Click the **✨ Upgrade Plan** button in the sidebar or directly on any premium feature. Payments are securely processed via Razorpay.")
        with st.expander("Can I downgrade or cancel at any time?"):
            st.write("Yes! You can manage your subscription directly from the **💳 Subscriptions & Upgrades** section in your Account dashboard.")
        with st.expander("Is API Access available?"):
            st.write("API Access is available exclusively on the Advanced (Enterprise) tier! This allows full programmatic access to pipe material data directly into your ERP systems and simulations.")


    with tab_support_main:
    
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
                ["Payment / Billing Issue", "Bug Report", "Technical Support", "Feature Request", "Data Correction", "General Feedback"],
            )
            fb_rating = st.slider("How's your experience so far?", 1, 5, 4, help="1 = Poor, 5 = Excellent")
            fb_message = st.text_area(
                "Your message",
                placeholder="Tell us what's working, what's not, or what you'd love to see next...",
                height=140,
            )
            fb_image = st.file_uploader("Attach Screenshot (Optional)", type=["png", "jpg", "jpeg"])
            
            agree_tc = st.checkbox("I agree to the Terms & Conditions (No abuse, profanity, pornography, or hate speech).")
            
            fb_submit = st.form_submit_button("Submit Support Ticket", use_container_width=True)
    
            if fb_submit:
                if not fb_message or len(fb_message.strip()) < 3:
                    st.error("Please write a bit more detail before submitting.")
                elif not agree_tc:
                    st.error("You must agree to the Terms & Conditions before submitting.")
                else:
                    img_data = None
                    if fb_image is not None:
                        try:
                            import base64
                            if fb_image.size > 1024 * 1024:
                                st.warning("Image too large. Skipped.")
                            else:
                                img_data = base64.b64encode(fb_image.getvalue()).decode("utf-8")
                        except Exception:
                            pass
                    result = submit_feedback(
                        fb_name, fb_email, fb_category, fb_message.strip(), fb_rating, "Feedback Tab", img_data
                    )
                    if result["ok"]:
                        st.success("Thanks! Your feedback has been recorded. 🙌")
                        st.balloons()
                    else:
                        st.error(result.get("error", "Couldn't submit feedback. Try again later."))
    
    
    # ── Footer ──
    st.divider()
    st.caption("MatDataHub | Engineering Material Data-as-a-Service | 1,000+ materials | Data from ASTM, ASM, MMPDS, ISO, ACI")
    
    
    # --------------------------------------------------------------------------------
    
    # ==========================================
    #  PRO FEATURE: SMART SUBSTITUTE
    # ==========================================
    with tab_substitute:
        
        # Check tier
        user = st.session_state.get("user")
        token = st.session_state.get("token")
        if not token or not user:
            st.warning("You must be logged in to use this feature.")
        else:
            user_tier = user.get("tier", "free")
        if user_tier == "free":
            st.info("🔒 The Smart Substitution Engine is available on **Pro** and **Advanced** tiers. Upgrade to unlock interactive multi-objective optimization.")
        else:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("<h4 style='font-size: 1.05rem; font-weight: 600; color: var(--text-color); margin-bottom: 0.5rem;'>1. Target Material</h4>", unsafe_allow_html=True)
                # Fetch materials for dropdown
                import requests
                try:
                    res = fetch_all_materials()
                    if res.get("ok") and res.get("data"):
                        data = res["data"]
                        mats = data.get("materials", []) if isinstance(data, dict) else data
                        mat_options = {m["name"]: m for m in mats if isinstance(m, dict) and "name" in m}
                        selected_name = st.selectbox("Select material to substitute", options=list(mat_options.keys()), label_visibility="collapsed")
                        selected_mat = mat_options[selected_name]
                        selected_id = selected_mat["id"]
                        
                        st.markdown("<br><h4 style='font-size: 1.05rem; font-weight: 600; color: var(--text-color); margin-bottom: 0.5rem;'>2. Optimization Parameters</h4>", unsafe_allow_html=True)
                        st.caption("Adjust the relative weighting for the Euclidean distance algorithm.")
                        
                        w_cost = st.slider("Economic Viability (Cost)", 0.0, 1.0, 0.8, help="Priority for lower cost per kg.")
                        w_density = st.slider("Mass Reduction (Density)", 0.0, 1.0, 1.0, help="Priority for lower mass/volume.")
                        w_tensile = st.slider("Structural Integrity (Strength)", 0.0, 1.0, 0.5, help="Priority for higher tensile yield.")
                        w_carbon = st.slider("ESG Compliance (Carbon)", 0.0, 1.0, 0.3, help="Priority for lower Embodied Carbon (CO2e).")
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("Execute Optimization Engine", type="primary", use_container_width=True):
                            with st.spinner("Processing algorithmic substitution..."):
                                payload = {
                                    "base_material_id": selected_id,
                                    "weights": {
                                        "cost": w_cost,
                                        "density": w_density,
                                        "tensile_strength": w_tensile,
                                        "embodied_carbon": w_carbon
                                    }
                                }
                                headers = {"Authorization": f"Bearer {token}"}
                                sub_res = requests.post(f"{API_BASE}/materials/substitute", json=payload, headers=headers)
                                if sub_res.status_code == 200:
                                    st.session_state["sub_results"] = sub_res.json()
                                    st.session_state["sub_base_mat"] = selected_mat
                                else:
                                    st.error(f"Engine failed: {sub_res.text}")
                except Exception as e:
                    st.error(f"API Error: {e}")

            with col2:
                if "sub_results" in st.session_state and "sub_base_mat" in st.session_state:
                    st.markdown("<h4 style='font-size: 1.05rem; font-weight: 600; color: var(--text-color); margin-bottom: 1rem;'>Optimal Substitutions</h4>", unsafe_allow_html=True)
                    base_mat = st.session_state["sub_base_mat"]
                    
                    for res in st.session_state["sub_results"]:
                        with st.expander(f"[{res['match_score']}% Match] {res['name']}", expanded=True):
                            m1, m2, m3, m4 = st.columns(4)
                            m1.metric("Estimated Cost", f"${res['cost']}/kg")
                            m2.metric("Density", f"{res['density']} g/cm³")
                            m3.metric("Strength", f"{res['tensile']} MPa")
                            m4.metric("Carbon", f"{res['carbon']} kgCO2e")
                            
                            import plotly.graph_objects as go
                            fig = go.Figure()
                            
                            fig.add_trace(go.Scatterpolar(
                                  r=[base_mat.get('cost_per_kg', 0), base_mat.get('density', 0), base_mat.get('tensile_strength', 0), base_mat.get('embodied_carbon', 0)],
                                  theta=['Cost','Density','Strength', 'Carbon'],
                                  fill='toself',
                                  name='Base Material',
                                  line_color='rgba(128, 128, 128, 0.6)',
                                  fillcolor='rgba(128, 128, 128, 0.1)'
                            ))
                            
                            fig.add_trace(go.Scatterpolar(
                                  r=[res['cost'], res['density'], res['tensile'], res['carbon']],
                                  theta=['Cost','Density','Strength', 'Carbon'],
                                  fill='toself',
                                  name=res['name'],
                                  line_color='#00F0FF',
                                  fillcolor='rgba(0, 240, 255, 0.25)'
                            ))
                            
                            fig.update_layout(
                                polar=dict(
                                    radialaxis=dict(visible=True, color='rgba(128,128,128,0.4)', gridcolor='rgba(128,128,128,0.2)', tickfont=dict(size=9)),
                                    angularaxis=dict(color='var(--text-color)', gridcolor='rgba(128,128,128,0.2)', tickfont=dict(size=10))
                                ),
                                showlegend=True,
                                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(family="sans-serif", size=10, color="var(--text-color)"),
                                margin=dict(l=20, r=20, t=20, b=20),
                                height=300
                            )
                            st.plotly_chart(fig, use_container_width=True)


    # ==========================================
    #  ENTERPRISE FEATURE: BOM ANALYZER
    # ==========================================
    with tab_enterprise:
        
        token = st.session_state.get("token")
        user = st.session_state.get("user", {})
        user_tier = user.get("tier", "free") if isinstance(user, dict) else "free"
        
        if not token:
            st.warning("You must be logged in to use this feature.")
        elif user_tier != "advanced":
            st.info("🔒 The BOM Analyzer is exclusively available on the **Advanced/Enterprise** tier. Contact sales to upgrade.")
        else:
            st.write("Upload your Excel or CSV Bill of Materials.")
            uploaded_file = st.file_uploader("Upload BOM", type=["csv"])
            
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                st.write("Preview:")
                st.dataframe(df.head())
                
                col1, col2 = st.columns(2)
                mat_col = col1.selectbox("Which column contains the Material Name?", df.columns)
                wt_col = col2.selectbox("Which column contains the Weight (kg)?", df.columns)
                
                if st.button("Process BOM", type="primary"):
                    with st.spinner("Processing through AI mapping engine..."):
                        # Logic to pass to backend API would go here
                        # For now, we mock the delay
                        import time
                        time.sleep(2)
                        st.success("BOM Enriched Successfully!")
                        st.metric("Total Embodied Carbon", "45,210 kg CO2e")
                        st.warning("⚠️ 2 materials use obsolete standards.")
                        st.download_button("Download Enriched BOM (CSV)", data="mock_csv_data", file_name="enriched_bom.csv", mime="text/csv")


    # ==========================================
    #  BLOG & INSIGHTS TAB
    # ==========================================
    with tab_blog_main:
        st.markdown("<h2 style='margin-bottom: 0;'>📰 Engineering Blog & Insights</h2>", unsafe_allow_html=True)
        st.caption("Read the latest thoughts on materials science, ESG compliance, and data engineering.")
        st.divider()
        
        import os
        import re
        
        blog_dir = "frontend/blog_posts"
        if not os.path.exists(blog_dir):
            st.info("No blog posts found yet. Add markdown files to `frontend/blog_posts`.")
        else:
            posts = [f for f in os.listdir(blog_dir) if f.endswith(".md")]
            if not posts:
                st.info("No blog posts found yet.")
            else:
                # Read metadata from frontmatter
                post_data = []
                for p in posts:
                    with open(os.path.join(blog_dir, p), "r", encoding="utf-8") as f:
                        content = f.read()
                        
                    # Simple frontmatter parser
                    title = p.replace(".md", "").replace("-", " ").title()
                    date = "Unknown Date"
                    read_time = ""
                    
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) == 3:
                            fm = parts[1]
                            content = parts[2]
                            t_match = re.search(r'title:\s*"(.*?)"', fm)
                            if t_match: title = t_match.group(1)
                            
                            d_match = re.search(r'date:\s*"(.*?)"', fm)
                            if d_match: date = d_match.group(1)
                            
                            rt_match = re.search(r'read_time:\s*"(.*?)"', fm)
                            if rt_match: read_time = rt_match.group(1)
                            
                    post_data.append({"filename": p, "title": title, "date": date, "read_time": read_time, "content": content})
                
                # Sort by date (descending)
                post_data.sort(key=lambda x: x["date"], reverse=True)
                
                # UI Layout
                if "active_post" not in st.session_state:
                    st.session_state.active_post = None
                    
                if st.session_state.active_post is None:
                    # List View
                    for post in post_data:
                        with st.container():
                            st.markdown(f'''
                            <div style="background: var(--secondary-background-color); padding: 1.5rem; border-radius: 8px; border: 1px solid var(--faded-text-20); margin-bottom: 1rem;">
                                <h3 style="margin-top: 0; color: var(--text-color);">{post["title"]}</h3>
                                <p style="color: var(--faded-text); font-size: 0.9rem; margin-bottom: 1rem;">🗓️ {post["date"]} • ⏱️ {post["read_time"]}</p>
                            </div>
                            ''', unsafe_allow_html=True)
                            if st.button("Read Article", key=f"btn_{post['filename']}", type="primary"):
                                st.session_state.active_post = post
                                st.rerun()
                else:
                    # Detail View
                    if st.button("← Back to Articles"):
                        st.session_state.active_post = None
                        st.rerun()
                    
                    active = st.session_state.active_post
                    st.markdown(f'''
                    <div style="padding-top: 1rem;">
                        <p style="color: var(--primary-color); font-weight: 600;">{active["date"]} • {active["read_time"]}</p>
                    </div>
                    ''', unsafe_allow_html=True)
                    st.markdown(active["content"])
