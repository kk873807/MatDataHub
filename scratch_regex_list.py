import sys
import re

file_path = 'app/routers/materials.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to extract the docstring and replace it correctly
# Find: def list_materials(.*?):.*?_check_mat_rate_limit\(request\)
content = re.sub(
    r'def list_materials\((.*?)\):\n\s+"""\n\s+_check_mat_rate_limit\(request\)',
    r'def list_materials(\1):\n    _check_mat_rate_limit(request)\n    _check_daily_limit(request, current_user)\n    """',
    content,
    flags=re.DOTALL
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Regex replace list_materials.")
