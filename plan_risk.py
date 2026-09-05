import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update the Analytics tabs declaration
old_tabs_analytics = """    with tab_analytics:
        st.markdown("## \u2696\ufe0f Advanced Analytics & AI Substitution")
        st.caption("Perform rigorous side-by-side material comparisons and optimize supply chain alternatives.")
        st.divider()
        tab_compare, tab_substitute = st.tabs(["\u2696\ufe0f Side-by-Side Compare", "\U0001f504 Smart AI Substitution (PRO)"])"""

new_tabs_analytics = """    with tab_analytics:
        st.markdown("## \u2696\ufe0f Advanced Analytics & AI Substitution")
        st.caption("Perform rigorous side-by-side material comparisons and optimize supply chain alternatives.")
        st.divider()
        tab_compare, tab_substitute, tab_risk = st.tabs(["\u2696\ufe0f Side-by-Side Compare", "\U0001f504 Smart AI Substitution (PRO)", "\U0001f30d Global Risk & CBAM Auditor (ENT)"])"""

if old_tabs_analytics in content:
    content = content.replace(old_tabs_analytics, new_tabs_analytics)
    print("Analytics tabs updated.")
else:
    print("Could not find Analytics tabs declaration.")

# 2. Append tab_risk logic at the end of the file (before the Blog logic if possible, or just at the end inside the main page block)
# Actually, the safest way is to find the end of tab_substitute and insert tab_risk right after it.
