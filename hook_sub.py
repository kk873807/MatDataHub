import re

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

mock_sub_code = """                        if st.button("Calculate Alternatives", type="primary"):
                            with st.spinner("Running optimization engine..."):
                                st.session_state["sub_results"] = [
                                    {"name": "Dummy Material A", "match_score": 92.5, "cost": 4.5, "density": 2.7, "tensile": 310, "carbon": 8.1},
                                    {"name": "Dummy Material B", "match_score": 88.0, "cost": 5.0, "density": 2.8, "tensile": 330, "carbon": 9.0}
                                ]
                                st.success("Optimization complete!")"""

real_sub_code = """                        if st.button("Calculate Alternatives", type="primary"):
                            with st.spinner("Running optimization engine..."):
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
                                    st.success("Optimization complete!")
                                else:
                                    st.error(f"Engine failed: {sub_res.text}")"""

content = content.replace(mock_sub_code, real_sub_code)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Streamlit hooked up to real Substitution API!")
