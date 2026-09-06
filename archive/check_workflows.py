import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if "with tab_workflows:" in line:
        start_idx = i
    if start_idx != -1 and "with tab_support_main:" in line:
        end_idx = i
        break
        
for i in range(start_idx, end_idx):
    print(f"Line {i}: {lines[i].strip()}")
