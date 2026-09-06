import sys

file_path = 'app/routers/feedback.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_loop = """    for f in fb:
        f.email = None
    return fb"""

new_loop = """    for f in fb:
        f.email = None
        f.image_data = None  # CRITICAL: Prevent giant base64 images from crashing the public feed
    return fb"""

content = content.replace(old_loop, new_loop)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Stripped base64 images from public feedback endpoint.")
