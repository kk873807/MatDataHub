import os

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update indirect emissions scope rule for CBAM
# Indirect emissions are only covered for Cement and Fertilisers!
old_carbon_factor = """            provided_carbon_factor = None
            if direct_em is not None and indirect_em is not None:
                provided_carbon_factor = direct_em + indirect_em
            elif direct_em is not None:
                provided_carbon_factor = direct_em
                
            # --- Sector-aware fuzzy matching ---"""

new_carbon_factor = """            # --- Sector-aware fuzzy matching ---"""

code = code.replace(old_carbon_factor, new_carbon_factor)

old_match = """            # Post-match: reject steel subfamily mismatches."""
new_match = """            
            provided_carbon_factor = None
            # CBAM scope rules: Indirect emissions only count for Cement and Fertilisers.
            # They are excluded for Iron & Steel, Aluminium, and Hydrogen.
            includes_indirect = False
            if allowed_cats is not None:
                # Based on the CBAM_SECTOR_CATEGORY_MAP logic above
                if any(k in sector_lower for k in ['cement', 'fertili']):
                    includes_indirect = True
            
            if direct_em is not None:
                provided_carbon_factor = direct_em
                if includes_indirect and indirect_em is not None:
                    provided_carbon_factor += indirect_em

            # Post-match: reject steel subfamily mismatches."""
code = code.replace(old_match, new_match)

# Make sure `allowed_cats` and `sector_lower` exist when checking `includes_indirect`
# `allowed_cats` is set just above the fuzzy matching.
# Wait, if `cbam_sector` is empty, `allowed_cats` won't be defined unless it's in the if block.
# Let's fix the scoping of `allowed_cats` and `sector_lower`.

old_sector = """            if cbam_sector and cbam_sector.lower() not in ('nan', ''):
                sector_lower = cbam_sector.strip().lower()
                allowed_cats = None"""
new_sector = """            sector_lower = ""
            allowed_cats = None
            if cbam_sector and cbam_sector.lower() not in ('nan', ''):
                sector_lower = cbam_sector.strip().lower()"""
code = code.replace(old_sector, new_sector)


with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\app\workflows.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Workflows patched with indirect emissions logic.")
