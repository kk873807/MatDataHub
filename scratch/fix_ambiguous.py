import sys
content = open('app/workflows.py', 'r', encoding='utf-8').read()

old_weight = """                            elif re.match(r'^\d{1,3}(?:\.\d{3})+$', rw_str):
                                rw_str = rw_str.replace('.', '')"""

new_weight = """                            elif re.match(r'^\d{1,3}\.\d{3}$', rw_str):
                                rw_str = rw_str.replace('.', '')
                                errors.append(f"Ambiguous weight format: '{raw_weight}'")
                                quarantine_reasons.append(f"Ambiguous weight format '{raw_weight}' - confirm if thousand or decimal")
                            elif re.match(r'^\d{1,3}(?:\.\d{3})+$', rw_str):
                                rw_str = rw_str.replace('.', '')"""

if old_weight in content:
    with open('app/workflows.py', 'w', encoding='utf-8') as f:
        f.write(content.replace(old_weight, new_weight))
    print('Added European ambiguous check')
else:
    print('European not found')
