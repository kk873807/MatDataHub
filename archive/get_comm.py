import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "    with tab_community:"
end_marker = "    with tab_feedback:"

if start_marker in content and end_marker in content:
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)
    
    community_block = content[start_idx:end_idx]
    print(community_block.encode('ascii', 'backslashreplace').decode()[:500])
else:
    print("Markers not found")
