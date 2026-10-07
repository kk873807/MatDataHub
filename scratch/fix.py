import sys, re
content = open('next-frontend/src/app/analytics/cbam/page.tsx', 'r', encoding='utf-8').read()
new_part = """                  {interimStats.rows > 0 && (
                    <p className="text-slate-500 dark:text-slate-400">
                      Using official Commission defaults for {interimStats.rows} covered row{interimStats.rows === 1 ? "" : "s"}
                      ({interimStats.heading} matched at heading level, {interimStats.global} using global fallback).
                    </p>
                  )}"""
pattern = r'                  \{interimStats\.rows > 0 && \([\s\S]*?                  \)\}'
new_content = re.sub(pattern, new_part, content)
with open('next-frontend/src/app/analytics/cbam/page.tsx', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Replaced')
