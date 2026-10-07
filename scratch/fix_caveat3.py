import sys
content = open('next-frontend/src/app/analytics/cbam/page.tsx', 'r', encoding='utf-8').read()

old_caveat = "⚠️ Warning: The phase-in model assumes product emissions equal the free-allocation benchmark. Because default values exceed benchmarks, actual 2026-2027 costs using defaults will be substantially higher."
new_caveat = "⚠️ Warning (simplified lower estimate): The phase-in model assumes product emissions equal the free-allocation benchmark. Because default values typically exceed benchmarks, actual 2026-2027 costs using defaults will likely be substantially higher."

if old_caveat in content:
    with open('next-frontend/src/app/analytics/cbam/page.tsx', 'w', encoding='utf-8') as f:
        f.write(content.replace(old_caveat, new_caveat))
    print('Replaced caveat in UI')
else:
    print('UI caveat not found')

content2 = open('app/workflows.py', 'r', encoding='utf-8').read()
old_note = 'Cost estimated as {phase_in*100:.1f}% of emissions (CAVEAT: assumes emissions ≈ benchmark. Actual cost will be higher if using defaults)'
new_note = 'Cost estimated as {phase_in*100:.1f}% of emissions (Simplified lower estimate: assumes emissions ≈ benchmark. Actual cost will be higher if using defaults)'
if old_note in content2:
    with open('app/workflows.py', 'w', encoding='utf-8') as f:
        f.write(content2.replace(old_note, new_note))
    print('Replaced caveat in backend notes')
else:
    print('Backend note not found')
