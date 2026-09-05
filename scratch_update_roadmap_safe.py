with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_steps = """
<div class="t-node">
<div class="t-card">
<span class="t-step" style="color: #FF9800;">Step 6 — Enterprise Scale</span>
<h4>Private Custom Materials Engine</h4>
<p>For engineering firms handling proprietary alloys, navigate to your <b>Account Dashboard</b> to access the <b>Custom Materials</b> engine. Upload secret material properties into an isolated database. These private materials automatically synchronize with your visual Comparison Engine and BOM Synthesizer (marked with a 🔒), allowing you safely compare proprietary alloys against public standards.</p>
</div>
</div>

<div class="t-node">
<div class="t-card">
<span class="t-step" style="color: #00BCD4;">Step 7 — Market Analytics</span>
<h4>Historical Commodity Price Tracking</h4>
<p>Supply chain economics are just as critical as yield strength. In the <b>Browse Materials</b> tab, scroll to the bottom of any standard material to access the 12-month <b>Historical Price Tracker</b>. Visualize market volatility and accurately project manufacturing costs.</p>
</div>
</div>
"""
lines.insert(1703, new_steps)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Updated Platform Roadmap HTML.")
