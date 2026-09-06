import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker_home = "    with tab_home:"
end_marker_home = "    with tab_guide:"
start_marker_guide = "    with tab_guide:"
end_marker_guide = "    #  TAB: BROWSE MATERIALS" # Wait, let's just use with tab_browse:
end_marker_guide_alt = "    with tab_browse:"

# Find precise indices
idx_home = content.find(start_marker_home)
idx_guide = content.find(start_marker_guide, idx_home)
idx_browse = content.find(end_marker_guide_alt, idx_guide)

if idx_home == -1 or idx_guide == -1 or idx_browse == -1:
    print("FAILED TO FIND INDICES")
    sys.exit(1)

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

new_guide = """    with tab_guide:
        st.markdown("### 📖 Interactive Platform Guide")
        st.caption("Select a workflow below to learn how to maximize your MatDataHub experience.")
        
        # Interactive Navigation
        guide_step = st.radio("Select Workflow:", [
            "🔍 Discover & Browse", 
            "⚖️ Analyze & Substitute", 
            "📊 Enterprise ESG & BOM", 
            "🤖 AI Metallurgist"
        ], horizontal=True, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if guide_step == "🔍 Discover & Browse":
            col1, col2 = st.columns([1, 1.5])
            with col1:
                st.markdown("#### 1. Navigate to Explorer")
                st.write("Use the **Explorer** tab to access the full global database of over 1,000+ verified engineering materials.")
                st.write("Filter by Category (Metals, Polymers, Ceramics) or search specific ASTM/ISO standards.")
            with col2:
                st.info("💡 **Pro Tip:** Free users can view basic mechanical and thermal properties. Upgrade to Pro to view pricing histories and advanced ESG data.")
                
        elif guide_step == "⚖️ Analyze & Substitute":
            col1, col2 = st.columns([1, 1.5])
            with col1:
                st.markdown("#### 2. The Smart Substitution Engine")
                st.write("Supply chain disruptions? Cost-cutting mandates? Use the **Analytics -> Smart Substitution** engine.")
                st.write("Select your base material (e.g., AISI 304) and use the sliders to prioritize Cost, Weight, Strength, and Carbon Footprint.")
            with col2:
                st.success("✅ **Mathematical Optimization:** The AI normalizes the database and generates interactive Radar Charts proving exactly why an alternative material is superior.")
                
        elif guide_step == "📊 Enterprise ESG & BOM":
            col1, col2 = st.columns([1, 1.5])
            with col1:
                st.markdown("#### 3. Automated BOM Enrichment")
                st.write("Procurement teams can upload messy Excel/CSV Bills of Materials directly into the **Workflows** tab.")
                st.write("Our fuzzy-matching AI cleans the data, finds the exact materials, and flags obsolete global standards.")
            with col2:
                st.warning("🌍 **ESG Compliance:** The system automatically calculates the Total Embodied Carbon (kg CO2e) for your entire project, generating instant sustainability reports.")
                
        elif guide_step == "🤖 AI Metallurgist":
            col1, col2 = st.columns([1, 1.5])
            with col1:
                st.markdown("#### 4. Natural Language Engineering")
                st.write("Skip the manual filters. Chat directly with our **AI Advisor** located in the Explorer tab.")
                st.write("Example: *'I need a lightweight alloy for an aerospace drone bracket that operates at 150°C and costs less than $15/kg.'*")
            with col2:
                st.error("🤖 **Context-Aware:** The AI is natively hooked into our verified database, meaning it doesn't hallucinate—it strictly recommends actual, purchasable materials.")

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("---")

"""

# Reassemble
content = content[:idx_home] + new_home + new_guide + content[idx_browse:]

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Safely replaced Home and Guide tabs!")
