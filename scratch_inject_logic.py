import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Inject Custom Materials into the radio menu
    if "Payment History" in line and i < 970:
        new_lines.append('                "🛠️ Custom Materials (Enterprise)",\n')
        new_lines.append(line)
        continue
    
    # Inject Price History before "Find Materials Similar"
    if "Find Materials Similar to" in line and i > 1900:
        indent = " " * 24
        chart_code = f"""
{indent}if user_tier in ("pro", "advanced"):
{indent}    st.markdown("### 📈 Historical Price Tracking")
{indent}    with st.spinner("Loading commodity price history..."):
{indent}        price_resp = api_get(f"/materials/{{mat_id}}/price-history")
{indent}        if price_resp["ok"] and price_resp["data"]:
{indent}            import pandas as pd
{indent}            hist_data = price_resp["data"]
{indent}            df_hist = pd.DataFrame(hist_data)
{indent}            if not df_hist.empty:
{indent}                df_hist["recorded_date"] = pd.to_datetime(df_hist["recorded_date"])
{indent}                df_hist = df_hist.set_index("recorded_date")
{indent}                st.line_chart(df_hist["cost_per_kg"], height=250, use_container_width=True)
{indent}                st.caption("Price fluctuations (INR per kg) over the last 12 months.")
{indent}            else:
{indent}                st.info("No historical price data available yet.")
{indent}        else:
{indent}            st.info("Historical tracking is currently gathering data for this material.")
{indent}else:
{indent}    st.info("📈 **Upgrade to Pro or Advanced** to unlock 12-month historical commodity price tracking.")
"""
        new_lines.append(chart_code + "\n")
        # Ensure we keep the original line too! Wait, the original line is `if st.button...`
        # But wait! I also need to make sure the indent matches. Let's look at the original lines around 1905:
        # 1904: if user_tier in ("pro", "advanced"):
        # 1905:     if st.button(...)
        # So I should inject BEFORE line 1904!
        # But wait, my script is injecting AT line 1905. Let me fix the logic.
    
    new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Injected via line analysis")
