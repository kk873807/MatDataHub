import sys

with open("app/main.py", "r", encoding="utf-8") as f:
    content = f.read()

import_old = "from app.routers import materials, auth, admin, feedback, payments, ai, projects, account"
import_new = "from app.routers import materials, auth, admin, feedback, payments, ai, projects, account, calculators"

mount_old = "app.include_router(account.router, prefix=\"/api/v1\")       # <-- added payments"
mount_new = """app.include_router(account.router, prefix=\"/api/v1\")       # <-- added payments
app.include_router(calculators.router, prefix=\"/api/v1\")"""

if import_old in content and mount_old in content:
    content = content.replace(import_old, import_new)
    content = content.replace(mount_old, mount_new)
    with open("app/main.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Mounted calculators router in main.py")
else:
    print("Could not find the target lines to replace.")
