import sys

with open("community_feed_extracted.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(10):
    print(repr(lines[i]))
