import sys
content = open('app/workflows.py', 'r', encoding='utf-8').read()

old_lookup = """                    db_default, db_incl_indirect, db_source, match_level, default_meta = self._lookup_cbam_default(
                        cn_code or "", origin_country_raw or "", lookup_year
                    )
                    if db_default is not None:
                        carbon_factor = db_default"""

new_lookup = """                    db_default, db_incl_indirect, db_source, match_level, default_meta = self._lookup_cbam_default(
                        cn_code or "", origin_country_raw or "", lookup_year
                    )
                    if db_source == 'AMBIGUOUS':
                        errors.append(f"CN code '{cn_code}' matches an ambiguous prefix. Needs exact 8-digit CN code.")
                        quarantine_reasons.append("Needs exact 8-digit CN code (ambiguous prefix)")
                        db_default = None
                        db_source = None
                    if db_default is not None:
                        carbon_factor = db_default"""

if old_lookup in content:
    with open('app/workflows.py', 'w', encoding='utf-8') as f:
        f.write(content.replace(old_lookup, new_lookup))
    print('Replaced')
else:
    print('Not found')
