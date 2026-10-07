import sys
content = open('app/workflows.py', 'r', encoding='utf-8').read()

old_weight = """                    import math
                    if isinstance(raw_weight, str):
                        raw_weight = str(raw_weight).replace(',', '')
                    weight_kg = float(raw_weight) * weight_multiplier"""

new_weight = """                    import math
                    if isinstance(raw_weight, str):
                        rw_str = str(raw_weight).strip()
                        # If format is 1.500,50 (European with dot thousands and comma decimal)
                        if import_re.match(r'^\d{1,3}(?:\.\d{3})*,\d+$', rw_str):
                            rw_str = rw_str.replace('.', '').replace(',', '.')
                        else:
                            # Standard US format or just comma thousands (1,500.50)
                            rw_str = rw_str.replace(',', '')
                        raw_weight = rw_str
                    weight_kg = float(raw_weight) * weight_multiplier"""

if old_weight in content:
    # Need to import re inside the function, or at top level
    new_weight = new_weight.replace('import_re.match', 're.match')
    with open('app/workflows.py', 'w', encoding='utf-8') as f:
        f.write(content.replace(old_weight, new_weight))
    print('Replaced weight parsing')
else:
    print('Weight parsing not found')
