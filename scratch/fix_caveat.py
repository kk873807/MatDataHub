import sys
content = open('next-frontend/src/app/analytics/cbam/page.tsx', 'r', encoding='utf-8').read()
old_str = '<p className="text-xs text-slate-400 mt-2 font-medium">@ €75/tCO₂e (assumed — actual CBAM certificate price is a published quarterly EEX average)</p>'
new_str = '''<p className="text-xs text-slate-400 mt-2 font-medium">@ €75/tCO₂e (assumed — actual CBAM certificate price is a published quarterly EEX average)</p>
                  <p className="text-xs text-amber-500 mt-1 font-semibold text-balance">
                    ⚠️ Warning: The phase-in model assumes product emissions equal the free-allocation benchmark. Because default values exceed benchmarks, actual 2026-2027 costs using defaults will be substantially higher.
                  </p>'''
if old_str in content:
    with open('next-frontend/src/app/analytics/cbam/page.tsx', 'w', encoding='utf-8') as f:
        f.write(content.replace(old_str, new_str))
    print('Replaced frontend text')
else:
    print('Frontend text not found')

content2 = open('app/workflows.py', 'r', encoding='utf-8').read()
old_note = 'notes.append(f"Cost adjusted by {phase_in_pct*100}% free allocation phase-out for {shipment_year}")'
new_note = 'notes.append(f"Cost estimated as {phase_in_pct*100}% of emissions (CAVEAT: assumes emissions ≈ benchmark. Actual cost will be higher if using defaults)")'
if old_note in content2:
    with open('app/workflows.py', 'w', encoding='utf-8') as f:
        f.write(content2.replace(old_note, new_note))
    print('Replaced backend note')
else:
    print('Backend note not found')
