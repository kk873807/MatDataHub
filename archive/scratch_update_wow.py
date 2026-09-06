with open("frontend/app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
    
# 1. Update Platform Mastery Roadmap HTML
step3_idx = -1
for i, line in enumerate(lines):
    if "Simulation & Economics" in line:
        step3_idx = i
        break

if step3_idx != -1:
    end_idx = -1
    for j in range(step3_idx, len(lines)):
        if "</div> <!-- wrapper -->" in lines[j]:
            end_idx = j
            break
    
    if end_idx != -1:
        new_roadmap_steps = """
<div class="t-node">
<div class="t-card">
<span class="t-step">Step 4 — Enterprise Scale (Advanced Tier)</span>
<h4>Private Custom Materials Engine</h4>
<p>For engineering firms handling proprietary alloys, navigate to your <b>Account Dashboard</b> to access the <b>Custom Materials</b> engine. Upload secret material properties into an isolated database. These private materials automatically synchronize with your visual Comparison Engine and BOM Synthesizer (marked with a 🔒), allowing you to safely compare your proprietary alloys against public ASTM standards.</p>
</div>
</div>

<div class="t-node">
<div class="t-card">
<span class="t-step">Step 5 — Market Analytics</span>
<h4>Historical Commodity Price Tracking</h4>
<p>Supply chain economics are just as critical as yield strength. In the <b>Browse Materials</b> tab, scroll to the bottom of any standard material to access the 12-month <b>Historical Price Tracker</b> (Pro/Advanced Tier). Visualize market volatility and accurately project manufacturing costs.</p>
</div>
</div>
"""
        lines.insert(end_idx, new_roadmap_steps)
        print("Injected Step 4 and 5 into Roadmap.")

# 2. Inject Custom Materials into Compare tool
for i, line in enumerate(lines):
    if 'name_to_id = {m["name"]: m["id"] for m in all_materials}' in line:
        injection = """
        user_tier = (st.session_state.user or {}).get("tier", "free")
        if user_tier == "advanced":
            cust_mats = api_get("/materials/custom/mine")
            if cust_mats["ok"] and cust_mats["data"]:
                for cm in cust_mats["data"]:
                    all_materials.append(cm)
                    name_to_id[f"🔒 {cm['name']}"] = -cm["id"]
"""
        lines.insert(i+1, injection)
        print("Injected custom materials into Comparison dropdown.")
        break

# 3. Intercept negative IDs in Comparison submit
for i, line in enumerate(lines):
    if 'ids = [name_to_id[name] for name in selections]' in line:
        injection = """
            standard_ids = [i for i in ids if i > 0]
            custom_ids = [-i for i in ids if i < 0]
            
            with st.spinner("Loading comparison..."):
                compare_result = api_get("/materials/compare", params={"ids": standard_ids}) if standard_ids else {"ok": True, "data": []}
                
                # Wow Feature: Merge private materials perfectly into the public API response!
                if custom_ids and compare_result["ok"]:
                    cust_mats = api_get("/materials/custom/mine")
                    if cust_mats["ok"] and cust_mats["data"]:
                        for cm in cust_mats["data"]:
                            if cm["id"] in custom_ids:
                                cm["name"] = f"🔒 {cm['name']}"
                                compare_result["data"].append(cm)
"""
        # We need to replace the api_get call
        # Find where api_get("/materials/compare") is
        for j in range(i, i+10):
            if 'compare_result = api_get("/materials/compare"' in lines[j]:
                lines[j] = "                pass # Replaced by custom merge logic below\n"
        
        lines.insert(i+1, injection)
        print("Injected Custom Material API interceptor.")
        break

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Done.")
