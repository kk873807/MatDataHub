import sys
content = open('app/workflows.py', 'r', encoding='utf-8').read()

old_de_minimis = """            is_deminimis_eligible = "NO"
            if cn_status == "EXACT_MATCH" and sector_lower:
                if any(x in sector_lower for x in ['electric', 'hydrogen']):
                    notes.append(f"De minimis exemption does not apply to {sector_lower.title()}")
                elif "Origin is exempt" not in " | ".join(notes) and "Destination outside EU" not in " | ".join(notes):
                    is_deminimis_eligible = "YES\""""

new_de_minimis = """            is_deminimis_eligible = "NO"
            is_exempt = "Origin is exempt" in " | ".join(notes) or "Destination outside EU" in " | ".join(notes)
            
            is_elec_or_hydro = False
            if clean_cn:
                if clean_cn.startswith('2716'):
                    is_elec_or_hydro = True
                    notes.append("De minimis exemption does not apply to Electricity")
                elif clean_cn.startswith('2804'):
                    is_elec_or_hydro = True
                    notes.append("De minimis exemption does not apply to Hydrogen")
            
            if not is_elec_or_hydro:
                if cn_status == "EXACT_MATCH" and sector_lower and any(x in sector_lower for x in ['electric', 'hydrogen']):
                    is_elec_or_hydro = True
                    notes.append(f"De minimis exemption does not apply to {sector_lower.title()}")

            if not is_exempt and not is_elec_or_hydro and not is_out_of_scope and clean_cn:
                is_deminimis_eligible = "YES\""""

if old_de_minimis in content:
    with open('app/workflows.py', 'w', encoding='utf-8') as f:
        f.write(content.replace(old_de_minimis, new_de_minimis))
    print('Updated de minimis logic')
else:
    print('De minimis logic not found')
