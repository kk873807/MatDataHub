"use client";
import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { ArrowLeft, Factory, UploadCloud, Loader2, FileSpreadsheet, Lock, Download, FileText, Table, AlertTriangle, Clock, Trash2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { API } from "@/lib/api";
import Papa from "papaparse";

// Columns that are audit/diagnostic detail: shown on screen, hidden in the printed report.
const DIAGNOSTIC_COLUMNS = new Set([
  "Parsed_Weight_kg", "Weight_Unit_Basis", "Importer", "Other_Imports_t", "Lookup_Year", "DeMinimis_Eligible_Mass_kg",
  "Emissions_Basis", "Default_Dataset", "Default_Match_Digits", "Default_Geography", "Default_Country_Matched",
  "Default_Base_Value", "Default_Markup_Pct", "Total_CO2_kg", "Provisional_CO2_kg", "Provisional_CO2_tonnes",
  "Domestic_Carbon_Price_Paid_EUR", "Reference_Price_EUR_per_tCO2e", "Is_Obsolete", "Replacement_Standard",
  "ESG_Risk_Score", "Notes", "CBAM_Estimate_Notice", "CBAM_Cost_If_Not_Exempt_EUR", "CBAM_Cost_After_DeMinimis_EUR",
  "CBAM_Taxable_CO2_tonnes", "DeMinimis_Status", "CBAM_Defaults_Info",
]);

// Phase-in share of the cost used by the what-if selector (the backend applies the full schedule per shipment year).
const WHAT_IF_PHASE_IN: Record<"2026" | "2027" | "2034", number> = { "2026": 0.025, "2027": 0.05, "2034": 1.0 };

// Quote a value for a hand-built CSV row (a comma, quote or newline in a cell would otherwise shift every later column).
const csvCell = (v: string) => (/[",\r\n]/.test(v) ? `"${v.replace(/"/g, '""')}"` : v);

export default function CBAMAnalytics() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<"upload" | "manual" | "history">("upload");
  const [historyData, setHistoryData] = useState<any[]>([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [selectedHistoryItem, setSelectedHistoryItem] = useState<any | null>(null);
  const [historyDetailData, setHistoryDetailData] = useState<any[] | null>(null);
  const [historyDetailLoading, setHistoryDetailLoading] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  
  // CSV Configuration
  const [materialCol, setMaterialCol] = useState("Material");
  const [weightCol, setWeightCol] = useState("Weight_kg");
  const [hardQuarantine, setHardQuarantine] = useState(true);
  const [disableDeMinimis, setDisableDeMinimis] = useState(false);
  
  // Manual Entry State
  const [manualMaterial, setManualMaterial] = useState("");
  const [manualWeight, setManualWeight] = useState("");
  const [manualCnCode, setManualCnCode] = useState("");
  const [manualSector, setManualSector] = useState("");
  const [manualOrigin, setManualOrigin] = useState("");

  const fetchHistory = async () => {
    setHistoryLoading(true);
    try {
      const token = localStorage.getItem("token");
      if (!token) return;
      const res = await fetch(`${API}/account/bom-history`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        setHistoryData(await res.json());
      }
    } catch (e) {
      console.error(e);
    } finally {
      setHistoryLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === "history") {
      fetchHistory();
    }
  }, [activeTab]);

  const loadHistoryItem = async (item: any) => {
    setSelectedHistoryItem(item);
    setHistoryDetailLoading(true);
    setHistoryDetailData(null);
    try {
      const token = localStorage.getItem("token");
      if (!token) return;
      const res = await fetch(`${API}/account/bom-history/${item.id}`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        if (data.results_json) {
          try {
            const parsed = JSON.parse(data.results_json);
            // New format: {metadata: {...}, rows: [...]}
            // Old format: [...]
            if (parsed.rows && Array.isArray(parsed.rows)) {
              setHistoryDetailData(parsed.rows);
            } else if (Array.isArray(parsed)) {
              setHistoryDetailData(parsed);
            } else {
              setHistoryDetailData([]);
            }
          } catch (err) {
            console.error("Failed to parse history json", err);
            setHistoryDetailData([]);
          }
        } else if (data.results_data && data.results_data.length > 0) {
          // Fallback for old API format
          setHistoryDetailData(data.results_data);
        } else {
          setHistoryDetailData([]);
        }
      }
    } catch (e) {
      console.error(e);
      setHistoryDetailData([]);
    } finally {
      setHistoryDetailLoading(false);
    }
  };

  const deleteHistoryItem = async (e: React.MouseEvent, id: number) => {
    e.stopPropagation(); // Prevent opening the detail view
    if (!confirm("Are you sure you want to delete this BOM analysis history?")) return;
    
    try {
      const token = localStorage.getItem("token");
      const res = await fetch(`${API}/account/bom-history/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        setHistoryData(prev => prev.filter(item => item.id !== id));
      } else {
        alert("Failed to delete history item.");
      }
    } catch (err) {
      console.error(err);
      alert("Error deleting history item.");
    }
  };

  // Results state
  const [loading, setLoading] = useState(false);
  const [isLocked, setIsLocked] = useState(true);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const [resultsData, setResultsData] = useState<any[] | null>(null);
  const [totalCO2, setTotalCO2] = useState(0);
  const [totalCbamCost, setTotalCbamCost] = useState(0);
  const [selectedYear, setSelectedYear] = useState<"ACTUAL" | "2034" | "2027" | "2026">("ACTUAL");
  const [pendingReviewCount, setPendingReviewCount] = useState(0);
  const [pendingReviewTonnes, setPendingReviewTonnes] = useState(0);
  const [fallbackTonnes, setFallbackTonnes] = useState(0);
  const [interimStats, setInterimStats] = useState({ rows: 0, heading: 0, global: 0 });
  const [taxableTonnes, setTaxableTonnes] = useState(0);
  const [deMinimisThreshold, setDeMinimisThreshold] = useState(50);
  const [isDeMinimisExempt, setIsDeMinimisExempt] = useState(false);
  const [eligibleMassTonnes, setEligibleMassTonnes] = useState(0);
  const [costIfNotExempt, setCostIfNotExempt] = useState(0);
  const [taxRows, setTaxRows] = useState<{ tonnes: number; net: number; deMin: boolean }[]>([]);
  const [referencePrice, setReferencePrice] = useState(75);
  const [defaultsSources, setDefaultsSources] = useState<string[]>([]);
  const [generatedAt, setGeneratedAt] = useState("");
  const [historyNotSaved, setHistoryNotSaved] = useState(false);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        setIsLocked(true);
        setIsCheckingAuth(false);
        return;
      }
      try {
        const res = await fetch(`${API}/auth/me`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (!res.ok) {
          setIsLocked(true);
          setIsCheckingAuth(false);
          return;
        }
        const data = await res.json();
        // Check admin or advanced tier
        if (data.is_admin || data.tier === "advanced") {
          setIsLocked(false);
        } else {
          setIsLocked(true);
        }
      } catch (err) {
        setIsLocked(true);
      } finally {
        setIsCheckingAuth(false);
      }
    };
    checkAuth();
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const DEMO_BOMS = {
    automotive: `material_id,Material,Weight_kg,cbam_sector,cn_code,country_of_origin,destination,release_date,supplier,importer
MAT-A1,Hot-Rolled Steel Coil,50000,Iron & Steel,7208 39 00,China,Germany,2026-06-15,Acme Metals,DE1234567890123
MAT-A2,Aluminium Alloy Bar,15000,Aluminium,7604 29 10,India,Germany,2026-06-15,Global Alum,DE1234567890123
MAT-A3,Plastic Dashboard,5000,,,Vietnam,Germany,2026-06-15,PolyCorp,DE1234567890123
MAT-A4,Stainless Steel Fasteners,2000,Iron & Steel,7318 15 20,Taiwan,Germany,2026-06-15,FastenTech,DE1234567890123`,
    construction: `material_id,Material,Weight_kg,cbam_sector,cn_code,country_of_origin,destination,release_date,supplier,importer
MAT-C1,Portland Cement,200000,Cement,2523 29 00,Turkey,France,2026-08-01,EuroCement,FR9876543210987
MAT-C2,Steel Rebar,100000,Iron & Steel,7214 20 00,China,France,2026-08-01,SteelCo,FR9876543210987
MAT-C3,Aluminium Window Frames,10000,Aluminium,7610 10 00,China,France,2026-08-01,AlumBuild,FR9876543210987
MAT-C4,Glass Panes,5000,,,India,France,2026-08-01,ClearGlass,FR9876543210987`
  };

  const handleLoadDemo = (type: "automotive" | "construction") => {
    const csvStr = DEMO_BOMS[type];
    const demoFile = new File([csvStr], `${type}_bom_demo.csv`, { type: "text/csv" });
    setFile(demoFile);
    processBOM(demoFile, "Material", "Weight_kg");
  };

  const downloadTemplate = () => {
    const csvContent = "material_id,Material,Weight_kg,cbam_sector,cn_code,country_of_origin,destination,release_date,supplier,importer,carbon_price_paid_eur_per_tco2e\nMAT-001,Hot-Rolled Steel Plate,10000,Iron & Steel,7208 39 00,China,Germany,2026-06-15,Example Supplier,DE0000000000000,0\n";
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "cbam_template.csv";
    a.click();
    URL.revokeObjectURL(url);
  };

  const generatePDF = () => {
    // We use native browser printing because html2canvas does not support
    // modern CSS color functions (like oklch) used by Tailwind v4.
    // print:hidden classes will ensure only the report is visible.
    window.print();
  };


  const processBOM = async (demoFile?: File | any, demoMatCol?: string | any, demoWeightCol?: string | any) => {
    const isFile = demoFile instanceof File;
    let payloadFile = isFile ? demoFile : file;
    let payloadMatCol = typeof demoMatCol === 'string' ? demoMatCol : materialCol;
    let payloadWeightCol = typeof demoWeightCol === 'string' ? demoWeightCol : weightCol;

    if (activeTab === "manual" && !isFile) {
      if (!manualMaterial || !manualWeight) {
        alert("Please enter both material and weight.");
        return;
      }
      if (!manualCnCode && !manualSector) {
        alert("Please select a CBAM Sector (e.g. Iron & Steel) or enter a CN Code. The calculator needs to know the material category to apply EU CBAM rules.");
        return;
      }
      // Generate virtual CSV with proper quoting to handle commas in material names
      // Every user-typed cell goes through csvCell (a weight typed as "1,5" used to add a column and shift the rest of the row).
      const origin = manualOrigin || "India";
      const today = new Date().toISOString().slice(0, 10); // manual entries are priced at today's release date, not a fixed 2026-01-01
      const csvContent = `material_id,Material,Weight_kg,cn_code,cbam_sector,country_of_origin,destination,release_date,supplier\nMANUAL-01,${csvCell(manualMaterial)},${csvCell(manualWeight)},${csvCell(manualCnCode)},${csvCell(manualSector)},${csvCell(origin)},Germany,${today},Manual Entry\n`;
      payloadFile = new File([csvContent], "manual_entry.csv", { type: "text/csv" });
      payloadMatCol = "Material";
      payloadWeightCol = "Weight_kg";
    } else {
      if (!payloadFile) return;
    }

    setLoading(true);
    setResultsData(null);
    setTotalCO2(0);

    try {
      const formData = new FormData();
      formData.append("file", payloadFile as File);
      formData.append("material_col", payloadMatCol);
      formData.append("weight_col", payloadWeightCol);
      formData.append("strict_mode", activeTab === "manual" ? "false" : hardQuarantine.toString());
      formData.append("disable_deminimis", disableDeMinimis.toString());

      // Note: Make sure the backend doesn't expect authentication, or send token if needed
      const token = localStorage.getItem("token");
      const headers: Record<string, string> = {};
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const res = await fetch(`${API}/materials/bom_analyze`, {
        method: "POST",
        headers,
        body: formData,
      });

      if (res.ok) {
        const text = await res.text();
        // Parse CSV text for live preview using PapaParse for robust comma handling
        const parsed = Papa.parse(text, { header: true, skipEmptyLines: true });
        const parsedData = parsed.data as any[];
        
        const num = (v: any) => {
          const n = parseFloat(v);
          return Number.isFinite(n) ? n : 0;
        };
        const hasTaxableCol = parsedData.length > 0 && "CBAM_Taxable_CO2_tonnes" in parsedData[0];
        const refHeader = parseFloat(res.headers.get("X-CBAM-Reference-Price") || "");
        const refPrice = Number.isFinite(refHeader) ? refHeader : 75;

        let total = 0;                 // CO2 (kg) of rows included in totals
        let costNotExempt = 0;         // cost if the importer is NOT under the de minimis threshold
        let costAfterDeMin = 0;        // cost after the de minimis outcome for each importer-year
        let revCount = 0;              // quarantined rows
        let revTonnes = 0;
        let fallbackKg = 0;
        let interimRows = 0;
        let interimHeadingRows = 0;
        let interimGlobalRows = 0;
        let deMinMassKg = 0;
        let taxableKg = 0;
        let anyDeMin = false;
        const rowsForTax: { tonnes: number; net: number; deMin: boolean }[] = [];
        const sources = new Set<string>();

        parsedData.forEach((rowObj: any) => {
          const included = String(rowObj["Included_In_Total"] || "");
          if (included.startsWith("YES")) {
            const rowKg = num(rowObj["Total_CO2_kg"]);
            total += rowKg;

            const rowEur = num(rowObj["CBAM_Cost_EUR"]);
            const deMin = String(rowObj["DeMinimis_Status"] || "").startsWith("Possibly exempt");
            costNotExempt += rowEur;
            costAfterDeMin += deMin ? 0 : rowEur;

            const taxT = hasTaxableCol ? num(rowObj["CBAM_Taxable_CO2_tonnes"]) : num(rowObj["Total_CO2_tonnes"]);
            const netPrice = rowObj["Reference_Price_EUR_per_tCO2e"] !== undefined && rowObj["Reference_Price_EUR_per_tCO2e"] !== ""
              ? num(rowObj["Reference_Price_EUR_per_tCO2e"]) : refPrice;
            rowsForTax.push({ tonnes: taxT, net: netPrice, deMin });
            if (deMin) {
              anyDeMin = true;
              deMinMassKg += num(rowObj["DeMinimis_Eligible_Mass_kg"]);
            } else {
              taxableKg += taxT * 1000;
            }

            const basis = rowObj["Emissions_Basis"];
            if (basis === "DEFAULT_FALLBACK" || basis === "LEGACY_FALLBACK" || basis === "GENERIC_ESTIMATE") {
              fallbackKg += rowKg;
            }
            if (basis === "COMMISSION_DEFAULT") {
              interimRows += 1;
              if (parseInt(rowObj["Default_Match_Digits"] || "0", 10) < 8) interimHeadingRows += 1;
              if (rowObj["Default_Geography"] !== "COUNTRY") interimGlobalRows += 1;
              if (rowObj["Default_Dataset"] && rowObj["Default_Dataset"] !== "N/A") sources.add(rowObj["Default_Dataset"]);
            }
          } else if (included.startsWith("QUARANTINE")) {
            // (the old test was startsWith("NO"), which never matched "QUARANTINED: ...", so this count was always 0)
            revCount += 1;
            revTonnes += num(rowObj["Parsed_Weight_kg"]) / 1000.0;
          }
        });

        setResultsData(parsedData);
        setTotalCO2(total);
        setTotalCbamCost(costAfterDeMin);
        setCostIfNotExempt(costNotExempt);
        setTaxRows(rowsForTax);
        setReferencePrice(refPrice);
        setPendingReviewCount(revCount);
        setPendingReviewTonnes(revTonnes);
        setFallbackTonnes(fallbackKg / 1000.0);
        setInterimStats({ rows: interimRows, heading: interimHeadingRows, global: interimGlobalRows });
        setDefaultsSources(Array.from(sources));
        setTaxableTonnes(taxableKg / 1000.0);
        setIsDeMinimisExempt(anyDeMin);
        setEligibleMassTonnes(deMinMassKg / 1000.0);
        setGeneratedAt(new Date().toLocaleString());
        setHistoryNotSaved(res.headers.get("X-CBAM-History-Saved") === "false");
      } else if (res.status === 403) {
        setIsLocked(true);
      } else {
        alert("Error processing BOM. Check column names and file format.");
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const downloadResults = () => {
    if (!resultsData) return;
    const csvContent = Papa.unparse(resultsData);
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "enriched_bom_cbam.csv";
    a.click();
    URL.revokeObjectURL(url);
  };

  if (isCheckingAuth) {
    return <div className="flex items-center justify-center h-screen"><Loader2 className="w-8 h-8 animate-spin text-amber-500" /></div>;
  }

  if (isLocked) {
    return (
      <main className="flex flex-col p-6 lg:p-10 w-full h-full">
        <div className="w-full max-w-5xl print:max-w-none mx-auto space-y-6">
          <Link href="/analytics" className="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back to Analytics
          </Link>
          
          <div className="p-10 mt-10 rounded-3xl bg-white dark:bg-slate-900 border border-amber-500/30 text-center relative overflow-hidden print:overflow-visible flex flex-col items-center justify-center">
            <div className="absolute inset-0 bg-gradient-to-br from-amber-900/20 to-transparent"></div>
            <div className="w-20 h-20 bg-amber-950 rounded-full flex items-center justify-center mb-6 relative z-10 border border-amber-500/50 shadow-[0_0_30px_rgba(245,158,11,0.2)]">
              <Lock className="w-10 h-10 text-amber-500" />
            </div>
            
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white font-heading mb-4 relative z-10">Enterprise Feature</h2>
            <p className="text-slate-600 dark:text-slate-300 relative z-10 max-w-2xl mx-auto mb-8 text-lg">
              Supply Chain Risk & CBAM (Carbon Border Adjustment Mechanism) modeling requires a dedicated Enterprise environment. 
              Automatically scan bulk Bills of Materials (BOMs) for embargoed materials, geographic obsolescence, and carbon taxation thresholds.
            </p>
            
            <div className="relative z-10 flex flex-col sm:flex-row gap-3 items-center">
              <Link href="/account" className="px-8 py-4 bg-amber-600 hover:bg-amber-700 text-white rounded-xl font-bold transition-all shadow-lg shadow-amber-900/50 hover:scale-105">
                Upgrade to Advanced
              </Link>
              <Link href="/contact" className="px-8 py-4 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white rounded-xl font-bold transition-colors">
                Talk to us
              </Link>
            </div>
          </div>
        </div>
      </main>
    );
  }

  // Cost comes from the backend row by row (reference price, carbon price paid, phase-in for each shipment year, de minimis).
  // A what-if year re-prices the SAME taxable tonnes: net of carbon price paid, excluding de minimis rows.
  const whatIfCost = (year: "2026" | "2027" | "2034") =>
    taxRows.reduce((sum, r) => (r.deMin ? sum : sum + r.tonnes * r.net * WHAT_IF_PHASE_IN[year]), 0);
  const estimatedTaxEUR = selectedYear === "ACTUAL" ? totalCbamCost : whatIfCost(selectedYear);
  const eur = (v: number) => v.toLocaleString(undefined, { maximumFractionDigits: 2 });

  return (
    <main 
      className="flex flex-col p-6 lg:p-10 w-full h-full overflow-y-auto print:overflow-visible print:h-auto print:p-8 print:bg-white"
      style={{ WebkitPrintColorAdjust: 'exact', printColorAdjust: 'exact' }}
    >
      <div className="w-full max-w-5xl print:max-w-none mx-auto space-y-8 ">
        
        <Link href="/analytics" className="print:hidden inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white transition-colors">
          <ArrowLeft className="w-4 h-4" /> Back to Analytics
        </Link>

        <div className="print:hidden">
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white font-heading flex items-center gap-3">
            <Factory className="w-8 h-8 text-amber-500" />
            CBAM Estimate & Supply Chain Risk
          </h1>
          <p className="text-slate-600 dark:text-slate-300 mt-2">Upload your Bill of Materials or enter manually to estimate CBAM carbon costs and supply chain risk.</p>
          
          <div className="mt-4 p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg flex items-start gap-3 text-amber-800 dark:text-amber-200 text-sm max-w-4xl">
            <AlertTriangle className="w-5 h-5 shrink-0 mt-0.5" />
            <div>
              <strong>For Planning & Estimation Only</strong><br/>
              This tool is not a substitute for professional compliance advice. Calculations, scope mappings, and default emission values may not perfectly reflect final EU Customs determinations or your specific regulatory obligations.
            </div>
          </div>
        </div>

        <div className="print:hidden bg-white dark:bg-slate-900 p-8 rounded-2xl border border-slate-200 dark:border-slate-800">
          
          {/* Tabs */}
          <div className="flex gap-4 mb-6 border-b border-slate-200 dark:border-slate-800 pb-4">
            <button
              onClick={() => setActiveTab("upload")}
              className={`px-4 py-2 font-bold rounded-2xl transition-colors ${activeTab === "upload" ? "bg-amber-100 dark:bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400" : "text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white"}`}
            >
              Upload CSV
            </button>
            <button
              onClick={() => setActiveTab("manual")}
              className={`px-4 py-2 font-bold rounded-2xl transition-colors ${activeTab === "manual" ? "bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400" : "text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white"}`}
            >
              Manual Entry
            </button>
            <button
              onClick={() => setActiveTab("history")}
              className={`px-4 py-2 font-bold rounded-2xl transition-colors ${activeTab === "history" ? "bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400" : "text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white"}`}
            >
              <span className="flex items-center gap-2">
                <Clock className="w-4 h-4" /> History
              </span>
            </button>
          </div>

          {activeTab === "upload" && (
            <div className="space-y-6">
              <div className="flex justify-between items-end">
                <div className="grid grid-cols-2 gap-6 flex-1 max-w-xl">
                  <div>
                    <label className="block text-sm font-semibold text-slate-600 dark:text-slate-300 mb-2">Material Column Header</label>
                    <input
                      type="text"
                      value={materialCol}
                      onChange={e => setMaterialCol(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-2.5 text-slate-900 dark:text-white outline-none focus:border-amber-500"
                      placeholder="e.g. Material"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-slate-600 dark:text-slate-300 mb-2">Weight Column Header (kg)</label>
                    <input
                      type="text"
                      value={weightCol}
                      onChange={e => setWeightCol(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-2.5 text-slate-900 dark:text-white outline-none focus:border-amber-500"
                      placeholder="e.g. Weight_kg"
                    />
                  </div>
                </div>
                <button onClick={downloadTemplate} className="text-amber-500 hover:text-amber-600 dark:text-amber-400 text-sm font-medium flex items-center gap-1">
                  <Download className="w-4 h-4" /> Template
                </button>
              </div>
              <div className="space-y-3 pt-2">
                <label className="flex items-center gap-3 cursor-pointer group">
                  <div className={`w-11 h-6 flex items-center rounded-full p-1 transition-colors ${hardQuarantine ? 'bg-amber-500' : 'bg-slate-300 dark:bg-slate-700'}`}>
                    <div className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform ${hardQuarantine ? 'translate-x-5' : ''}`}></div>
                  </div>
                  <input type="checkbox" className="hidden" checked={hardQuarantine} onChange={e => setHardQuarantine(e.target.checked)} />
                  <div>
                    <span className="text-sm font-semibold text-slate-700 dark:text-slate-300 group-hover:text-amber-600 transition-colors">Strict Quarantine</span>
                    <p className="text-xs text-slate-500 dark:text-slate-400">Quarantine rows with missing CN code, country, date or emissions data.</p>
                  </div>
                </label>
                <label className="flex items-center gap-3 cursor-pointer group">
                  <div className={`w-11 h-6 flex items-center rounded-full p-1 transition-colors ${disableDeMinimis ? 'bg-red-500' : 'bg-slate-300 dark:bg-slate-700'}`}>
                    <div className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform ${disableDeMinimis ? 'translate-x-5' : ''}`}></div>
                  </div>
                  <input type="checkbox" className="hidden" checked={disableDeMinimis} onChange={e => setDisableDeMinimis(e.target.checked)} />
                  <div>
                    <span className="text-sm font-semibold text-slate-700 dark:text-slate-300 group-hover:text-red-600 transition-colors">Ignore De Minimis Exemption</span>
                    <p className="text-xs text-slate-500 dark:text-slate-400">Treat all in-scope goods as chargeable regardless of the 50 t threshold.</p>
                  </div>
                </label>
              </div>

              <div 
                onDragOver={e => e.preventDefault()}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-colors ${file ? 'border-amber-500 bg-amber-100 dark:bg-amber-100 dark:bg-amber-900/10' : 'border-slate-200 dark:border-slate-700 hover:border-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800/50'}`}
              >
                <input 
                  type="file" 
                  accept=".csv" 
                  ref={fileInputRef} 
                  className="hidden" 
                  onChange={handleFileChange} 
                />
                {file ? (
                  <div className="flex flex-col items-center">
                    <FileSpreadsheet className="w-12 h-12 text-amber-500 mb-3" />
                    <p className="font-bold text-slate-900 dark:text-white">{file.name}</p>
                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Ready to process</p>
                  </div>
                ) : (
                  <div className="flex flex-col items-center">
                    <UploadCloud className="w-12 h-12 text-slate-500 dark:text-slate-400 mb-3" />
                    <p className="font-bold text-slate-900 dark:text-white text-lg">Click or drag BOM CSV file here</p>
                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Must contain material and weight columns (Max 5,000 rows / 10MB)</p>
                  </div>
                )}
              </div>

              {/* Demo Buttons */}
              <div className="flex flex-col items-center mt-6">
                <p className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-3">No CSV? Try with demo data:</p>
                <div className="flex gap-4">
                  <button 
                    onClick={() => handleLoadDemo('automotive')}
                    className="px-4 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl text-sm font-semibold transition-colors flex items-center gap-2"
                  >
                    🚗 Automotive BOM
                  </button>
                  <button 
                    onClick={() => handleLoadDemo('construction')}
                    className="px-4 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl text-sm font-semibold transition-colors flex items-center gap-2"
                  >
                    🏗️ Construction BOM
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === "manual" && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 bg-slate-50 dark:bg-slate-950 p-6 rounded-xl border border-slate-200 dark:border-slate-800">
              <div>
                <label className="block text-sm font-semibold text-slate-600 dark:text-slate-300 mb-2">Material Name / Grade</label>
                <input
                  type="text"
                  value={manualMaterial}
                  onChange={e => setManualMaterial(e.target.value)}
                  className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-2.5 text-slate-900 dark:text-white outline-none focus:border-amber-500"
                  placeholder="e.g. Steel 304L"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-600 dark:text-slate-300 mb-2">Total Weight (kg)</label>
                <input
                  type="number"
                  value={manualWeight}
                  onChange={e => setManualWeight(e.target.value)}
                  className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-2.5 text-slate-900 dark:text-white outline-none focus:border-amber-500"
                  placeholder="e.g. 1500"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-600 dark:text-slate-300 mb-2">CN Code (Provide this or Sector)</label>
                <input
                  type="text"
                  value={manualCnCode}
                  onChange={e => setManualCnCode(e.target.value)}
                  className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-2.5 text-slate-900 dark:text-white outline-none focus:border-amber-500"
                  placeholder="e.g. 7208 39 00"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-600 dark:text-slate-300 mb-2">CBAM Sector (Provide this or CN Code)</label>
                <select
                  value={manualSector}
                  onChange={e => setManualSector(e.target.value)}
                  className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-2.5 text-slate-900 dark:text-white outline-none focus:border-amber-500"
                >
                  <option value="">Auto-detect / Not Sure</option>
                  <option value="Iron & Steel">Iron & Steel</option>
                  <option value="Aluminium">Aluminium</option>
                  <option value="Cement">Cement</option>
                  <option value="Fertilisers">Fertilisers</option>
                  <option value="Hydrogen">Hydrogen</option>
                  <option value="Electricity">Electricity</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-600 dark:text-slate-300 mb-2">Country of Origin (Optional)</label>
                <input
                  type="text"
                  value={manualOrigin}
                  onChange={e => setManualOrigin(e.target.value)}
                  className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-2.5 text-slate-900 dark:text-white outline-none focus:border-amber-500"
                  placeholder="e.g. China, India, UK"
                />
              </div>
            </div>
          )}

          {activeTab === "history" && (
            <div className="space-y-4">
              {/* Detail View */}
              {selectedHistoryItem ? (
                <div className="space-y-6">
                  {/* Header with back button */}
                  <div className="flex items-center gap-4">
                    <button
                      onClick={() => { setSelectedHistoryItem(null); setHistoryDetailData(null); }}
                      className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl transition-colors"
                    >
                      <ArrowLeft className="w-5 h-5 text-slate-600 dark:text-slate-400" />
                    </button>
                    <div>
                      <h3 className="text-lg font-bold text-slate-900 dark:text-white">{selectedHistoryItem.filename}</h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400">
                        {new Date(selectedHistoryItem.created_at).toLocaleDateString()} {new Date(selectedHistoryItem.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                        {" · "}
                        <span className={`font-bold ${selectedHistoryItem.strict_mode ? 'text-amber-500' : 'text-emerald-500'}`}>
                          {selectedHistoryItem.strict_mode ? 'Strict Quarantine' : 'Normal'}
                        </span>
                      </p>
                    </div>
                  </div>

                  {/* Summary Cards */}
                  <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4">
                      <p className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Total CO₂</p>
                      <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{(selectedHistoryItem.total_co2_tonnes || 0).toFixed(2)} <span className="text-sm font-normal text-slate-500">t</span></p>
                    </div>
                    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4">
                      <p className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">CBAM Cost</p>
                      <p className="text-2xl font-bold text-amber-600 dark:text-amber-400 mt-1">€{(selectedHistoryItem.cbam_cost_eur || 0).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
                    </div>
                    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4">
                      <p className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Total Rows</p>
                      <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{selectedHistoryItem.total_rows}</p>
                    </div>
                    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4">
                      <p className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Quarantined</p>
                      <p className={`text-2xl font-bold mt-1 ${selectedHistoryItem.quarantined_rows > 0 ? 'text-red-500' : 'text-emerald-500'}`}>{selectedHistoryItem.quarantined_rows}</p>
                    </div>
                  </div>

                  {/* Results Table */}
                  {historyDetailLoading ? (
                    <div className="flex items-center justify-center py-12">
                      <Loader2 className="w-6 h-6 animate-spin text-amber-500" />
                      <span className="ml-2 text-slate-500 dark:text-slate-400">Loading detailed results...</span>
                    </div>
                  ) : historyDetailData && historyDetailData.length > 0 ? (
                    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden print:overflow-visible">
                      <div className="p-4 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/50">
                        <h4 className="font-bold text-slate-900 dark:text-white flex items-center gap-2">
                          <Table className="w-4 h-4 text-amber-500" /> Line-by-Line Breakdown
                        </h4>
                      </div>
                      <div className="overflow-x-auto max-h-[500px] print:max-h-none print:overflow-visible overflow-y-auto">
                        <table className="w-full text-xs">
                          <thead className="sticky top-0 bg-slate-100 dark:bg-slate-950">
                            <tr>
                              <th className="text-left px-3 py-2 font-bold text-slate-600 dark:text-slate-400">Material</th>
                              <th className="text-right px-3 py-2 font-bold text-slate-600 dark:text-slate-400">Weight (kg)</th>
                              <th className="text-left px-3 py-2 font-bold text-slate-600 dark:text-slate-400">Sector</th>
                              <th className="text-left px-3 py-2 font-bold text-slate-600 dark:text-slate-400">Origin</th>
                              <th className="text-right px-3 py-2 font-bold text-slate-600 dark:text-slate-400">CO₂ (t)</th>
                              <th className="text-right px-3 py-2 font-bold text-slate-600 dark:text-slate-400">CBAM (€)</th>
                              <th className="text-left px-3 py-2 font-bold text-slate-600 dark:text-slate-400">Basis</th>
                              <th className="text-left px-3 py-2 font-bold text-slate-600 dark:text-slate-400">Status</th>
                              <th className="text-left px-3 py-2 font-bold text-slate-600 dark:text-slate-400 min-w-[200px]">Notes</th>
                            </tr>
                          </thead>
                          <tbody>
                            {historyDetailData.slice(0, 500).map((row: any, i: number) => {
                              const included = (row.Included_In_Total || "").toString();
                              const isYes = included.startsWith("YES");
                              const isNo = included.startsWith("NO") || included.startsWith("QUARANTINE");
                              return (
                                <tr key={i} className={`border-b border-slate-100 dark:border-slate-800 ${isNo ? 'bg-red-50/50 dark:bg-red-950/10' : ''}`}>
                                  <td className="px-3 py-2 text-slate-900 dark:text-white font-semibold max-w-[180px] truncate">{row.Material || row.material_id || '-'}</td>
                                  <td className="px-3 py-2 text-right text-slate-700 dark:text-slate-300 font-mono">{parseFloat(row.Parsed_Weight_kg || 0).toLocaleString()}</td>
                                  <td className="px-3 py-2 text-slate-600 dark:text-slate-400">{row.cbam_sector || '-'}</td>
                                  <td className="px-3 py-2 text-slate-600 dark:text-slate-400">{row.country_of_origin || '-'}</td>
                                  <td className="px-3 py-2 text-right text-slate-700 dark:text-slate-300 font-mono">{parseFloat(row.Total_CO2_tonnes || 0).toFixed(3)}</td>
                                  <td className="px-3 py-2 text-right font-bold text-slate-900 dark:text-white font-mono">€{parseFloat(row.CBAM_Cost_EUR || 0).toFixed(2)}</td>
                                  <td className="px-3 py-2">
                                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                                      row.Emissions_Basis === 'VERIFIED' ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400' :
                                      'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400'
                                    }`}>{row.Emissions_Basis || '-'}</span>
                                  </td>
                                  <td className="px-3 py-2">
                                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                                      isYes ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400' :
                                      included.startsWith("OUT OF SCOPE") ? 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400' :
                                      'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
                                    }`}>{isYes ? 'INCLUDED' : included.startsWith("OUT OF SCOPE") ? 'OUT OF SCOPE' : 'QUARANTINE'}</span>
                                  </td>
                                  <td className="px-3 py-2 text-slate-500 dark:text-slate-400 text-[11px] max-w-[250px] truncate" title={row.Notes || ''}>{row.Notes || '-'}</td>
                                </tr>
                              );
                            })}
                          </tbody>
                        </table>
                      </div>
                      {historyDetailData.length > 500 && (
                        <div className="p-3 text-center text-sm text-slate-500 dark:text-slate-400 bg-slate-50 dark:bg-slate-950/50 border-t border-slate-200 dark:border-slate-800">
                          Showing first 500 of {historyDetailData.length.toLocaleString()} rows. Download the full CSV from the upload tab for complete data.
                        </div>
                      )}
                    </div>
                  ) : historyDetailData && historyDetailData.length === 0 ? (
                    <div className="text-center py-8 text-slate-500 dark:text-slate-400 bg-slate-50 dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
                      <AlertTriangle className="w-8 h-8 mx-auto mb-2 text-amber-500" />
                      <p className="font-semibold">Detailed results unavailable</p>
                      <p className="text-sm mt-1">This analysis was run before detailed logging was enabled.</p>
                    </div>
                  ) : null}
                </div>
              ) : (
              /* History List View */
              <div>
              <h3 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2 mb-4">
                <Clock className="w-5 h-5 text-amber-500" /> Analysis History
              </h3>
              {historyLoading ? (
                <div className="flex items-center justify-center py-12">
                  <Loader2 className="w-6 h-6 animate-spin text-amber-500" />
                  <span className="ml-2 text-slate-500 dark:text-slate-400">Loading history...</span>
                </div>
              ) : historyData.length === 0 ? (
                <div className="text-center py-12 text-slate-500 dark:text-slate-400">
                  <FileSpreadsheet className="w-12 h-12 mx-auto mb-3 opacity-40" />
                  <p className="font-semibold">No analyses yet</p>
                  <p className="text-sm mt-1">Upload a BOM CSV or try demo data to get started.</p>
                </div>
              ) : (
                <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden print:overflow-visible">
                  <div className="overflow-x-auto print:overflow-visible">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="bg-slate-50 dark:bg-slate-950/50 border-b border-slate-200 dark:border-slate-800">
                          <th className="text-left px-4 py-3 font-bold text-slate-700 dark:text-slate-300">#</th>
                          <th className="text-left px-4 py-3 font-bold text-slate-700 dark:text-slate-300">File</th>
                          <th className="text-left px-4 py-3 font-bold text-slate-700 dark:text-slate-300">Date</th>
                          <th className="text-right px-4 py-3 font-bold text-slate-700 dark:text-slate-300">Rows</th>
                          <th className="text-right px-4 py-3 font-bold text-slate-700 dark:text-slate-300">Quarantined</th>
                          <th className="text-right px-4 py-3 font-bold text-slate-700 dark:text-slate-300">CO₂ (t)</th>
                          <th className="text-right px-4 py-3 font-bold text-slate-700 dark:text-slate-300">CBAM Cost (€)</th>
                          <th className="text-center px-4 py-3 font-bold text-slate-700 dark:text-slate-300">Mode</th>
                          <th className="text-center px-4 py-3 font-bold text-slate-700 dark:text-slate-300">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {historyData.map((item: any, idx: number) => (
                          <tr 
                            key={item.id} 
                            onClick={() => loadHistoryItem(item)}
                            className="border-b border-slate-100 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors cursor-pointer group"
                          >
                            <td className="px-4 py-3 text-slate-500 dark:text-slate-400 font-mono text-xs">{idx + 1}</td>
                            <td className="px-4 py-3 text-slate-900 dark:text-white font-semibold truncate max-w-[200px]">{item.filename}</td>
                            <td className="px-4 py-3 text-slate-500 dark:text-slate-400 text-xs whitespace-nowrap">
                              {new Date(item.created_at).toLocaleDateString()} {new Date(item.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                            </td>
                            <td className="px-4 py-3 text-right text-slate-700 dark:text-slate-300 font-mono">{item.total_rows}</td>
                            <td className="px-4 py-3 text-right">
                              <span className={`font-mono ${item.quarantined_rows > 0 ? 'text-amber-600 dark:text-amber-400' : 'text-emerald-600 dark:text-emerald-400'}`}>
                                {item.quarantined_rows}
                              </span>
                            </td>
                            <td className="px-4 py-3 text-right text-slate-700 dark:text-slate-300 font-mono">{(item.total_co2_tonnes || 0).toFixed(2)}</td>
                            <td className="px-4 py-3 text-right font-bold text-slate-900 dark:text-white font-mono">€{(item.cbam_cost_eur || 0).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                            <td className="px-4 py-3 text-center">
                              <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${item.strict_mode ? 'bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400' : 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400'}`}>
                                {item.strict_mode ? 'Strict' : 'Normal'}
                              </span>
                            </td>
                            <td className="px-4 py-3 text-center">
                              <button 
                                onClick={(e) => deleteHistoryItem(e, item.id)}
                                className="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-lg transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100"
                                title="Delete analysis"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
              </div>
              )}
            </div>
          )}

          {activeTab !== "history" && (
          <div className="mt-8 flex justify-end">
            <button
              onClick={processBOM}
              disabled={(activeTab === "upload" && !file) || (activeTab === "manual" && (!manualMaterial || !manualWeight || (!manualCnCode && !manualSector))) || loading}
              className="px-8 py-3 bg-amber-600 hover:bg-amber-700 disabled:opacity-50 text-white rounded-2xl font-bold transition-colors flex items-center gap-2 shadow-lg shadow-amber-900/20"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Factory className="w-5 h-5" />}
              {loading ? "Analyzing..." : "Estimate CBAM Cost"}
            </button>
          </div>
          )}
        </div>

        {/* Live Preview Results */}
        {resultsData && (
          <div className="space-y-6" id="cbam-report">
            <div className="flex flex-col sm:flex-row print:flex-row justify-between items-start sm:items-center print:items-center gap-4 bg-slate-50 dark:bg-slate-900/50 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
              <div>
                <h2 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                  <FileText className="w-5 h-5 text-amber-500" />
                  CBAM Executive Summary
                </h2>
                <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                  Generated by MatDataHub CBAM Engine &bull; {generatedAt}
                </p>
                {historyNotSaved && (
                  <p className="print:hidden text-xs text-amber-600 dark:text-amber-400 mt-1">This run could not be saved to your history. Download the CSV if you need a record.</p>
                )}
              </div>
              <button
                onClick={generatePDF}
                className="print:hidden px-4 py-2.5 bg-slate-800 dark:bg-slate-700 hover:bg-slate-900 dark:hover:bg-slate-600 text-white rounded-xl text-sm font-semibold transition-colors flex items-center gap-2 shadow-sm"
              >
                <Download className="w-4 h-4" /> Download PDF Report
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 print:grid-cols-3 gap-4">
              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-2xl flex flex-col justify-center">
                <p className="text-slate-500 dark:text-slate-400 font-medium mb-1 flex items-center gap-2"><Factory className="w-4 h-4 text-emerald-600 dark:text-emerald-400" /> Total Embodied Carbon (Included)</p>
                <h3 className="text-3xl font-bold text-slate-900 dark:text-white font-heading">{(totalCO2/1000).toLocaleString(undefined, { maximumFractionDigits: 1 })} <span className="text-lg text-slate-500 dark:text-slate-400 font-normal">t CO₂</span></h3>
                <div className="text-xs text-slate-400 mt-2 font-medium space-y-1">
                  {fallbackTonnes > 0 && totalCO2 > 0 && (fallbackTonnes / (totalCO2/1000)) > 0.5 ? (
                    <p className="text-red-500 font-bold">⚠ {fallbackTonnes.toLocaleString(undefined, { maximumFractionDigits: 1 })} t ({Math.round(fallbackTonnes / (totalCO2/1000) * 100)}%) estimated with generic fallback factors, not Commission defaults. These figures should not be used for declarations.</p>
                  ) : fallbackTonnes > 0 ? (
                    <p className="text-amber-500">of which {fallbackTonnes.toLocaleString(undefined, { maximumFractionDigits: 1 })} t based on generic fallback defaults</p>
                  ) : null}
                  {interimStats.rows > 0 && (
                    <p className="text-slate-500 dark:text-slate-400">
                      Commission default values{defaultsSources.length > 0 ? ` (${defaultsSources.join("; ")})` : ""} used for {interimStats.rows} covered row{interimStats.rows === 1 ? "" : "s"}
                      ({interimStats.heading} matched at heading level, {interimStats.global} using the "other countries" values).
                    </p>
                  )}
                  {pendingReviewCount > 0 && (
                    <p className="text-amber-500">{pendingReviewTonnes.toLocaleString(undefined, { maximumFractionDigits: 1 })} t (material mass) in {pendingReviewCount} rows pending review</p>
                  )}
                </div>
              </div>

              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-2xl flex flex-col justify-center">
                <p className="text-slate-500 dark:text-slate-400 font-medium mb-1 flex items-center gap-2"><FileText className="w-4 h-4 text-blue-600 dark:text-blue-400" /> Embodied Carbon In Scope</p>
                <h3 className="text-3xl font-bold text-slate-900 dark:text-white font-heading">{taxableTonnes.toLocaleString(undefined, { maximumFractionDigits: 1 })} <span className="text-lg text-slate-500 dark:text-slate-400 font-normal">t CO₂</span></h3>
                <p className="text-xs text-slate-400 mt-2 font-medium">
                  {Math.max((totalCO2/1000) - taxableTonnes, 0).toLocaleString(undefined, { maximumFractionDigits: 1 })} t excluded (EU/EEA origin, non-EU destination, pre-2026 release, or de minimis)
                </p>
              </div>

              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-2xl flex flex-col justify-center">
                <div className="flex justify-between items-start mb-1">
                  <p className="text-slate-500 dark:text-slate-400 font-medium flex items-center gap-2"><FileText className="w-4 h-4 text-amber-600 dark:text-amber-400" /> Est. CBAM Tax Payable</p>
                  <select 
                    value={selectedYear} 
                    onChange={e => setSelectedYear(e.target.value as any)}
                    className="text-xs bg-slate-100 dark:bg-slate-800 border-none rounded p-1 font-bold text-slate-700 dark:text-slate-300 outline-none cursor-pointer max-w-[160px]"
                  >
                    <option value="ACTUAL">Actual Shipment Year</option>
                    <option disabled>──────────</option>
                    <option value="2034">What-if: 2034 (100%)</option>
                    <option value="2027">What-if: 2027 (~5%)</option>
                    <option value="2026">What-if: 2026 (~2.5%)</option>
                  </select>
                </div>
                <h3 className="text-3xl font-bold text-amber-500">€{estimatedTaxEUR.toLocaleString(undefined, { maximumFractionDigits: 2 })}</h3>
                  <div className="bg-amber-50 dark:bg-amber-900/20 px-2 py-1 rounded inline-block mt-1 border border-amber-100 dark:border-amber-800/50">
                    <p className="text-xs text-amber-700 dark:text-amber-400 font-medium">Ref 2034 (100%): €{eur(whatIfCost("2034"))}</p>
                  </div>
                <p className="text-xs text-slate-400 mt-2 font-medium">@ €{referencePrice}/tCO₂e (assumed reference price, not the Commission-published CBAM certificate price)</p>
                  <p className="text-xs text-amber-500 mt-1 font-semibold text-balance">
                    ⚠️ Warning (simplified lower estimate): The phase-in model assumes product emissions equal the free-allocation benchmark. Because default values typically exceed benchmarks, actual 2026-2027 costs using defaults will likely be substantially higher.
                  </p>
                {isDeMinimisExempt && (
                  <div className="mt-3 bg-emerald-50 dark:bg-emerald-900/20 p-2 rounded border border-emerald-100 dark:border-emerald-800">
                    <p className="text-xs text-emerald-600 dark:text-emerald-400 font-medium">
                      <span className="font-bold">De minimis assumed:</span> {eligibleMassTonnes.toLocaleString(undefined, { maximumFractionDigits: 1 })} t of goods belong to importer-years at or below the {deMinimisThreshold} t threshold and are shown as exempt
                      {costIfNotExempt > totalCbamCost ? ` (without the exemption: €${eur(costIfNotExempt)})` : ""}. Confirm the importer's full annual total before relying on this.
                    </p>
                  </div>
                )}
              </div>
            </div>

            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden print:overflow-visible">
              <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex justify-between items-center bg-slate-50 dark:bg-slate-950/50">
                <h3 className="font-bold text-slate-900 dark:text-white font-heading flex items-center gap-2"><Table className="w-5 h-5 text-amber-500" /> Results Breakdown</h3>
                <button onClick={downloadResults} className="print:hidden flex items-center gap-2 px-3 py-1.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-700 text-slate-900 dark:text-white text-xs font-bold rounded-2xl transition-colors border border-slate-200 dark:border-slate-700">
                  <Download className="w-3 h-3" /> Export to CSV
                </button>
              </div>
              <div className="overflow-x-auto print:overflow-visible">
                <table className="w-full text-left text-sm print:text-xs">
                  <thead className="bg-white dark:bg-slate-900">
                    <tr>
                      {Object.keys(resultsData[0] || {}).map((header) => {
                        const isDiagnostic = DIAGNOSTIC_COLUMNS.has(header);
                        return (
                          <th key={header} className={`p-4 print:p-2 text-slate-500 dark:text-slate-400 font-medium whitespace-nowrap print:whitespace-normal border-b border-slate-200 dark:border-slate-800 ${isDiagnostic ? 'print:hidden' : ''}`}>
                            {header.replace(/_/g, " ")}
                          </th>
                        );
                      })}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/50">
                    {resultsData.map((row, idx) => (
                      <tr key={idx} className="hover:bg-slate-100 dark:hover:bg-slate-800/30 transition-colors">
                        {Object.keys(row).map((header) => {
                          const isDiagnostic = DIAGNOSTIC_COLUMNS.has(header);
                          const val = row[header];
                          let display = val || "-";
                          
                          if (header === "ESG_Risk_Score" && val) {
                            const score = parseFloat(val);
                            const colorClass = score > 60 ? "bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400" : 
                                               score > 30 ? "bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400" : 
                                               "bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400";
                            display = <span className={`px-2.5 py-1 rounded-md text-xs font-bold ${colorClass}`}>{val}</span>;
                          } else if (header === "CBAM_Cost_EUR" && val && parseFloat(val) > 0) {
                            display = <span className="font-mono font-bold text-amber-600 dark:text-amber-500">€{parseFloat(val).toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>;
                          } else if (header === "Total_CO2_tonnes" && val && parseFloat(val) > 0) {
                            display = <span className="font-mono font-bold text-slate-700 dark:text-slate-300">{val} t</span>;
                          }
                          
                          return (
                            <td key={`${idx}-${header}`} className={`p-4 print:p-2 text-slate-600 dark:text-slate-300 whitespace-nowrap print:whitespace-normal print:break-words ${isDiagnostic ? 'print:hidden' : ''}`}>
                              {display}
                            </td>
                          );
                        })}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="hidden print:block border-t border-slate-300 pt-3 text-xs text-slate-700 space-y-1">
              <p className="font-bold">Estimate only. This is not a CBAM declaration and not advice from a customs broker or accredited verifier.</p>
              <p>Reference price assumed: €{referencePrice}/tCO₂e. Phase-in of the cost is simplified (assumes emissions close to the free-allocation benchmark), so actual costs using default values may be higher.</p>
              <p>Emission default values: {defaultsSources.length > 0 ? defaultsSources.join("; ") : "none used"}. De minimis shown as a possibility only; confirm the importer's annual total.</p>
              <p>Generated {generatedAt} by MatDataHub CBAM Engine.</p>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
