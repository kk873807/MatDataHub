import sys

with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

delete_indices = set()

# tab_browse
for i in range(1669, 1675): delete_indices.add(i)

# tab_compare
delete_indices.add(1913)

# tab_projects
for i in range(2153, 2159): delete_indices.add(i)

# tab_ai
delete_indices.add(2849)

# tab_faq_main
delete_indices.add(2902)
delete_indices.add(2903)

# tab_support_main
delete_indices.add(2935)
delete_indices.add(2936)

# tab_substitute
delete_indices.add(3002)
delete_indices.add(3003)

# tab_enterprise
delete_indices.add(3104)
delete_indices.add(3105)

new_lines = []
for i, line in enumerate(lines):
    if i not in delete_indices:
        new_lines.append(line)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"Removed {len(delete_indices)} lines of duplicate/unnecessary headings!")
