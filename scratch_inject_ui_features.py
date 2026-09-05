import sys
import re

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Price History Chart to the Material Details View
chart_code = """
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
                            st.line_chart(df_hist["cost_per_kg"], height=250, use_container_width=True)
                            st.caption("Price fluctuations (INR per kg) over the last 12 months.")
                        else:
                            st.info("No historical price data available yet.")
                    else:
                        st.info("Historical tracking is currently gathering data for this material.")
            else:
                st.info("📈 **Upgrade to Pro or Advanced** to unlock 12-month historical commodity price tracking.")
"""
if "Historical Price Tracking" not in content:
    content = content.replace(
        'if user_tier in ("pro", "advanced"):\n                            if st.button(f"🔎 Find Materials Similar',
        chart_code + '\n                        if user_tier in ("pro", "advanced"):\n                            if st.button(f"🔎 Find Materials Similar'
    )

# 2. Add Custom Materials UI in Account Tab
custom_mat_ui = """
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
"""
if "Custom Materials (Enterprise)" not in content:
    content = content.replace(
        '"🔑 Profile & Security", ',
        '"🔑 Profile & Security", \n                "🛠️ Custom Materials (Enterprise)", '
    )
    content = content.replace(
        'elif account_menu == "💳 Payment History":',
        custom_mat_ui + '\n            elif account_menu == "💳 Payment History":'
    )

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Injected Price Chart and Custom Materials UI.")
