import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find exactly the start of the block.
# We are looking for: user_tier = (st.session_state.user or {}).get("tier", "free")
start_idx = -1
for i, line in enumerate(lines):
    if 'user_tier = (st.session_state.user or {}).get("tier", "free")' in line:
        start_idx = i
        break

if start_idx == -1:
    print("Could not find start index")
    sys.exit(1)

# The end of the block is the line before TAB 2
end_idx = -1
for i in range(start_idx, len(lines)):
    if 'TAB 2: COMPARE MATERIALS' in line:
        # Actually, let's look for `# TAB 2: COMPARE MATERIALS`
        pass
    if '#  TAB 2: COMPARE MATERIALS' in lines[i]:
        end_idx = i - 1  # -1 because of the preceding `# -----------`
        break

print(f"Replacing from {start_idx + 1} to {end_idx - 1}")

new_block = """
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

"""

final_lines = lines[:start_idx + 1] + [new_block] + lines[end_idx:]

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.writelines(final_lines)
print("Block replaced successfully.")
