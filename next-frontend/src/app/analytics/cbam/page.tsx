"use client";
import { useState, useRef } from "react";
import Link from "next/link";
import { ArrowLeft, Factory, UploadCloud, Loader2, FileSpreadsheet, Lock } from "lucide-react";

export default function CBAMAnalytics() {
  const [file, setFile] = useState<File | null>(null);
  const [materialCol, setMaterialCol] = useState("Material");
  const [weightCol, setWeightCol] = useState("Weight_kg");
  const [loading, setLoading] = useState(false);
  const [isLocked, setIsLocked] = useState(true); // Default to locked for Enterprise
  const fileInputRef = useRef<HTMLInputElement>(null);

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

  const processBOM = async () => {
    if (!file) return;
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("material_col", materialCol);
      formData.append("weight_col", weightCol);

      const res = await fetch("http://127.0.0.1:8000/api/v1/materials/bom_analyze", {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        // Handle CSV Download
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "enriched_bom_cbam.csv";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
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

  if (isLocked) {
    return (
      <main className="flex flex-col p-6 lg:p-10 w-full h-full">
        <div className="w-full max-w-5xl mx-auto space-y-6">
          <Link href="/analytics" className="inline-flex items-center gap-2 text-slate-400 hover:text-white transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back to Analytics
          </Link>
          
          <div className="p-10 mt-10 rounded-3xl bg-slate-900 border border-amber-500/30 text-center relative overflow-hidden flex flex-col items-center justify-center">
            <div className="absolute inset-0 bg-gradient-to-br from-amber-900/20 to-transparent"></div>
            <div className="w-20 h-20 bg-amber-950 rounded-full flex items-center justify-center mb-6 relative z-10 border border-amber-500/50 shadow-[0_0_30px_rgba(245,158,11,0.2)]">
              <Lock className="w-10 h-10 text-amber-500" />
            </div>
            
            <h2 className="text-3xl font-bold text-white mb-4 relative z-10">Enterprise Feature</h2>
            <p className="text-slate-300 relative z-10 max-w-2xl mx-auto mb-8 text-lg">
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

  // If unlocked (which is false by default above per user request for "CBAM(ENT)"):
  return (
    <main className="flex flex-col p-6 lg:p-10 w-full h-full overflow-y-auto">
      <div className="w-full max-w-4xl mx-auto space-y-8">
        
        <Link href="/analytics" className="inline-flex items-center gap-2 text-slate-400 hover:text-white transition-colors">
          <ArrowLeft className="w-4 h-4" /> Back to Analytics
        </Link>

        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            <Factory className="w-8 h-8 text-amber-500" />
            Supply Chain Risk & CBAM Analyzer
          </h1>
          <p className="text-slate-300 mt-2">Upload your Bill of Materials to calculate ESG impact and flag obsolescence risks.</p>
        </div>

        <div className="bg-slate-900 p-8 rounded-2xl border border-slate-800">
          
          <div className="grid grid-cols-2 gap-6 mb-8">
            <div>
              <label className="block text-sm font-semibold text-slate-300 mb-2">Material Column Header</label>
              <input
                type="text"
                value={materialCol}
                onChange={e => setMaterialCol(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 text-white outline-none focus:border-amber-500"
                placeholder="e.g. Material"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-300 mb-2">Weight Column Header (kg)</label>
              <input
                type="text"
                value={weightCol}
                onChange={e => setWeightCol(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 text-white outline-none focus:border-amber-500"
                placeholder="e.g. Weight_kg"
              />
            </div>
          </div>

          <div 
            onDragOver={e => e.preventDefault()}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-colors ${file ? 'border-amber-500 bg-amber-900/10' : 'border-slate-700 hover:border-slate-500 hover:bg-slate-800/50'}`}
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
                <p className="font-bold text-white">{file.name}</p>
                <p className="text-sm text-slate-400 mt-1">Ready to process</p>
              </div>
            ) : (
              <div className="flex flex-col items-center">
                <UploadCloud className="w-12 h-12 text-slate-500 mb-3" />
                <p className="font-bold text-white text-lg">Click or drag BOM CSV file here</p>
                <p className="text-sm text-slate-400 mt-1">Must contain material and weight columns</p>
              </div>
            )}
          </div>

          <div className="mt-8 flex justify-end">
            <button
              onClick={processBOM}
              disabled={!file || loading}
              className="px-8 py-3 bg-amber-600 hover:bg-amber-700 disabled:opacity-50 text-white rounded-lg font-bold transition-colors flex items-center gap-2"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Factory className="w-5 h-5" />}
              {loading ? "Analyzing Supply Chain..." : "Run CBAM Analysis"}
            </button>
          </div>

        </div>
      </div>
    </main>
  );
}
