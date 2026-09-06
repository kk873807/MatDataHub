import sys

file_path = 'app/routers/feedback.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
content = re.sub(r'from fastapi import (.*?)\n', r'from fastapi import \1, BackgroundTasks\n', content, count=1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added BackgroundTasks import.")
