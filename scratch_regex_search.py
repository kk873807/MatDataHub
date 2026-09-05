import sys
import re

file_path = 'app/routers/materials.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add _check_daily_limit to search_materials
content = re.sub(
    r'def search_materials\((.*?)\):\n\s+"""',
    r'def search_materials(\1):\n    _check_daily_limit(request, current_user)\n    """',
    content,
    flags=re.DOTALL
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated search_materials.")
