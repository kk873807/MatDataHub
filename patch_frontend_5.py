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

# 1. Simplify activeTaxEur calculation
old_calc = """        const elMassTonnes = eligibleMassKg / 1000.0;
        // Using the current state threshold is tricky in a closure if stale, but it's safe for simple recalculations. 
        // We will default to 50 if it's undefined.
        const isExempt = elMassTonnes <= 50 && elMassTonnes > 0;
        const activeTaxEur = isExempt ? ineligibleTaxEur : totalCbamEur;
        
        // Reverse engineer taxable equivalent kg (Tax = Tonnes * €75)
        taxableKg = activeTaxEur / 0.075;

        setResultsData(parsedData);
        setTotalCO2(total);
        setTotalCbamCost(activeTaxEur);"""

new_calc = """        const elMassTonnes = eligibleMassKg / 1000.0;
        const isExempt = elMassTonnes <= 50 && elMassTonnes > 0;
        // Tax is now fully processed by the backend per-row, so totalCbamEur is inherently correct
        const activeTaxEur = totalCbamEur;
        
        // Reverse engineer taxable equivalent kg (Tax = Tonnes * €75)
        taxableKg = activeTaxEur / 0.075;

        setResultsData(parsedData);
        setTotalCO2(total);
        setTotalCbamCost(activeTaxEur);"""
code = code.replace(old_calc, new_calc)

# 2. Update UI block for DeMinimis rendering
old_ui = """                {isDeMinimisExempt ? (
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
                )}"""

new_ui = """                <h3 className="text-3xl font-bold text-amber-500">€{estimatedTaxEUR.toLocaleString(undefined, { maximumFractionDigits: 2 })}</h3>
                <p className="text-xs text-slate-400 mt-2 font-medium">@ €75/tCO₂e · assumes emissions near benchmark</p>
                {isDeMinimisExempt && (
                  <div className="mt-3 bg-emerald-50 dark:bg-emerald-900/20 p-2 rounded border border-emerald-100 dark:border-emerald-800">
                    <p className="text-xs text-emerald-600 dark:text-emerald-400 font-medium">
                      <span className="font-bold">De Minimis Applied:</span> {eligibleMassTonnes.toLocaleString(undefined, { maximumFractionDigits: 1 })} t of eligible goods excluded (≤ {deMinimisThreshold} t limit).
                    </p>
                  </div>
                )}"""
code = code.replace(old_ui, new_ui)


with open(r"c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\analytics\cbam\page.tsx", "w", encoding="utf-8") as f:
    f.write(code)

print("Frontend patched successfully.")
