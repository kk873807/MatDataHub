import os

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\analytics\cbam\page.tsx", "r", encoding="utf-8") as f:
    code = f.read()

# 1. State updates
old_state = """  const [totalCbamCost, setTotalCbamCost] = useState(0);
  const [selectedYear, setSelectedYear] = useState<"2034" | "2027" | "2026">("2034");"""
new_state = """  const [totalCbamCost, setTotalCbamCost] = useState(0);
  const [selectedYear, setSelectedYear] = useState<"2034" | "2027" | "2026">("2034");
  const [pendingReviewCount, setPendingReviewCount] = useState(0);
  const [pendingReviewTonnes, setPendingReviewTonnes] = useState(0);"""
code = code.replace(old_state, new_state)

# 2. processBOM parse loop
old_parse = """        let total = 0;
        let totalCbamEur = 0;
        parsedData.forEach((rowObj: any) => {
          // Only sum rows that don't have validation errors (or only 'None')
          // Wait, the backend already zeroes out critical errors, but the user wants to exclude ALL rows with ANY error from the top-level total for safety!
          const errors = rowObj["Validation_Errors"];
          const hasErrors = errors && errors !== "None";
          
          if (!hasErrors) {
            if (rowObj["Total_CO2_kg"]) total += parseFloat(rowObj["Total_CO2_kg"] || "0");
            if (rowObj["CBAM_Cost_EUR"]) totalCbamEur += parseFloat(rowObj["CBAM_Cost_EUR"] || "0");
          }
        });

        setResultsData(parsedData);
        setTotalCO2(total);
        setTotalCbamCost(totalCbamEur);"""

new_parse = """        let total = 0;
        let totalCbamEur = 0;
        let revCount = 0;
        let revTonnes = 0;
        
        parsedData.forEach((rowObj: any) => {
          const included = rowObj["Included_In_Total"];
          if (included && included.startsWith("YES")) {
            if (rowObj["Total_CO2_kg"]) total += parseFloat(rowObj["Total_CO2_kg"] || "0");
            if (rowObj["CBAM_Cost_EUR"]) totalCbamEur += parseFloat(rowObj["CBAM_Cost_EUR"] || "0");
          } else if (included && included.startsWith("NO")) {
            revCount += 1;
            if (rowObj["Total_CO2_kg"]) revTonnes += parseFloat(rowObj["Total_CO2_kg"] || "0") / 1000.0;
          }
        });

        setResultsData(parsedData);
        setTotalCO2(total);
        setTotalCbamCost(totalCbamEur);
        setPendingReviewCount(revCount);
        setPendingReviewTonnes(revTonnes);"""
code = code.replace(old_parse, new_parse)

# 3. UI totalCO2 card
old_co2_card = """              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-2xl flex flex-col justify-center">
                <p className="text-slate-500 dark:text-slate-400 font-medium mb-1 flex items-center gap-2"><Factory className="w-4 h-4 text-emerald-600 dark:text-emerald-400" /> Total Embodied Carbon</p>
                <h3 className="text-3xl font-bold text-slate-900 dark:text-white font-heading">{totalCO2.toLocaleString(undefined, { maximumFractionDigits: 2 })} <span className="text-lg text-slate-500 dark:text-slate-400 font-normal">kg CO₂</span></h3>
              </div>"""

new_co2_card = """              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-2xl flex flex-col justify-center">
                <p className="text-slate-500 dark:text-slate-400 font-medium mb-1 flex items-center gap-2"><Factory className="w-4 h-4 text-emerald-600 dark:text-emerald-400" /> Total Embodied Carbon</p>
                <h3 className="text-3xl font-bold text-slate-900 dark:text-white font-heading">{totalCO2.toLocaleString(undefined, { maximumFractionDigits: 2 })} <span className="text-lg text-slate-500 dark:text-slate-400 font-normal">kg CO₂</span></h3>
                {pendingReviewCount > 0 && (
                  <p className="text-xs text-slate-400 mt-2 font-medium">
                    {(totalCO2 / 1000).toLocaleString(undefined, { maximumFractionDigits: 0 })} t included · {pendingReviewTonnes.toLocaleString(undefined, { maximumFractionDigits: 0 })} t in {pendingReviewCount} rows pending review
                  </p>
                )}
              </div>"""
code = code.replace(old_co2_card, new_co2_card)

# 4. UI select options
old_select = """                  <select 
                    value={selectedYear} 
                    onChange={e => setSelectedYear(e.target.value as any)}
                    className="text-xs bg-slate-100 dark:bg-slate-800 border-none rounded p-1 font-bold text-slate-700 dark:text-slate-300 outline-none cursor-pointer"
                  >
                    <option value="2034">2034 (100% Gross Exposure)</option>
                    <option value="2027">2027 (5% Phase-in)</option>
                    <option value="2026">2026 (2.5% Phase-in)</option>
                  </select>"""
                  
new_select = """                  <select 
                    value={selectedYear} 
                    onChange={e => setSelectedYear(e.target.value as any)}
                    className="text-xs bg-slate-100 dark:bg-slate-800 border-none rounded p-1 font-bold text-slate-700 dark:text-slate-300 outline-none cursor-pointer max-w-[200px]"
                  >
                    <option value="2034">2034 (100% Gross Exposure)</option>
                    <option value="2027">2027 (Est. ~5% effective, near benchmark)</option>
                    <option value="2026">2026 (Est. ~2.5% effective, near benchmark)</option>
                  </select>"""
code = code.replace(old_select, new_select)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\analytics\cbam\page.tsx", "w", encoding="utf-8") as f:
    f.write(code)

print("page.tsx patched successfully.")
