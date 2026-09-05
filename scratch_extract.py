with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
with open("out1.txt", "w", encoding="utf-8") as f:
    f.writelines(lines[950:980])
with open("out2.txt", "w", encoding="utf-8") as f:
    f.writelines(lines[1050:1100])
with open("out3.txt", "w", encoding="utf-8") as f:
    f.writelines(lines[1880:1940])
