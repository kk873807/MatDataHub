import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old_tabs = """    tab_home_main, tab_browse_main, tab_analytics, tab_workflows, tab_support_main, tab_faq_main = st.tabs([
        "\U0001f3e0 Dashboard", "\U0001f50d Explorer", "\u2696\ufe0f Analytics", "\u2699\ufe0f Workflows", "\U0001f4ac Support Center", "\u2753 FAQ"
    ])"""

new_tabs = """    tab_home_main, tab_browse_main, tab_analytics, tab_workflows, tab_support_main, tab_faq_main, tab_blog_main = st.tabs([
        "\U0001f3e0 Dashboard", "\U0001f50d Explorer", "\u2696\ufe0f Analytics", "\u2699\ufe0f Workflows", "\U0001f4ac Support Center", "\u2753 FAQ", "\U0001f4f0 Engineering Blog"
    ])"""

if old_tabs in content:
    content = content.replace(old_tabs, new_tabs)
    with open("frontend/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Tabs updated.")
else:
    print("Could not find tabs declaration.")
