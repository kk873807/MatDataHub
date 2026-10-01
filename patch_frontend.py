import os

def replace_between(text, start_str, end_str, replacement):
    start_idx = text.find(start_str)
    if start_idx == -1: return text
    end_idx = text.find(end_str, start_idx)
    if end_idx == -1: return text
    end_idx += len(end_str)
    return text[:start_idx] + replacement + text[end_idx:]

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\analytics\cbam\page.tsx", "r", encoding="utf-8") as f:
    code = f.read()

# 1. State updates
old_state = """  const [fallbackTonnes, setFallbackTonnes] = useState(0);
  const [taxableTonnes, setTaxableTonnes] = useState(0);"""
new_state = """  const [fallbackTonnes, setFallbackTonnes] = useState(0);
  const [taxableTonnes, setTaxableTonnes] = useState(0);
  const [deMinimisThreshold, setDeMinimisThreshold] = useState(50);
  const [isDeMinimisExempt, setIsDeMinimisExempt] = useState(false);
  const [eligibleMassTonnes, setEligibleMassTonnes] = useState(0);"""
code = code.replace(old_state, new_state)

# 2. Parse Loop
old_parse = """        let total = 0; // Total physical kg included
        let totalCbamEur = 0;
        let revCount = 0;
        let revTonnes = 0;
        let fallbackKg = 0;
        let taxableKg = 0;
        
        parsedData.forEach((rowObj: any) => {
          const included = rowObj["Included_In_Total"];
          if (included && included.startsWith("YES")) {
            const rowKg = parseFloat(rowObj["Total_CO2_kg"] || "0");
            total += rowKg;
            const rowEur = parseFloat(rowObj["CBAM_Cost_EUR"] || "0");
            totalCbamEur += rowEur;
            
            if (rowObj["Emissions_Basis"] === "DEFAULT_FALLBACK") {
                fallbackKg += rowKg;
            }
          } else if (included && included.startsWith("NO")) {
            revCount += 1;
            if (rowObj["Provisional_CO2_kg"]) {
                revTonnes += parseFloat(rowObj["Provisional_CO2_kg"] || "0") / 1000.0;
            }
          }
        });
        
        // Reverse engineer taxable equivalent kg (Tax = Tonnes * €75)
        // 1 Tonne = €75. 1 Kg = €0.075.
        taxableKg = totalCbamEur / 0.075;

        setResultsData(parsedData);
        setTotalCO2(total);
        setTotalCbamCost(totalCbamEur);
        setPendingReviewCount(revCount);
        setPendingReviewTonnes(revTonnes);
        setFallbackTonnes(fallbackKg / 1000.0);
        setTaxableTonnes(taxableKg / 1000.0);"""

new_parse = """        let total = 0; // Total physical kg included
        let totalCbamEur = 0;
        let revCount = 0;
        let revTonnes = 0;
        let fallbackKg = 0;
        let taxableKg = 0;
        
        let eligibleMassKg = 0;
        let eligibleTaxEur = 0;
        let ineligibleTaxEur = 0;
        
        parsedData.forEach((rowObj: any) => {
          const included = rowObj["Included_In_Total"];
          if (included && included.startsWith("YES")) {
            const rowKg = parseFloat(rowObj["Total_CO2_kg"] || "0");
            total += rowKg;
            const rowEur = parseFloat(rowObj["CBAM_Cost_EUR"] || "0");
            totalCbamEur += rowEur;
            
            const elMass = parseFloat(rowObj["DeMinimis_Eligible_Mass_kg"] || "0");
            if (elMass > 0) {
              eligibleMassKg += elMass;
              eligibleTaxEur += rowEur;
            } else {
              ineligibleTaxEur += rowEur;
            }
            
            if (rowObj["Emissions_Basis"] === "DEFAULT_FALLBACK") {
                fallbackKg += rowKg;
            }
          } else if (included && included.startsWith("NO")) {
            revCount += 1;
            if (rowObj["Provisional_CO2_kg"]) {
                revTonnes += parseFloat(rowObj["Provisional_CO2_kg"] || "0") / 1000.0;
            }
          }
        });
        
        const elMassTonnes = eligibleMassKg / 1000.0;
        // Using the current state threshold is tricky in a closure if stale, but it's safe for simple recalculations. 
        // We will default to 50 if it's undefined.
        const isExempt = elMassTonnes <= 50 && elMassTonnes > 0;
        const activeTaxEur = isExempt ? ineligibleTaxEur : totalCbamEur;
        
        // Reverse engineer taxable equivalent kg (Tax = Tonnes * €75)
        taxableKg = activeTaxEur / 0.075;

        setResultsData(parsedData);
        setTotalCO2(total);
        setTotalCbamCost(activeTaxEur);
        setPendingReviewCount(revCount);
        setPendingReviewTonnes(revTonnes);
        setFallbackTonnes(fallbackKg / 1000.0);
        setTaxableTonnes(taxableKg / 1000.0);
        setIsDeMinimisExempt(isExempt);
        setEligibleMassTonnes(elMassTonnes);"""

code = code.replace(old_parse, new_parse)

# 3. UI logic
old_ui = """              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-2xl flex flex-col justify-center">
                <div className="flex justify-between items-start mb-1">
                  <p className="text-slate-500 dark:text-slate-400 font-medium flex items-center gap-2"><FileText className="w-4 h-4 text-amber-600 dark:text-amber-400" /> Est. CBAM Tax Payable</p>
                  <select 
                    value={selectedYear} 
                    onChange={e => setSelectedYear(e.target.value as any)}
                    className="text-xs bg-slate-100 dark:bg-slate-800 border-none rounded p-1 font-bold text-slate-700 dark:text-slate-300 outline-none cursor-pointer max-w-[160px]"
                  >
                    <option value="2034">If imported in 2034 (100%)</option>
                    <option value="2027">If imported in 2027 (~5%)</option>
                    <option value="2026">If imported in 2026 (~2.5%)</option>
                  </select>
                </div>
                <h3 className="text-3xl font-bold text-amber-500">€{estimatedTaxEUR.toLocaleString(undefined, { maximumFractionDigits: 2 })}</h3>
                <p className="text-xs text-slate-400 mt-2 font-medium">@ €75/tCO₂e · assumes emissions near benchmark</p>
              </div>"""

new_ui = """              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-2xl flex flex-col justify-center">
                <div className="flex justify-between items-start mb-1">
                  <p className="text-slate-500 dark:text-slate-400 font-medium flex items-center gap-2"><FileText className="w-4 h-4 text-amber-600 dark:text-amber-400" /> Est. CBAM Tax Payable</p>
                  <select 
                    value={selectedYear} 
                    onChange={e => setSelectedYear(e.target.value as any)}
                    className="text-xs bg-slate-100 dark:bg-slate-800 border-none rounded p-1 font-bold text-slate-700 dark:text-slate-300 outline-none cursor-pointer max-w-[160px]"
                  >
                    <option value="2034">If imported in 2034 (100%)</option>
                    <option value="2027">If imported in 2027 (~5%)</option>
                    <option value="2026">If imported in 2026 (~2.5%)</option>
                  </select>
                </div>
                {isDeMinimisExempt ? (
                  <div className="mt-2">
                    <h3 className="text-2xl font-bold text-emerald-500">Below threshold</h3>
                    <p className="text-xs text-slate-500 mt-1 font-medium bg-emerald-50 dark:bg-emerald-900/20 p-2 rounded">
                      Assuming this BOM is your whole annual import, the {eligibleMassTonnes.toLocaleString(undefined, { maximumFractionDigits: 1 })} t of eligible goods stay within the {deMinimisThreshold} t de minimis exemption. No obligation.
                    </p>
                  </div>
                ) : (
                  <>
                    <h3 className="text-3xl font-bold text-amber-500">€{estimatedTaxEUR.toLocaleString(undefined, { maximumFractionDigits: 2 })}</h3>
                    <p className="text-xs text-slate-400 mt-2 font-medium">@ €75/tCO₂e · assumes emissions near benchmark</p>
                  </>
                )}
              </div>"""

code = code.replace(old_ui, new_ui)

with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\analytics\cbam\page.tsx", "w", encoding="utf-8") as f:
    f.write(code)

print("Frontend patched.")
