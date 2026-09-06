import sys

file_path = 'frontend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    if "Request Upgrade to Pro" in line:
        print("Pro line bytes:", line.strip().encode('utf-8'))
    if "Request Upgrade to Advanced" in line:
        print("Adv line bytes:", line.strip().encode('utf-8'))
