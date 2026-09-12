import os

with open('requirements.txt', 'r', encoding='utf-8') as f:
    reqs = f.read()

# Fix the pip backtracking by pinning google-api-core
if 'google-api-core==2.23.0' not in reqs:
    reqs = reqs.replace('google-generativeai', 'google-generativeai\ngoogle-api-core==2.23.0')
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(reqs)

# Remove the slow migrations from main.py so it boots up instantly
with open('app/main.py', 'r', encoding='utf-8') as f:
    main_code = f.read()

import re
# Regex to remove the 'Quick and dirty auto-migration for MVP' block
main_code = re.sub(r'# Quick and dirty auto-migration for MVP.*?app = FastAPI\(', 'app = FastAPI(', main_code, flags=re.DOTALL)

with open('app/main.py', 'w', encoding='utf-8') as f:
    f.write(main_code)

print("Fixed backend requirements and main.py startup")
