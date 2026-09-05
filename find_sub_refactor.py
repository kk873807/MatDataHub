import sys
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
    print(f"Start: {start_idx}, End: {end_idx}")
else:
    print("Not found")
