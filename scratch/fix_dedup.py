import sys
content = open('app/workflows.py', 'r', encoding='utf-8').read()

old = 'quarantine_reasons.append(f"Strict Mode: {err}")'
new = '''if f"Strict Mode: {err}" not in quarantine_reasons:
                            quarantine_reasons.append(f"Strict Mode: {err}")'''
content = content.replace(old, new)

# Let's deduplicate later where errors is converted to a string or at the end of row loop.
# Before:
#             if quarantine_reasons:
#                 included_str = "QUARANTINED: " + " | ".join(quarantine_reasons)
# Let's change it to:
#             if quarantine_reasons:
#                 # deduplicate order preserving
#                 quarantine_reasons = list(dict.fromkeys(quarantine_reasons))
#                 errors = list(dict.fromkeys(errors))
#                 included_str = "QUARANTINED: " + " | ".join(quarantine_reasons)

old_end = 'if quarantine_reasons:'
new_end = '''if quarantine_reasons:
                quarantine_reasons = list(dict.fromkeys(quarantine_reasons))
                errors = list(dict.fromkeys(errors))'''
content = content.replace(old_end, new_end)

with open('app/workflows.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Deduplicated')
