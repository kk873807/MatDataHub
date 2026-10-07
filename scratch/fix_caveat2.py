import sys
content = open('app/workflows.py', 'r', encoding='utf-8').read()
old_note = 'notes.append(f"Cost adjusted by {phase_in*100:.1f}% free allocation phase-out for {lookup_year}")'
new_note = 'notes.append(f"Cost estimated as {phase_in*100:.1f}% of emissions (CAVEAT: assumes emissions ≈ benchmark. Actual cost will be higher if using defaults)")'
if old_note in content:
    with open('app/workflows.py', 'w', encoding='utf-8') as f:
        f.write(content.replace(old_note, new_note))
    print('Replaced backend note')
else:
    print('Backend note not found')
