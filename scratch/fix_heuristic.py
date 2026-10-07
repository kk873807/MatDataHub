import sys
content = open('app/workflows.py', 'r', encoding='utf-8').read()

old_heuristic = """                    # Coarse non-CBAM class check based on material name
                    mat_name_lower = str(raw_name).lower() if raw_name else ""
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

new_heuristic = """                    # Coarse non-CBAM class check based on material name
                    mat_name_lower = str(raw_name).lower() if raw_name else ""
                    non_cbam_keywords = ["plastic", "glass", "textile", "electronic", "polymer", "wood", "paper", "copper", "pcb", "battery", "rubber", "leather", "ceramic"]
                    cbam_terms = ["steel", "iron", "aluminium", "aluminum", "cement", "fertiliser", "fertilizer", "hydrogen"]
                    
                    if any(kw in mat_name_lower for kw in non_cbam_keywords) and not any(term in mat_name_lower for term in cbam_terms):
                        is_out_of_scope = True
                        notes.append("OUT OF SCOPE (assumed from name)")
                        errors = [e for e in errors if "Missing CN Code" not in e and "Missing CN code" not in e]
                        # Remove quarantine reasons too
                        quarantine_reasons = [q for q in quarantine_reasons if "Missing CN Code" not in q]
                    else:
                        errors.append("Missing CN code and sector - cannot determine CBAM scope")
                        quarantine_reasons.append("Needs data: provide CN code or CBAM sector")"""

if old_heuristic in content:
    with open('app/workflows.py', 'w', encoding='utf-8') as f:
        f.write(content.replace(old_heuristic, new_heuristic))
    print('Updated heuristic')
else:
    print('Heuristic not found')
