import sys

new_block = """            with col1:
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
                                  line_color='rgba(255, 255, 255, 0.4)',
                                  fillcolor='rgba(255, 255, 255, 0.05)'
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
                                    radialaxis=dict(visible=True, color='rgba(255,255,255,0.2)', gridcolor='rgba(255,255,255,0.1)'),
                                    angularaxis=dict(color='var(--text-color)', gridcolor='rgba(255,255,255,0.1)')
                                ),
                                showlegend=True,
                                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(family="sans-serif", size=12, color="var(--text-color)"),
                                margin=dict(l=20, r=20, t=20, b=20),
                                height=300
                            )
                            st.plotly_chart(fig, use_container_width=True)\n"""

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if "with col1:" in line and "selected_name = st.selectbox" in "".join(lines[i:i+20]):
        start_idx = i
    if start_idx != -1 and "st.plotly_chart(fig, use_container_width=True)" in line:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    final_lines = lines[:start_idx] + [new_block] + lines[end_idx+1:]
    with open("frontend/app.py", "w", encoding="utf-8") as f:
        f.writelines(final_lines)
    print("Refactored Smart Substitution UI successfully!")
else:
    print("Could not find block boundaries")
