"use client";
import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { ArrowLeft, Factory, UploadCloud, Loader2, FileSpreadsheet, Lock, Download, FileText, Table, AlertTriangle } from "lucide-react";
import { useRouter } from "next/navigation";
import { API } from "@/lib/api";
import Papa from "papaparse";

export default function CBAMAnalytics() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<"upload" | "manual">("upload");
  const [file, setFile] = useState<File | null>(null);
  
  // CSV Configuration
  const [materialCol, setMaterialCol] = useState("Material");
  const [weightCol, setWeightCol] = useState("Weight_kg");
  const [strictMode, setStrictMode] = useState(false);
  
  // Manual Entry State
  const [manualMaterial, setManualMaterial] = useState("");
  const [manualWeight, setManualWeight] = useState("");

  // Results state
  const [loading, setLoading] = useState(false);
  const [isLocked, setIsLocked] = useState(true);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const [resultsData, setResultsData] = useState<any[] | null>(null);
  const [totalCO2, setTotalCO2] = useState(0);
  const [totalCbamCost, setTotalCbamCost] = useState(0);
  const [selectedYear, setSelectedYear] = useState<"2034" | "2027" | "2026">("2034");
  const [pendingReviewCount, setPendingReviewCount] = useState(0);
  const [pendingReviewTonnes, setPendingReviewTonnes] = useState(0);
  const [fallbackTonnes, setFallbackTonnes] = useState(0);
  const [taxableTonnes, setTaxableTonnes] = useState(0);
  const [deMinimisThreshold, setDeMinimisThreshold] = useState(50);
  const [isDeMinimisExempt, setIsDeMinimisExempt] = useState(false);
  const [eligibleMassTonnes, setEligibleMassTonnes] = useState(0);
  
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
    automotive: `material_id,Material,Weight_kg,cbam_sector,cn_code,country_of_origin,destination,shipment_date,supplier
MAT-A1,Hot-Rolled Steel Coil,50000,Iron & Steel,7208 51 00,China,Germany,2026-06-15,Acme Metals
MAT-A2,Aluminium Engine Block,15000,Aluminium,7601 20 00,India,Germany,2026-06-15,Global Alum
MAT-A3,Plastic Dashboard,5000,,,Vietnam,Germany,2026-06-15,PolyCorp
MAT-A4,Stainless Steel Fasteners,2000,Iron & Steel,7318 15 00,Taiwan,Germany,2026-06-15,FastenTech`,
    construction: `material_id,Material,Weight_kg,cbam_sector,cn_code,country_of_origin,destination,shipment_date,supplier
MAT-C1,Portland Cement,200000,Cement,2523 29 00,Turkey,France,2026-08-01,EuroCement
MAT-C2,Steel Rebar,100000,Iron & Steel,7214 20 00,China,France,2026-08-01,SteelCo
MAT-C3,Aluminium Window Frames,10000,Aluminium,7610 10 00,China,France,2026-08-01,AlumBuild
MAT-C4,Glass Panes,5000,,,India,France,2026-08-01,ClearGlass`
  };

  const handleLoadDemo = (type: "automotive" | "construction") => {
    const csvStr = DEMO_BOMS[type];
    const demoFile = new File([csvStr], `${type}_bom_demo.csv`, { type: "text/csv" });
    setFile(demoFile);
    processBOM(demoFile, "Material", "Weight_kg");
  };

  const downloadTemplate = () => {
    const csvContent = "Material,Weight_kg\nSteel 304L,100\nAluminum 6061,50\n";
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "cbam_template.csv";
    a.click();
    URL.revokeObjectURL(url);
  };

  const generatePDF = async () => {
    try {
      // @ts-ignore
      const html2pdf = (await import('html2pdf.js')).default;
      const element = document.getElementById('cbam-report');
      if (!element) return;
      
      const opt = {
        margin: 0.5,
        filename: 'CBAM_Executive_Report.pdf',
        image: { type: 'jpeg' as const, quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'in', format: 'a4', orientation: 'landscape' as const }
      };
      
      html2pdf().set(opt).from(element).save();
    } catch (error) {
      console.error("PDF generation failed", error);
      alert("Failed to generate PDF. Make sure you are in a modern browser.");
    }
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
      // Generate virtual CSV with proper quoting to handle commas in material names
      const escapedMaterial = manualMaterial.includes(",") ? `"${manualMaterial.replace(/"/g, '""')}"` : manualMaterial;
      const csvContent = `Material,Weight_kg\n${escapedMaterial},${manualWeight}\n`;
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
      formData.append("strict_mode", strictMode.toString());

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
        
        let total = 0; // Total physical kg included
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
            if (rowObj["Parsed_Weight_kg"]) {
                revTonnes += parseFloat(rowObj["Parsed_Weight_kg"] || "0") / 1000.0;
            }
          }
        });
        
        const elMassTonnes = eligibleMassKg / 1000.0;
        const isExempt = elMassTonnes <= 50 && elMassTonnes > 0;
        // Tax is now fully processed by the backend per-row, so totalCbamEur is inherently correct
        const activeTaxEur = totalCbamEur;
        
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
        setEligibleMassTonnes(elMassTonnes);
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
        <div className="w-full max-w-5xl mx-auto space-y-6">
          <Link href="/analytics" className="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back to Analytics
          </Link>
          
          <div className="p-10 mt-10 rounded-3xl bg-white dark:bg-slate-900 border border-amber-500/30 text-center relative overflow-hidden flex flex-col items-center justify-center">
            <div className="absolute inset-0 bg-gradient-to-br from-amber-900/20 to-transparent"></div>
            <div className="w-20 h-20 bg-amber-950 rounded-full flex items-center justify-center mb-6 relative z-10 border border-amber-500/50 shadow-[0_0_30px_rgba(245,158,11,0.2)]">
              <Lock className="w-10 h-10 text-amber-500" />
            </div>
            
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white font-heading mb-4 relative z-10">Enterprise Feature</h2>
            <p className="text-slate-600 dark:text-slate-300 relative z-10 max-w-2xl mx-auto mb-8 text-lg">
              Supply Chain Risk & CBAM (Carbon Border Adjustment Mechanism) modeling requires a dedicated Enterprise environment. 
              Automatically scan bulk Bills of Materials (BOMs) for embargoed materials, geographic obsolescence, and carbon taxation thresholds.
            </p>
            
            <button className="relative z-10 px-8 py-4 bg-amber-600 hover:bg-amber-700 text-white rounded-xl font-bold transition-all shadow-lg shadow-amber-900/50 hover:scale-105">
              Contact Sales to Unlock
            </button>
          </div>
        </div>
      </main>
    );
  }

  // CBAM cost now comes from backend (€75/tCO2e reference price)
  const phaseInFactor = selectedYear === "2026" ? 0.025 : selectedYear === "2027" ? 0.05 : 1.0;
  const estimatedTaxEUR = totalCbamCost * phaseInFactor;

  return (
    <main className="flex flex-col p-6 lg:p-10 w-full h-full overflow-y-auto">
      <div className="w-full max-w-5xl mx-auto space-y-8">
        
        <Link href="/analytics" className="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white transition-colors">
          <ArrowLeft className="w-4 h-4" /> Back to Analytics
        </Link>

        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white font-heading flex items-center gap-3">
            <Factory className="w-8 h-8 text-amber-500" />
            CBAM Calculator & ESG Analyzer
          </h1>
          <p className="text-slate-600 dark:text-slate-300 mt-2">Upload your Bill of Materials or enter manually to calculate ESG impact and carbon tax estimates.</p>
          
          <div className="mt-4 p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg flex items-start gap-3 text-amber-800 dark:text-amber-200 text-sm max-w-4xl">
            <AlertTriangle className="w-5 h-5 shrink-0 mt-0.5" />
            <div>
              <strong>For Planning & Estimation Only</strong><br/>
              This tool is not a substitute for professional compliance advice. Calculations, scope mappings, and default emission values may not perfectly reflect final EU Customs determinations or your specific regulatory obligations.
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 p-8 rounded-2xl border border-slate-200 dark:border-slate-800">
          
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
              className={`px-4 py-2 font-bold rounded-2xl transition-colors ${activeTab === "manual" ? "bg-amber-100 dark:bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400" : "text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white"}`}
            >
              Manual Entry
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
              <div className="flex items-center pt-2">
                <label className="flex items-center gap-3 cursor-pointer group">
                  <div className={`w-11 h-6 flex items-center rounded-full p-1 transition-colors ${strictMode ? 'bg-amber-500' : 'bg-slate-300 dark:bg-slate-700'}`}>
                    <div className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform ${strictMode ? 'translate-x-5' : ''}`}></div>
                  </div>
                  <input type="checkbox" className="hidden" checked={strictMode} onChange={e => setStrictMode(e.target.checked)} />
                  <span className="text-sm font-semibold text-slate-700 dark:text-slate-300 group-hover:text-amber-600 transition-colors">Strict Compliance Mode (Disable De Minimis Exemption, Hard Quarantine on Missing Compliance Data)</span>
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
                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Must contain material and weight columns</p>
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
            </div>
          )}

          <div className="mt-8 flex justify-end">
            <button
              onClick={processBOM}
              disabled={(activeTab === "upload" && !file) || (activeTab === "manual" && (!manualMaterial || !manualWeight)) || loading}
              className="px-8 py-3 bg-amber-600 hover:bg-amber-700 disabled:opacity-50 text-white rounded-2xl font-bold transition-colors flex items-center gap-2 shadow-lg shadow-amber-900/20"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Factory className="w-5 h-5" />}
              {loading ? "Analyzing..." : "Calculate CBAM & ESG"}
            </button>
          </div>
        </div>

        {/* Live Preview Results */}
        {resultsData && (
          <div className="space-y-6" id="cbam-report">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-50 dark:bg-slate-900/50 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
              <div>
                <h2 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                  <FileText className="w-5 h-5 text-amber-500" />
                  CBAM Executive Summary
                </h2>
                <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Generated by MatDataHub CBAM Engine</p>
              </div>
              <button
                onClick={generatePDF}
                className="px-4 py-2.5 bg-slate-800 dark:bg-slate-700 hover:bg-slate-900 dark:hover:bg-slate-600 text-white rounded-xl text-sm font-semibold transition-colors flex items-center gap-2 shadow-sm"
              >
                <Download className="w-4 h-4" /> Download PDF Report
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-2xl flex flex-col justify-center">
                <p className="text-slate-500 dark:text-slate-400 font-medium mb-1 flex items-center gap-2"><Factory className="w-4 h-4 text-emerald-600 dark:text-emerald-400" /> Total Embodied Carbon (Included)</p>
                <h3 className="text-3xl font-bold text-slate-900 dark:text-white font-heading">{(totalCO2/1000).toLocaleString(undefined, { maximumFractionDigits: 1 })} <span className="text-lg text-slate-500 dark:text-slate-400 font-normal">t CO₂</span></h3>
                <div className="text-xs text-slate-400 mt-2 font-medium space-y-1">
                  <p>of which {fallbackTonnes.toLocaleString(undefined, { maximumFractionDigits: 1 })} t based on fallback defaults</p>
                  {pendingReviewCount > 0 && (
                    <p className="text-amber-500">{pendingReviewTonnes.toLocaleString(undefined, { maximumFractionDigits: 1 })} t (material mass) in {pendingReviewCount} rows pending review</p>
                  )}
                </div>
              </div>

              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-2xl flex flex-col justify-center">
                <p className="text-slate-500 dark:text-slate-400 font-medium mb-1 flex items-center gap-2"><FileText className="w-4 h-4 text-blue-600 dark:text-blue-400" /> Taxable Carbon Base</p>
                <h3 className="text-3xl font-bold text-slate-900 dark:text-white font-heading">{taxableTonnes.toLocaleString(undefined, { maximumFractionDigits: 1 })} <span className="text-lg text-slate-500 dark:text-slate-400 font-normal">t CO₂</span></h3>
                <p className="text-xs text-slate-400 mt-2 font-medium">
                  {((totalCO2/1000) - taxableTonnes).toLocaleString(undefined, { maximumFractionDigits: 1 })} t-equivalent excluded (exempt origin/dest, pre-2026, or carbon price paid)
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
                    <option value="2034">If imported in 2034 (100%)</option>
                    <option value="2027">If imported in 2027 (~5%)</option>
                    <option value="2026">If imported in 2026 (~2.5%)</option>
                  </select>
                </div>
                <h3 className="text-3xl font-bold text-amber-500">€{estimatedTaxEUR.toLocaleString(undefined, { maximumFractionDigits: 2 })}</h3>
                <p className="text-xs text-slate-400 mt-2 font-medium">@ €75/tCO₂e · assumes emissions near benchmark</p>
                {isDeMinimisExempt && (
                  <div className="mt-3 bg-emerald-50 dark:bg-emerald-900/20 p-2 rounded border border-emerald-100 dark:border-emerald-800">
                    <p className="text-xs text-emerald-600 dark:text-emerald-400 font-medium">
                      <span className="font-bold">De Minimis Applied:</span> {eligibleMassTonnes.toLocaleString(undefined, { maximumFractionDigits: 1 })} t of eligible goods excluded (≤ {deMinimisThreshold} t limit).
                    </p>
                  </div>
                )}
              </div>
            </div>

            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden">
              <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex justify-between items-center bg-slate-50 dark:bg-slate-950/50">
                <h3 className="font-bold text-slate-900 dark:text-white font-heading flex items-center gap-2"><Table className="w-5 h-5 text-amber-500" /> Results Breakdown</h3>
                <button onClick={downloadResults} className="flex items-center gap-2 px-3 py-1.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-700 text-slate-900 dark:text-white text-xs font-bold rounded-2xl transition-colors border border-slate-200 dark:border-slate-700">
                  <Download className="w-3 h-3" /> Export to CSV
                </button>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-white dark:bg-slate-900">
                    <tr>
                      {Object.keys(resultsData[0] || {}).map((header) => (
                        <th key={header} className="p-4 text-slate-500 dark:text-slate-400 font-medium whitespace-nowrap border-b border-slate-200 dark:border-slate-800">{header.replace(/_/g, " ")}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/50">
                    {resultsData.map((row, idx) => (
                      <tr key={idx} className="hover:bg-slate-100 dark:hover:bg-slate-800/30 transition-colors">
                        {Object.keys(row).map((header) => {
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
                            <td key={`${idx}-${header}`} className="p-4 text-slate-600 dark:text-slate-300 whitespace-nowrap">
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
          </div>
        )}
      </div>
    </main>
  );
}
