import re

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# The exact old tabs definition
old_tabs = """    tab_home, tab_guide, tab_browse, tab_compare, tab_projects, tab_ai, tab_faq, tab_feedback, tab_substitute, tab_enterprise = st.tabs([
        "🏠 Home", "📖 Platform Guide", "🔍 Browse Materials", "⚖️ Compare", "⚙️ Engineering (BOM)", "🤖 AI Advisor", "❓ FAQ", "🎫 Help & Contact", "🔄 Smart Substitute (PRO)", "📊 Enterprise BOM (ADV)"
    ])"""

# The new hierarchical tabs definition
new_tabs = """    # Massive UI/UX IA Refactor: Grouping 10 tabs into 5 logical Workspaces
    tab_home_main, tab_browse, tab_analytics, tab_workflows, tab_support = st.tabs([
        "🏠 Dashboard", "🔍 Explorer", "⚖️ Analytics", "⚙️ Workflows", "💬 Support Center"
    ])
    
    with tab_home_main:
        tab_home, tab_guide = st.tabs(["🏠 Overview", "📖 Quick Start Guide"])
        
    with tab_analytics:
        tab_compare, tab_substitute = st.tabs(["⚖️ Side-by-Side Compare", "🔄 Smart AI Substitution (PRO)"])
        
    with tab_workflows:
        tab_projects, tab_enterprise = st.tabs(["⚙️ Standard BOM Builder", "📊 Enterprise ESG Analyzer (ADV)"])
        
    with tab_support:
        tab_ai, tab_faq, tab_feedback = st.tabs(["🤖 AI Advisor", "❓ FAQ", "🎫 Submit Support Ticket"])"""

content = content.replace(old_tabs, new_tabs)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("UI IA Refactored successfully!")
