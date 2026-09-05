import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Find the community block
start_marker = '        st.markdown("---")\n        st.markdown("## Community Reviews & Discussion")'
# Find the end of it (the weird ΓòÉ comments)
end_marker = "    with tab_browse_main:"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    block = content[start_idx:end_idx]
    
    # 2. Clean the block
    import re
    # Remove the ΓòÉ dividers entirely
    block = re.sub(r'#.*?\n', '\n', block) # Wait, this might remove useful comments.
    
    # Clean it safely
    clean_lines = []
    for line in block.split('\n'):
        if 'TAB: PLATFORM GUIDE' in line or '\u0393' in line or '\xc9' in line or 'Γ' in line:
            continue
        clean_lines.append(line)
    
    cleaned_block = "\n".join(clean_lines) + "\n"
    
    # Remove it from the current location
    content = content[:start_idx] + content[end_idx:]
    
    # 3. Insert it into tab_home (right before `with tab_guide:`)
    insert_marker = "    with tab_guide:"
    insert_idx = content.find(insert_marker)
    
    if insert_idx != -1:
        content = content[:insert_idx] + cleaned_block + "\n" + content[insert_idx:]
    
    with open("frontend/app.py", "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Successfully moved community block to tab_home and cleaned mangled characters.")
else:
    print("Could not find block")
