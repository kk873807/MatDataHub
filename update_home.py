import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "    with tab_home:"
end_marker = "    with tab_guide:"

if start_marker in content and end_marker in content:
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)
    
    new_home = """    with tab_home:
        if st.session_state.get("user"):
            st.markdown(f\"\"\"
                <div style="background: rgba(79, 195, 161, 0.1); border-left: 4px solid #4FC3A1; border-radius: 4px; padding: 15px 20px; color: var(--text-color); margin-bottom: 2rem; font-weight: 500; font-size: 1.1rem; line-height: 1.5;">
                     Welcome back, <b style="color: #4FC3A1;">{st.session_state.user.get('name') or st.session_state.user['email']}</b> to MatDataHub! <br>
                    <span style="opacity: 0.85; font-size: 1rem; font-weight: 400;">Your enterprise command center for metallurgical analytics, ESG compliance, and supply chain optimization.</span>
                </div>
            \"\"\", unsafe_allow_html=True)
        else:
            st.markdown(\"\"\"
<div style="background: rgba(46, 134, 171, 0.1); border-left: 4px solid #2E86AB; border-radius: 4px; padding: 15px 20px; color: var(--text-color); margin-bottom: 2rem; font-weight: 500; font-size: 1.1rem; line-height: 1.5;">
                     <b>Welcome to MatDataHub!</b> Browse materials freely — sign in to unlock intelligent ESG tracking, bulk BOM analysis, and the AI Advisor.<br>
<span style="opacity: 0.85; font-size: 1rem; font-weight: 400;">The ultimate operating system for modern materials engineering.</span>
</div>
            \"\"\", unsafe_allow_html=True)

        # --- LIVE DATABASE STATS ---
        st.markdown("### 🌐 Platform Capabilities")
        s1, s2, s3, s4 = st.columns(4)
        for col, num, label in [
            (s1, "1,030+", "Verified Materials"),
            (s2, "AI", "Substitution Engine"),
            (s3, "ESG", "Carbon Footprint Tracking"),
            (s4, "Bulk", "BOM Parsing & Analysis"),
        ]:
            with col:
                st.markdown(f'<div class="cyber-stat"><div class="cyber-num">{num}</div><div class="cyber-label">{label}</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        # --- QUICK ACTIONS ---
        st.markdown("### ⚡ Quick Actions & Tools")
        qa1, qa2, qa3 = st.columns(3)
        with qa1:
            st.info("🔄 **Smart Substitution**\\n\\nMathematically find alternative supply chain materials based on cost, weight, and carbon footprint. Available in Analytics.")
        with qa2:
            st.success("📊 **Enterprise BOM Analyzer**\\n\\nUpload a CSV assembly to instantly verify ESG compliance and obsolete global standards. Available in Workflows.")
        with qa3:
            st.warning("🤖 **AI Metallurgist**\\n\\nDescribe your engineering constraints in natural language and get instantaneous material recommendations. Available in Explorer.")
        
        st.markdown("---")

"""
    content = content[:start_idx] + new_home + content[end_idx:]
    with open("frontend/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("tab_home replaced successfully!")
else:
    print("Could not find markers.")
