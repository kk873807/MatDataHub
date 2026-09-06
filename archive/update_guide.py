with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "    with tab_guide:"
end_marker = "    #  TAB: BROWSE MATERIALS" # Or whatever comes next... wait, the next tab is tab_browse_main!
end_marker = "    with tab_browse_main:"

if start_marker in content and end_marker in content:
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)
    
    # We will replace this entire block!
    new_guide_code = """    with tab_guide:
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
    
    content = content[:start_idx] + new_guide_code + content[end_idx:]
    
    with open("frontend/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("tab_guide replaced successfully!")
else:
    print("Could not find markers.")
