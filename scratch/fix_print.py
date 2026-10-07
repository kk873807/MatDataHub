import sys
content = open('app/routers/materials.py', 'r', encoding='utf-8').read()

old = 'print(f"CSV read in {time.time()-t0:.2f}s, rows: {len(df)}, delimiter: \'{sep}\'", flush=True)'
new = 'print(f"Parsed {len(df)} rows. Delimiter: \'{sep}\'. Proceeding to calculate.", flush=True)'
if old in content:
    with open('app/routers/materials.py', 'w', encoding='utf-8') as f:
        f.write(content.replace(old, new))
    print('Replaced')
else:
    print('Not found')
