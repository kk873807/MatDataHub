import sys
content = open('app/workflows.py', 'r', encoding='utf-8').read()

old = """            else:
                if clean_cn:
                    # CN code positively identified as not in Annex I
                    is_out_of_scope = True
                    notes.append("CN code is not covered by CBAM Annex I")
                else:"""

new = """            else:
                if clean_cn:
                    if clean_cn.startswith('2716'):
                        errors.append("No default values published for Electricity. Need actual data.")
                        quarantine_reasons.append("Electricity needs actual emissions data")
                    else:
                        # CN code positively identified as not in Annex I
                        is_out_of_scope = True
                        notes.append("CN code is not covered by CBAM Annex I")
                else:"""

if old in content:
    with open('app/workflows.py', 'w', encoding='utf-8') as f:
        f.write(content.replace(old, new))
    print('Replaced')
else:
    print('Not found')
