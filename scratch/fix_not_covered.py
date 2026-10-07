import sys
content = open('app/workflows.py', 'r', encoding='utf-8').read()

old_not_covered = """                    if cn_status == "NOT_COVERED":
                        errors.append(f"CN code '{clean_cn}' is not covered by CBAM Annex I")
                        is_out_of_scope = True
                        notes.append("CN code is not covered by CBAM Annex I")"""

new_not_covered = """                    if cn_status == "NOT_COVERED":
                        # hardcode electricity which is CBAM covered but might lack default values
                        if clean_cn.startswith('2716'):
                            cn_status = "EXACT_MATCH" # treat as covered
                            errors.append("No default values published for Electricity. Need actual data.")
                            quarantine_reasons.append("Electricity needs actual emissions data")
                        else:
                            errors.append(f"CN code '{clean_cn}' is not covered by CBAM Annex I")
                            is_out_of_scope = True
                            notes.append("CN code is not covered by CBAM Annex I")"""

if old_not_covered in content:
    with open('app/workflows.py', 'w', encoding='utf-8') as f:
        f.write(content.replace(old_not_covered, new_not_covered))
    print('Updated NOT_COVERED logic')
else:
    print('NOT_COVERED logic not found')
