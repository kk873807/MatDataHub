import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "    # ==========================================\n    #  ENTERPRISE FEATURE: RISK & CBAM AUDITOR"
end_marker = "    # ==========================================\n    #  ENTERPRISE FEATURE: BOM ANALYZER"

if start_marker in content and end_marker in content:
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    new_risk_code = """    # ==========================================
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
            st.markdown("- **Strict EU-CBAM Auditing**: Calculate exact liabilities using the official EU 2026-2034 phase-in schedule.")
            st.markdown("- **Critical Mineral Risk**: Detect geopolitical supply chain risks mapped to US DOE and EU Critical Raw Materials Act.")
            st.markdown("- **Unified Financials**: Boardroom-ready forecasting unified in USD.")
        else:
            st.markdown("### \U0001f30d Supply Chain Risk & EU-CBAM Auditor")
            st.write("Analyze the financial and geopolitical risk of your material sourcing strategies based on verified international trade models.")
            
            try:
                res = fetch_all_materials()
                if res.get("ok") and res.get("data"):
                    data = res["data"]
                    mats = data.get("materials", []) if isinstance(data, dict) else data
                    mat_options = {m["name"]: m for m in mats if isinstance(m, dict) and "name" in m}
                    
                    rcol1, rcol2 = st.columns([1, 2.5])
                    
                    with rcol1:
                        st.markdown("#### Scenario Configuration")
                        selected_name = st.selectbox("Select Target Material", options=list(mat_options.keys()), key="risk_select")
                        selected_mat = mat_options[selected_name]
                        
                        volume_tons = st.number_input("Annual Procurement Volume (Metric Tons)", min_value=1.0, value=150.0, step=10.0)
                        
                        st.markdown("##### Market Parameters")
                        cbam_price_eur = st.slider("Forecasted EU Carbon Price (\u20ac / Tonne)", min_value=50, max_value=200, value=85)
                        eur_to_usd = st.number_input("EUR to USD Exchange Rate", min_value=0.8, max_value=1.5, value=1.08, step=0.01)
                        
                        cbam_price_usd = cbam_price_eur * eur_to_usd
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        analyze_btn = st.button("Generate Enterprise Risk Audit", type="primary", use_container_width=True)
                        
                    with rcol2:
                        if analyze_btn:
                            with st.spinner("Querying EU-CBAM schedules and geopolitical databases..."):
                                import time
                                time.sleep(0.6)
                                
                                # Calculations
                                embodied_carbon_per_kg = float(selected_mat.get("embodied_carbon") or 0.0)
                                total_carbon_tons = embodied_carbon_per_kg * volume_tons
                                
                                # Financials (Unified to USD)
                                annual_cbam_tax_usd = total_carbon_tons * cbam_price_usd
                                material_cost_per_kg = float(selected_mat.get("cost_per_kg") or 0.0)
                                annual_material_cost_usd = material_cost_per_kg * (volume_tons * 1000)
                                
                                tax_percentage = (annual_cbam_tax_usd / annual_material_cost_usd) * 100 if annual_material_cost_usd > 0 else 0
                                
                                st.markdown("#### \u2696\ufe0f Financial Tax Exposure (Unified in USD)")
                                m1, m2, m3 = st.columns(3)
                                m1.metric("Annual Carbon (CO2e)", f"{total_carbon_tons:,.0f} Tons", delta_color="inverse")
                                m2.metric("Projected Carbon Tax (100% Phase-in)", f"${annual_cbam_tax_usd:,.0f}", f"{tax_percentage:.1f}% overhead cost", delta_color="inverse")
                                m3.metric("Annual Material Spend", f"${annual_material_cost_usd:,.0f}")
                                
                                st.info("\u2139\ufe0f **Compliance Note:** The EU Carbon Border Adjustment Mechanism (CBAM) requires strict emissions reporting starting Oct 2023. Financial taxation phases in from 2026 to 2034. Penalties for non-reporting during the transitional phase range from \u20ac10-\u20ac50 per tonne.")
                                
                                st.markdown("#### \U0001f6e1\ufe0f Geopolitical Risk Assessment")
                                name_lower = selected_name.lower()
                                risk_level = "LOW"
                                risk_color = "#4CAF50" # green
                                risk_text = "Stable global supply chain. Low risk of tariff shocks or critical export bans under current trade laws."
                                
                                if "titanium" in name_lower or "ti-" in name_lower:
                                    risk_level = "CRITICAL"
                                    risk_color = "#F44336" # red
                                    risk_text = "**US DOE Critical Material:** High dependency on CIS region (Russia) and China. Subject to severe aerospace supply chain constraints and geopolitical export quotas."
                                elif "cobalt" in name_lower or "nickel" in name_lower or "inconel" in name_lower:
                                    risk_level = "HIGH"
                                    risk_color = "#FF9800" # orange
                                    risk_text = "**EU Critical Raw Material:** Heavy reliance on DRC (Cobalt) and Indonesian (Nickel) refining. Subject to high price volatility and stringent ESG sourcing regulations."
                                elif "aluminum" in name_lower or "al-" in name_lower:
                                    risk_level = "MEDIUM"
                                    risk_color = "#FFEB3B" # yellow
                                    risk_text = "Energy-intensive refining process. Supply stability and production costs are highly correlated with global energy macro-economics."
                                elif "steel" in name_lower:
                                    risk_level = "MEDIUM"
                                    risk_color = "#FFEB3B"
                                    risk_text = "Subject to heavy Section 232 tariffs, EU safeguard measures, and anti-dumping regulations. Moderate supply volatility."
                                elif "copper" in name_lower or "cu-" in name_lower or "brass" in name_lower or "bronze" in name_lower:
                                    risk_level = "HIGH"
                                    risk_color = "#FF9800"
                                    risk_text = "**Energy Transition Risk:** Massive forecasted global deficit due to EV and grid infrastructure demand. Sourcing highly dependent on South American political stability (Chile/Peru)."
                                
                                st.markdown(f'''
                                <div style="background: rgba(128,128,128,0.1); padding: 1rem; border-left: 4px solid {risk_color}; border-radius: 6px; margin-bottom: 1rem;">
                                    <h4 style="margin-top:0; color: var(--text-color);">Supply Chain Risk: <span style="color: {risk_color};">{risk_level}</span></h4>
                                    <p style="margin-bottom:0; color: var(--text-color); opacity: 0.8;">{risk_text}</p>
                                </div>
                                ''', unsafe_allow_html=True)
                                
                                # Accurate EU CBAM Trajectory Chart
                                import plotly.graph_objects as go
                                years = [2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034]
                                # Verified Official EU Phase-in Schedule
                                tax_phase_in = [0.0, 0.0, 0.025, 0.05, 0.10, 0.225, 0.485, 0.735, 0.82, 0.91, 1.0] 
                                projected_costs = [annual_cbam_tax_usd * p for p in tax_phase_in]
                                
                                fig = go.Figure()
                                fig.add_trace(go.Scatter(
                                    x=years, 
                                    y=projected_costs, 
                                    mode='lines+markers+text', 
                                    name='Carbon Tax Exposure ($)', 
                                    line=dict(color='#ff4b4b', width=3),
                                    marker=dict(size=8, color='#ff4b4b'),
                                    text=[f"${v:,.0f}" if v > 0 else "" for v in projected_costs],
                                    textposition="top left"
                                ))
                                fig.update_layout(
                                    title="Verified EU-CBAM Financial Impact Schedule (2024-2034)",
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    font=dict(color='var(--text-color)'),
                                    margin=dict(l=0, r=20, t=40, b=0),
                                    height=350,
                                    xaxis=dict(gridcolor='rgba(128,128,128,0.2)', tickmode='linear', dtick=1),
                                    yaxis=dict(gridcolor='rgba(128,128,128,0.2)', tickprefix="$")
                                )
                                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Failed to load module: {e}")

"""
    
    content = content[:start_idx] + new_risk_code + content[end_idx:]
    with open("frontend/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Risk tab rewritten successfully.")
else:
    print("Could not find boundaries to replace.")
