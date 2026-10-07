import sys
content = open('app/workflows.py', 'r', encoding='utf-8').read()

old1 = '"Matched_Material": matched_name if is_match else ("N/A (default factor used)" if default_meta else "NO MATCH FOUND"),'
old2 = '"Match_Confidence": f"{confidence}%" if is_match else ("N/A" if default_meta else "0%"),'

new1 = '"Matched_Material": "N/A (CBAM Default applied)" if default_meta else (matched_name if is_match else "NO MATCH FOUND"),'
new2 = '"Match_Confidence": "N/A" if default_meta else (f"{confidence}%" if is_match else "0%"),'

if old1 in content and old2 in content:
    with open('app/workflows.py', 'w', encoding='utf-8') as f:
        f.write(content.replace(old1, new1).replace(old2, new2))
    print('Replaced Matched_Material logic')
else:
    print('Not found')
