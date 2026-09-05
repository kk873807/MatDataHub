import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_css = """                        .compact-admin {
                            background-color: #1c2a38;
                            border: 1px solid #4DA8DA;
                            border-radius: 5px;
                            padding: 8px;
                            margin-top: 5px;
                            font-size: 0.8em;
                        }"""

new_css = """                        .compact-admin {
                            background-color: var(--secondary-background-color);
                            border: 1px solid var(--faded-text-20);
                            border-left: 3px solid #00f0ff;
                            border-radius: 5px;
                            padding: 10px;
                            margin-top: 10px;
                            font-size: 0.85em;
                            color: var(--text-color);
                        }"""

if old_css in content:
    content = content.replace(old_css, new_css)
    # Also fix the verified admin response header color
    old_admin_header = '<strong style="color:#00ffcc">✅ Verified Admin Response:</strong><br/>'
    new_admin_header = '<strong style="color: #00f0ff;">✅ Verified Admin Response:</strong><br/>'
    content = content.replace(old_admin_header, new_admin_header)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("CSS updated for light mode compatibility.")
else:
    print("Could not find old CSS block.")
