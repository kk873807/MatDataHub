with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

target = '        st.markdown("---")\n\n        # --- EXPLORE THE DOMAINS ---'

quick_actions = """        # --- QUICK ACTIONS ---
        st.markdown("### ⚡ Quick Actions")
        qa1, qa2, qa3 = st.columns(3)
        with qa1:
            st.info("🔄 **Smart Substitution**\\n\\nMathematically find alternative supply chain materials based on cost, weight, and carbon footprint.")
        with qa2:
            st.success("📊 **Enterprise BOM Analyzer**\\n\\nUpload a CSV assembly to instantly verify ESG compliance and obsolete global standards.")
        with qa3:
            st.warning("🤖 **AI Metallurgist**\\n\\nDescribe your engineering constraints in natural language and get instantaneous material recommendations.")
        
        st.markdown("---")

        # --- EXPLORE THE DOMAINS ---"""

content = content.replace(target, quick_actions)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Quick actions injected!")
