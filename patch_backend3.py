import os

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "r", encoding="utf-8") as f:
    code = f.read()

old_cn_code = """            # CN Code Validation
            cn_code = extract_string(['cn_code', 'hs_code', 'cn code'])
            if cn_code:
                # Strip spaces, dots, hyphens
                clean_cn = cn_code.replace(" ", "").replace(".", "").replace("-", "")
                if not clean_cn.isdigit() or len(clean_cn) < 4:
                    errors.append("Invalid CN Code format")
            else:
                pass # Only flag if explicitly required by business rules, but user mainly cared about malformed ones"""

new_cn_code = """            # CN Code Validation
            cn_code = extract_string(['cn_code', 'hs_code', 'cn code'])
            clean_cn = ""
            if cn_code:
                # Strip spaces, dots, hyphens
                clean_cn = cn_code.replace(" ", "").replace(".", "").replace("-", "")
                if not clean_cn.isdigit() or len(clean_cn) < 4:
                    errors.append("Invalid CN Code format")
            else:
                pass # Only flag if explicitly required by business rules, but user mainly cared about malformed ones"""
code = code.replace(old_cn_code, new_cn_code)

old_match_logic = """            # Post-match: reject steel subfamily mismatches."""
new_match_logic = """            # Cross-validate CN Code against Sector
            if clean_cn and sector_lower:
                if "steel" in sector_lower or "iron" in sector_lower:
                    if not clean_cn.startswith(("72", "73", "26")):
                        errors.append("CN Code does not match Iron & Steel sector")
                elif "cement" in sector_lower:
                    if not clean_cn.startswith("2523"):
                        errors.append("CN Code does not match Cement sector")
                elif "alumin" in sector_lower:
                    if not clean_cn.startswith("76"):
                        errors.append("CN Code does not match Aluminium sector")
                elif "fertil" in sector_lower:
                    if not clean_cn.startswith(("2808", "2814", "2834", "3102", "3105")):
                        errors.append("CN Code does not match Fertilisers sector")

            # Post-match: reject steel subfamily mismatches."""
code = code.replace(old_match_logic, new_match_logic)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Workflows patched with CN code contradiction logic.")
