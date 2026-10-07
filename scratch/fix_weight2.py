import sys
content = open('app/workflows.py', 'r', encoding='utf-8').read()

old_def = 'def process_bom(self, df, material_col, weight_col, strict_mode=True, disable_deminimis=False):'
new_def = 'def process_bom(self, df, material_col, weight_col, strict_mode=True, disable_deminimis=False, delimiter=","):'
content = content.replace(old_def, new_def)

old_weight = """                    if isinstance(raw_weight, str):
                        rw_str = str(raw_weight).strip()
                        # If format is 1.500,50 (European with dot thousands and comma decimal)
                        if re.match(r'^\d{1,3}(?:\.\d{3})*,\d+$', rw_str):
                            rw_str = rw_str.replace('.', '').replace(',', '.')
                        else:
                            # Standard US format or just comma thousands (1,500.50)
                            rw_str = rw_str.replace(',', '')
                        raw_weight = rw_str"""

new_weight = """                    if isinstance(raw_weight, str):
                        rw_str = str(raw_weight).strip()
                        rw_str = rw_str.replace(' ', '')
                        
                        import re
                        if delimiter == ';':
                            # European convention: dot is thousands, comma is decimal
                            if re.match(r'^\d{1,3}(?:\.\d{3})*,\d+$', rw_str):
                                rw_str = rw_str.replace('.', '').replace(',', '.')
                            elif re.match(r'^\d+,\d+$', rw_str):
                                rw_str = rw_str.replace(',', '.')
                            elif re.match(r'^\d{1,3}(?:\.\d{3})+$', rw_str):
                                rw_str = rw_str.replace('.', '')
                            else:
                                rw_str = rw_str.replace('.', '') # catch all for remaining dots
                        else:
                            # US convention: comma is thousands, dot is decimal
                            if re.match(r'^\d{1,3}(?:,\d{3})*\.\d+$', rw_str):
                                rw_str = rw_str.replace(',', '')
                            elif re.match(r'^\d{1,3}(?:,\d{3})+$', rw_str):
                                rw_str = rw_str.replace(',', '')
                            else:
                                rw_str = rw_str.replace(',', '')
                        raw_weight = rw_str"""

if old_weight in content:
    with open('app/workflows.py', 'w', encoding='utf-8') as f:
        f.write(content.replace(old_weight, new_weight))
    print('Replaced')
else:
    print('Not found')
