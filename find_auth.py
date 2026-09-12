import os

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\account\page.tsx'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

import re

# We will replace everything from `if (!profile) return (` up to the ending `);` of that block.
# Let's find the exact block.
start_str = "if (!profile) return ("
end_str = "              </button>\n            </div>\n          </div>"

if start_str in text and end_str in text:
    print("Found block")
else:
    print("Not found")

