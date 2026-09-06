import sys
import re

file_path = 'app/routers/materials.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix list_materials docstring bug and add rate limits
old_list = '    ):\n        """\n        _check_mat_rate_limit(request)\n        List materials'
new_list = '    ):\n        _check_mat_rate_limit(request)\n        _check_daily_limit(request, current_user)\n        """\n        List materials'

if old_list in content:
    content = content.replace(old_list, new_list)
else:
    # maybe spacing is different
    old_list2 = '    ):\n        """\n        _check_mat_rate_limit(request)\n'
    if old_list2 in content:
        print("Found old list 2")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated list_materials.")
