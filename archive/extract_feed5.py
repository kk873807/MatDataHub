import sys

with open("old_app.py", "r", encoding="utf-16") as f:
    content = f.read()

start = content.find('st.markdown("## Community Reviews & Discussion")')
end = content.find('    with tab_guide:', start)
if end == -1: # Wait, tab_guide comes BEFORE this in old_app.py!
    end = content.find('    # ══════════════════════════════════════════════\n    #  TAB: BROWSE MATERIALS', start)
    if end == -1:
        end = content.find('    with tab_browse:', start)

if start != -1:
    text = content[start-40:end]
    # write to a new file safely
    with open("community_feed_extracted.py", "w", encoding="utf-8") as out:
        out.write(text)
    print("Extracted to community_feed_extracted.py")
else:
    print("NOT FOUND IN old_app.py")
