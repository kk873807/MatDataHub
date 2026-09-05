import sys

with open("app/routers/projects.py", "r") as f:
    content = f.read()

# Remove the auth dependency
content = content.replace("current_user: User = Depends(get_current_user)", "current_user_id: int = 1")
content = content.replace("current_user.tier == \"free\"", "False")
content = content.replace("current_user.tier == \"pro\"", "False")
content = content.replace("current_user.id", "current_user_id")

with open("app/routers/projects.py", "w") as f:
    f.write(content)

