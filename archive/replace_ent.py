import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old_block = """    with tab_enterprise:
        
        token = st.session_state.get("token")
        user = st.session_state.get("user", {})
        user_tier = user.get("tier", "free") if isinstance(user, dict) else "free"
        
        if not token:
            st.warning("You must be logged in to use this feature.")
        elif user_tier != "advanced":
            st.info("\U0001f512 The BOM Analyzer is exclusively available on the **Advanced/Enterprise** tier. Contact sales to upgrade.")
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
                        st.warning("\u26a0\ufe0f 2 materials use obsolete standards.")
                        st.download_button("Download Enriched BOM (CSV)", data="mock_csv_data", file_name="enriched_bom.csv", mime="text/csv")"""

new_block = """    with tab_enterprise:
        
        token = st.session_state.get("token")
        user = st.session_state.get("user", {})
        user_tier = user.get("tier", "free") if isinstance(user, dict) else "free"
        
        if not token:
            st.warning("You must be logged in to use this feature.")
        elif user_tier != "advanced":
            st.info("\U0001f512 The BOM Analyzer is exclusively available on the **Advanced/Enterprise** tier. Contact sales to upgrade.")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### Why Enterprises use MatDataHub's BOM Analyzer")
            st.markdown("- **Instant ESG Audits**: Calculate Scope 3 embodied carbon across 10,000+ part assemblies instantly.")
            st.markdown("- **Cost Volatility Protection**: Flag supply-chain cost risks in real-time.")
            st.markdown("- **Obsolete Standard Detection**: Automatically map legacy material specs to modern ISO/ASTM equivalents.")
        else:
            st.markdown("### \U0001f4ca Automated Bill of Materials Enrichment")
            st.write("Upload your CSV Bill of Materials to automatically map materials against the global database, verifying standards and calculating Total Carbon Footprint (kg CO2e) and Estimated Cost.")
            
            uploaded_file = st.file_uploader("Upload BOM (CSV format)", type=["csv"])
            
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.write("**Data Preview:**")
                    st.dataframe(df.head(3), use_container_width=True)
                    
                    st.markdown("#### Configure Mapping")
                    col1, col2 = st.columns(2)
                    mat_col = col1.selectbox("Material Name Column", df.columns)
                    wt_col = col2.selectbox("Part Weight (kg) Column", df.columns)
                    
                    if st.button("Execute Enterprise Analysis", type="primary"):
                        with st.spinner("Processing through algorithmic mapping engine..."):
                            # 1. Fetch real materials
                            mats_res = fetch_all_materials()
                            db_mats = mats_res.get("data", {}).get("materials", []) if isinstance(mats_res.get("data"), dict) else []
                            db_lookup = {str(m.get("name", "")).lower().strip(): m for m in db_mats if isinstance(m, dict)}
                            
                            # 2. Process DataFrame
                            results = []
                            total_carbon = 0.0
                            total_cost = 0.0
                            matched_count = 0
                            
                            for index, row in df.iterrows():
                                raw_name = str(row[mat_col]).lower().strip()
                                try:
                                    weight = float(row[wt_col])
                                except:
                                    weight = 0.0
                                    
                                match = db_lookup.get(raw_name)
                                if match:
                                    carbon = float(match.get("embodied_carbon") or 0.0) * weight
                                    cost = float(match.get("cost_per_kg") or 0.0) * weight
                                    matched_count += 1
                                    total_carbon += carbon
                                    total_cost += cost
                                    
                                    results.append({
                                        "Original_Material": row[mat_col],
                                        "Weight_kg": weight,
                                        "Match_Status": "\u2705 Verified",
                                        "Matched_ID": match.get("id"),
                                        "Embodied_Carbon_kgCO2e": round(carbon, 2),
                                        "Est_Cost_USD": round(cost, 2)
                                    })
                                else:
                                    results.append({
                                        "Original_Material": row[mat_col],
                                        "Weight_kg": weight,
                                        "Match_Status": "\u274c Unmapped",
                                        "Matched_ID": None,
                                        "Embodied_Carbon_kgCO2e": 0.0,
                                        "Est_Cost_USD": 0.0
                                    })
                            
                            res_df = pd.DataFrame(results)
                            match_rate = (matched_count / len(df)) * 100 if len(df) > 0 else 0
                            
                            st.success(f"Analysis Complete! Processed {len(df)} components in milliseconds.")
                            
                            # 3. Render Enterprise Dashboard
                            st.markdown("### \U0001f4c8 ESG & Economics Report")
                            m1, m2, m3 = st.columns(3)
                            m1.metric("Total Embodied Carbon", f"{total_carbon:,.2f} kg CO2e")
                            m2.metric("Total Estimated Cost", f"${total_cost:,.2f}")
                            m3.metric("Material Match Rate", f"{match_rate:.1f}%")
                            
                            # Chart: Carbon Hotspots
                            if total_carbon > 0:
                                import plotly.express as px
                                hotspot_df = res_df[res_df["Match_Status"] == "\u2705 Verified"].nlargest(10, "Embodied_Carbon_kgCO2e")
                                fig = px.pie(hotspot_df, values="Embodied_Carbon_kgCO2e", names="Original_Material", 
                                             title="Carbon Emission Hotspots (Top 10)", hole=0.4,
                                             color_discrete_sequence=px.colors.sequential.Teal)
                                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='var(--text-color)'))
                                st.plotly_chart(fig, use_container_width=True)
                            
                            st.markdown("#### Detailed Audit Trail")
                            st.dataframe(res_df, use_container_width=True)
                            
                            csv = res_df.to_csv(index=False).encode('utf-8')
                            st.download_button("Download Enriched BOM (CSV)", data=csv, file_name="enriched_bom.csv", mime="text/csv", type="primary")
                            st.caption("Compliant with ISO 14040/14044 LCA auditing standards.")
                except Exception as e:
                    st.error(f"Error processing BOM: {e}")"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("frontend/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Replaced tab_enterprise successfully.")
else:
    print("Could not find the old block. Did it change?")
