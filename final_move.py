import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the start of the community block
start_idx = -1
for i, line in enumerate(lines):
    if "st.markdown(\"## Community Reviews & Discussion\")" in line:
        # Start from the '---' divider above it
        start_idx = i - 1 
        break

# Find the end of the community block
end_idx = -1
for i in range(start_idx, len(lines)):
    if "with tab_browse_main:" in lines[i]:
        end_idx = i - 2 # Leaves some blank space
        break

if start_idx == -1 or end_idx == -1:
    print("Could not find start/end")
    sys.exit(1)

# Extract and clean
block_lines = lines[start_idx:end_idx]
clean_block = []
for line in block_lines:
    line = line.replace("\u0393\xa1\xc9", "⭐")
    line = line.replace("\u2261\u0192\xe6\xec", "👍")
    line = line.replace("\u2261\u0192\xc6\xbc", "💬")
    line = line.replace("\u2261\u0192\xa2\xe1\u2229\u2555\xc5", "🛡️")
    line = line.replace("\u0393\xf2\xc9", "")
    line = line.replace("I\"AA%", "⭐")
    clean_block.append(line)

# Remove the block from its current location
new_lines = lines[:start_idx] + lines[end_idx:]

# Find `with tab_guide:` in the new list to insert BEFORE it
insert_idx = -1
for i, line in enumerate(new_lines):
    if "with tab_guide:" in line:
        insert_idx = i
        break

if insert_idx != -1:
    # Insert the block
    final_lines = new_lines[:insert_idx] + ["\n"] + clean_block + ["\n"] + new_lines[insert_idx:]
    
    with open("frontend/app.py", "w", encoding="utf-8") as f:
        f.writelines(final_lines)
    print("Community block moved and cleaned successfully!")
else:
    print("Could not find tab_guide")
