import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Define the boundaries of tab_risk
start_marker = "    # ==========================================\n    #  ENTERPRISE FEATURE: RISK & CBAM AUDITOR"
end_marker = "    # ==========================================\n    #  ENTERPRISE FEATURE: BOM ANALYZER"

if start_marker in content and end_marker in content:
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    old_risk_code = content[start_idx:end_idx]
    print("Found tab_risk block.")
else:
    print("Could not find boundaries.")
