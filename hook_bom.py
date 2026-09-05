with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

mock_bom_code = """                if st.button("Process BOM", type="primary"):
                    with st.spinner("Processing through AI mapping engine..."):
                        # Logic to pass to backend API would go here
                        # For now, we mock the delay
                        import time
                        time.sleep(2)
                        st.success("BOM Enriched Successfully!")
                        st.metric("Total Embodied Carbon", "45,210 kg CO2e")
                        st.warning(" 2 materials use obsolete standards.")
                        st.download_button("Download Enriched BOM (CSV)", data="mock_csv_data", file_name="enriched_bom.csv", mime="text/csv")"""

real_bom_code = """                if st.button("Process BOM", type="primary"):
                    with st.spinner("Processing through AI mapping engine..."):
                        try:
                            # Re-read file to pass to requests
                            uploaded_file.seek(0)
                            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                            data = {"material_col": mat_col, "weight_col": wt_col}
                            headers = {"Authorization": f"Bearer {token}"}
                            
                            bom_res = requests.post(f"{API_BASE}/materials/bom_analyze", files=files, data=data, headers=headers)
                            
                            if bom_res.status_code == 200:
                                st.success("BOM Enriched Successfully!")
                                
                                # Let's show a preview of the returned CSV
                                import io
                                enriched_df = pd.read_csv(io.StringIO(bom_res.text))
                                st.write("Enriched Output:")
                                st.dataframe(enriched_df.head())
                                
                                # Total carbon
                                if "Total_Carbon_kgCO2e" in enriched_df.columns:
                                    total_c = enriched_df["Total_Carbon_kgCO2e"].sum()
                                    st.metric("Total Embodied Carbon", f"{total_c:,.2f} kg CO2e")
                                
                                # Obsolete standards
                                if "Is_Obsolete" in enriched_df.columns:
                                    obs_count = (enriched_df["Is_Obsolete"] == "YES").sum()
                                    if obs_count > 0:
                                        st.warning(f"⚠️ {obs_count} materials use obsolete standards.")
                                
                                st.download_button("Download Enriched BOM (CSV)", data=bom_res.text, file_name="enriched_bom.csv", mime="text/csv")
                            else:
                                st.error(f"Failed to process BOM: {bom_res.text}")
                        except Exception as e:
                            st.error(f"Error during upload: {e}")"""

content = content.replace(mock_bom_code, real_bom_code)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Enterprise BOM hooked up to backend!")
