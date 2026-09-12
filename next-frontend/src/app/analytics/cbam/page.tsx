"use client";
import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { ArrowLeft, Factory, UploadCloud, Loader2, FileSpreadsheet, Lock, Download, FileText, Table } from "lucide-react";
import { useRouter } from "next/navigation";
import { API } from "@/lib/api";

export default function CBAMAnalytics() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<"upload" | "manual">("upload");
  const [file, setFile] = useState<File | null>(null);
  
  // CSV Configuration
  const [materialCol, setMaterialCol] = useState("Material");
  const [weightCol, setWeightCol] = useState("Weight_kg");
  
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

  const processBOM = async () => {
    let payloadFile = file;
    let payloadMatCol = materialCol;
    let payloadWeightCol = weightCol;

    if (activeTab === "manual") {
      if (!manualMaterial || !manualWeight) {
        alert("Please enter both material and weight.");
        return;
      }
      // Generate virtual CSV
      const csvContent = `Material,Weight_kg\n${manualMaterial},${manualWeight}\n`;
      payloadFile = new File([csvContent], "manual_entry.csv", { type: "text/csv" });
      payloadMatCol = "Material";
      payloadWeightCol = "Weight_kg";
    } else {
      if (!file) return;
    }

    setLoading(true);
    setResultsData(null);
    setTotalCO2(0);

    try {
      const formData = new FormData();
      formData.append("file", payloadFile as File);
      formData.append("material_col", payloadMatCol);
      formData.append("weight_col", payloadWeightCol);

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
        // Parse CSV text for live preview
        const rows = text.trim().split("\n");
        const headersArr = rows[0].split(",").map(h => h.trim());
        
        let total = 0;
        let totalCbamEur = 0;
        const parsedData = rows.slice(1).map(row => {
          const values = row.split(",");
          const rowObj: any = {};
          headersArr.forEach((header, index) => {
            rowObj[header] = values[index];
            if (header === "Total_CO2_kg") {
              total += parseFloat(values[index] || "0");
            }
            if (header === "CBAM_Cost_EUR") {
              totalCbamEur += parseFloat(values[index] || "0");
            }
          });
          return rowObj;
        });

        setResultsData(parsedData);
        setTotalCO2(total);
        setTotalCbamCost(totalCbamEur);
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
    const headers = Object.keys(resultsData[0]);
    const csvContent = [
      headers.join(","),
      ...resultsData.map(row => headers.map(h => row[h]).join(","))
    ].join("\n");
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
  const estimatedTaxEUR = totalCbamCost;

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
        </div>

        <div className="bg-white dark:bg-slate-900 p-8 rounded-2xl border border-slate-200 dark:border-slate-800">
          
          {/* Tabs */}
          <div className="flex gap-4 mb-6 border-b border-slate-200 dark:border-slate-800 pb-4">
            <button
              onClick={() => setActiveTab("upload")}
              className={`px-4 py-2 font-bold rounded-2xl transition-colors ${activeTab === "upload" ? "bg-amber-900/30 text-amber-400" : "text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white"}`}
            >
              Upload CSV
            </button>
            <button
              onClick={() => setActiveTab("manual")}
              className={`px-4 py-2 font-bold rounded-2xl transition-colors ${activeTab === "manual" ? "bg-amber-900/30 text-amber-400" : "text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white"}`}
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
                <button onClick={downloadTemplate} className="text-amber-500 hover:text-amber-400 text-sm font-medium flex items-center gap-1">
                  <Download className="w-4 h-4" /> Template
                </button>
              </div>

              <div 
                onDragOver={e => e.preventDefault()}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-colors ${file ? 'border-amber-500 bg-amber-900/10' : 'border-slate-200 dark:border-slate-700 hover:border-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800/50'}`}
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
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-2xl flex flex-col justify-center">
                <p className="text-slate-500 dark:text-slate-400 font-medium mb-1 flex items-center gap-2"><Factory className="w-4 h-4 text-emerald-400" /> Total Embodied Carbon</p>
                <h3 className="text-3xl font-bold text-slate-900 dark:text-white font-heading">{totalCO2.toLocaleString(undefined, { maximumFractionDigits: 2 })} <span className="text-lg text-slate-500 dark:text-slate-400 font-normal">kg CO₂</span></h3>
              </div>
              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 rounded-2xl flex flex-col justify-center">
                <p className="text-slate-500 dark:text-slate-400 font-medium mb-1 flex items-center gap-2"><FileText className="w-4 h-4 text-amber-400" /> Est. CBAM Tax Obligation</p>
                <h3 className="text-3xl font-bold text-amber-500">€{estimatedTaxEUR.toLocaleString(undefined, { maximumFractionDigits: 2 })} <span className="text-lg text-slate-500 dark:text-slate-400 font-normal">(@ €75/tCO₂e)</span></h3>
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
                        {Object.keys(row).map((header) => (
                          <td key={`${idx}-${header}`} className="p-4 text-slate-600 dark:text-slate-300 whitespace-nowrap">
                            {row[header] || "-"}
                          </td>
                        ))}
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
