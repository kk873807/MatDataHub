import sys
import re

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the API Key visibility in the Profile page
content = content.replace(
    'if user.get("tier") in ["pro", "advanced"]:',
    'if user.get("tier") == "advanced":'
)
content = content.replace(
    'st.warning("API Access is only available on the Pro and Advanced tiers.")',
    'st.warning("API Access is strictly reserved for the Advanced (Enterprise) tier.")'
)
content = content.replace(
    'API Access is available on the Pro and Advanced tiers! You can generate your secure `X-API-Key` directly from this Account Dashboard once you upgrade.',
    'API Access is available exclusively on the Advanced (Enterprise) tier! This allows full programmatic access to pipe material data directly into your ERP systems and simulations.'
)

# 2. Update the Pricing Page
content = content.replace(
    'st.markdown("## ₹1999 / mo")',
    'st.markdown("## ₹14999 / mo")'
)
content = content.replace(
    'st.markdown("- ✅ Unlimited Comparisons\\n- ✅ Cost Optimization Engine\\n- ✅ Download PDF Reports\\n- ✅ Priority Support")',
    'st.markdown("- ✅ Unlimited Comparisons\\n- ✅ Cost Optimization Engine\\n- ✅ Download PDF Reports\\n- ✅ Programmatic API Access")'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated frontend UI for Advanced Tier API isolation.")
