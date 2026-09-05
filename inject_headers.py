import re

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# We want to replace the current tab_home_main logic with enhanced immersive headers

old_logic = """    with tab_home_main:
        tab_home, tab_guide = st.tabs(["🏠 Overview", "📖 Quick Start Guide"])
        
    with tab_analytics:
        tab_compare, tab_substitute = st.tabs(["⚖️ Side-by-Side Compare", "🔄 Smart AI Substitution (PRO)"])
        
    with tab_workflows:
        tab_projects, tab_enterprise = st.tabs(["⚙️ Standard BOM Builder", "📊 Enterprise ESG Analyzer (ADV)"])
        
    with tab_support:
        tab_ai, tab_faq, tab_feedback = st.tabs(["🤖 AI Advisor", "❓ FAQ", "🎫 Submit Support Ticket"])"""

new_logic = """    with tab_home_main:
        st.markdown("## 🏠 Command Center")
        st.caption("Welcome to your MatDataHub operations dashboard. Access materials, engineering insights, and enterprise tools from one unified platform.")
        st.divider()
        tab_home, tab_guide = st.tabs(["🏠 Overview", "📖 Quick Start Guide"])
        
    with tab_analytics:
        st.markdown("## ⚖️ Advanced Analytics & AI Substitution")
        st.caption("Compare materials side-by-side or use our proprietary AI to mathematically calculate the perfect supply chain substitute.")
        st.divider()
        tab_compare, tab_substitute = st.tabs(["⚖️ Side-by-Side Compare", "🔄 Smart AI Substitution (PRO)"])
        
    with tab_workflows:
        st.markdown("## ⚙️ Engineering & Enterprise Workflows")
        st.caption("Build custom project assemblies, calculate weights, and utilize our AI-powered ESG (Environmental, Social, & Governance) compliance engine.")
        st.divider()
        tab_projects, tab_enterprise = st.tabs(["⚙️ Standard BOM Builder", "📊 Enterprise ESG Analyzer (ADV)"])
        
    with tab_support:
        st.markdown("## 💬 Support & Intelligence Center")
        st.caption("Get instantaneous AI-driven metallurgical advice or reach out to our dedicated enterprise support team.")
        st.divider()
        tab_ai, tab_faq, tab_feedback = st.tabs(["🤖 AI Advisor", "❓ FAQ", "🎫 Submit Support Ticket"])"""

content = content.replace(old_logic, new_logic)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Enhanced Workspace Headers injected!")
