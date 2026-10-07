import sys, re
content = open('app/workflows.py', 'r', encoding='utf-8').read()

pattern = r'                else:\s*# No CN code AND no declared sector.*?quarantine_reasons\.append\("Needs data: provide CN code or CBAM sector"\)'

new_block = """                else:
                    # Coarse non-CBAM class check based on material name
                    mat_name_lower = str(mat_name).lower() if mat_name else ""
                    non_cbam_keywords = ["plastic", "glass", "textile", "electronic", "polymer", "wood", "paper", "copper", "pcb", "battery", "rubber", "leather", "ceramic"]
                    if any(kw in mat_name_lower for kw in non_cbam_keywords):
                        is_out_of_scope = True
                        notes.append("Positive non-CBAM material identified (e.g., polymer, glass, electronics)")
                        errors = [e for e in errors if "Missing CN Code" not in e and "Missing CN code" not in e]
                        # Remove quarantine reasons too
                        quarantine_reasons = [q for q in quarantine_reasons if "Missing CN Code" not in q]
                    else:
                        errors.append("Missing CN code and sector - cannot determine CBAM scope")
                        quarantine_reasons.append("Needs data: provide CN code or CBAM sector")"""

new_content = re.sub(pattern, new_block, content, flags=re.DOTALL)
if new_content != content:
    with open('app/workflows.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Replaced successfully")
else:
    print("Not found")
