with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# We need to extract the CSS from tab_home and move it up.
start_marker = "# --- THEME-AWARE CSS ---"
end_marker = '        """, unsafe_allow_html=True)'

if start_marker in content:
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx) + len(end_marker)
    
    css_block = content[start_idx:end_idx]
    
    # Remove from original location
    content = content[:start_idx] + content[end_idx:]
    
    # Insert right after: if st.session_state.current_page == "main":
    insert_target = 'if st.session_state.current_page == "main":\n'
    insert_idx = content.find(insert_target) + len(insert_target)
    
    # Need to fix indentation for the global scope (4 spaces instead of 8)
    unindented_css = css_block.replace("\n        ", "\n    ")
    
    content = content[:insert_idx] + "    " + unindented_css + "\n" + content[insert_idx:]
    
    with open("frontend/app.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("CSS hoisted to global scope!")
else:
    print("CSS block not found.")
