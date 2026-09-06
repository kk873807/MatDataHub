import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace tabs declaration
old_tabs = """    with tab_analytics:
        st.markdown("## \u2696\ufe0f Advanced Analytics & AI Substitution")
        st.caption("Compare materials side-by-side or use our proprietary AI to mathematically calculate the perfect supply chain substitute.")
        st.divider()
        tab_compare, tab_substitute = st.tabs(["\u2696\ufe0f Side-by-Side Compare", "\U0001f504 Smart AI Substitution (PRO)"])"""

new_tabs = """    with tab_analytics:
        st.markdown("## \u2696\ufe0f Advanced Analytics & AI Substitution")
        st.caption("Compare materials side-by-side, leverage AI for algorithmic substitution, or audit geopolitical risk and carbon taxes.")
        st.divider()
        tab_compare, tab_substitute, tab_risk = st.tabs(["\u2696\ufe0f Side-by-Side Compare", "\U0001f504 Smart AI Substitution (PRO)", "\U0001f30d Supply Chain Risk & CBAM (ENT)"])"""

if old_tabs in content:
    content = content.replace(old_tabs, new_tabs)
else:
    print("WARNING: Could not find old tabs declaration to replace.")

# 2. Insert tab_risk implementation
risk_code = """
    # ==========================================
    #  ENTERPRISE FEATURE: RISK & CBAM AUDITOR
    # ==========================================
    with tab_risk:
        token = st.session_state.get("token")
        user = st.session_state.get("user", {})
        user_tier = user.get("tier", "free") if isinstance(user, dict) else "free"
        
        if not token:
            st.warning("You must be logged in to use this feature.")
        elif user_tier != "advanced":
            st.info("\U0001f512 The Global Risk & CBAM Auditor is an **Enterprise** exclusive feature. Contact sales to upgrade.")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### Bridge the Gap Between Engineering and Finance")
            st.markdown("- **EU-CBAM Financial Forecasting**: Calculate exact Carbon Border Adjustment Mechanism tax liabilities for your BOM.")
            st.markdown("- **Critical Mineral Risk**: Detect geopolitical supply chain risks (e.g., Cobalt, Nickel, Titanium dependencies).")
            st.markdown("- **Executive Dashboards**: Generate boardroom-ready financial risk reports.")
        else:
            st.markdown("### \U0001f30d Supply Chain Risk & EU-CBAM Auditor")
            st.write("Analyze the financial and geopolitical risk of your material sourcing strategies.")
            
            try:
                res = fetch_all_materials()
                if res.get("ok") and res.get("data"):
                    data = res["data"]
                    mats = data.get("materials", []) if isinstance(data, dict) else data
                    mat_options = {m["name"]: m for m in mats if isinstance(m, dict) and "name" in m}
                    
                    rcol1, rcol2 = st.columns([1, 2])
                    
                    with rcol1:
                        st.markdown("#### Scenario Configuration")
                        selected_name = st.selectbox("Select Target Material", options=list(mat_options.keys()), key="risk_select")
                        selected_mat = mat_options[selected_name]
                        
                        volume_tons = st.number_input("Annual Procurement Volume (Metric Tons)", min_value=1.0, value=150.0, step=10.0)
                        cbam_price = st.slider("Forecasted EU Carbon Price (\u20ac / Tonne CO2)", min_value=50, max_value=200, value=85)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        analyze_btn = st.button("Generate Risk Audit", type="primary", use_container_width=True)
                        
                    with rcol2:
                        if analyze_btn:
                            with st.spinner("Calculating geopolitical and financial risk exposure..."):
                                import time
                                time.sleep(0.5)
                                
                                # Calculations
                                embodied_carbon_per_kg = float(selected_mat.get("embodied_carbon") or 0.0)
                                total_carbon_tons = (embodied_carbon_per_kg * (volume_tons * 1000)) / 1000
                                annual_cbam_tax = total_carbon_tons * cbam_price
                                
                                material_cost_per_kg = float(selected_mat.get("cost_per_kg") or 0.0)
                                annual_material_cost = material_cost_per_kg * (volume_tons * 1000)
                                
                                tax_percentage = (annual_cbam_tax / annual_material_cost) * 100 if annual_material_cost > 0 else 0
                                
                                st.markdown("#### Financial Tax Exposure (EU CBAM 2027+)")
                                m1, m2, m3 = st.columns(3)
                                m1.metric("Annual Carbon (CO2e)", f"{total_carbon_tons:,.0f} Tons", delta_color="inverse")
                                m2.metric("Projected Carbon Tax", f"\u20ac{annual_cbam_tax:,.0f}", f"{tax_percentage:.1f}% overhead", delta_color="inverse")
                                m3.metric("Annual Material Spend", f"${annual_material_cost:,.0f}")
                                
                                st.markdown("#### Geopolitical Risk Assessment")
                                name_lower = selected_name.lower()
                                risk_level = "Low"
                                risk_color = "#4CAF50" # green
                                risk_text = "Stable global supply chain. Low risk of tariff shocks or export bans."
                                
                                if "titanium" in name_lower or "ti-" in name_lower:
                                    risk_level = "CRITICAL"
                                    risk_color = "#F44336" # red
                                    risk_text = "High dependency on CIS region (Russia/Ukraine) and China. High risk of export quotas."
                                elif "cobalt" in name_lower or "nickel" in name_lower or "inconel" in name_lower:
                                    risk_level = "HIGH"
                                    risk_color = "#FF9800" # orange
                                    risk_text = "Heavy reliance on DRC and Indonesian supply chains. Subject to high price volatility and ESG sourcing risks."
                                elif "aluminum" in name_lower or "al-" in name_lower:
                                    risk_level = "MEDIUM"
                                    risk_color = "#FFEB3B" # yellow
                                    risk_text = "Energy-intensive refining process. Supply stability is highly correlated with global energy prices."
                                elif "steel" in name_lower:
                                    risk_level = "MEDIUM"
                                    risk_color = "#FFEB3B"
                                    risk_text = "Subject to heavy global tariffs and anti-dumping regulations. Medium supply volatility."
                                
                                st.markdown(f'''
                                <div style="background: rgba(128,128,128,0.1); padding: 1rem; border-left: 4px solid {risk_color}; border-radius: 6px; margin-bottom: 1rem;">
                                    <h4 style="margin-top:0; color: var(--text-color);">Supply Chain Risk: <span style="color: {risk_color};">{risk_level}</span></h4>
                                    <p style="margin-bottom:0; color: var(--text-color); opacity: 0.8;">{risk_text}</p>
                                </div>
                                ''', unsafe_allow_html=True)
                                
                                # Trajectory Chart
                                import plotly.graph_objects as go
                                years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
                                tax_phase_in = [0, 0, 0.05, 0.20, 0.50, 0.80, 1.0] # EU CBAM phase-in schedule
                                projected_costs = [annual_cbam_tax * p for p in tax_phase_in]
                                
                                fig = go.Figure()
                                fig.add_trace(go.Scatter(x=years, y=projected_costs, mode='lines+markers', name='Carbon Tax Exposure (\u20ac)', line=dict(color='#ff4b4b', width=3)))
                                fig.update_layout(
                                    title="Projected EU-CBAM Financial Impact (2024-2030)",
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    font=dict(color='var(--text-color)'),
                                    margin=dict(l=0, r=0, t=40, b=0),
                                    height=250,
                                    xaxis=dict(gridcolor='rgba(128,128,128,0.2)'),
                                    yaxis=dict(gridcolor='rgba(128,128,128,0.2)')
                                )
                                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Failed to load module: {e}")

"""

# Find where tab_enterprise starts and inject risk_code before it
target = "    # ==========================================\n    #  ENTERPRISE FEATURE: BOM ANALYZER"
if target in content:
    content = content.replace(target, risk_code + target)
    print("Risk Tab added successfully.")
else:
    print("WARNING: Could not find target to insert Risk tab.")

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)
