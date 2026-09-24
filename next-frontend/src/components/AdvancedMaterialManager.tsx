"use client";
import { useState, useRef, useEffect } from "react";
import { Database, Loader2, CheckCircle2, Mail, Info } from "lucide-react";
import { API } from "@/lib/api";

export default function AdvancedMaterialManager() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const [myMaterials, setMyMaterials] = useState<any[]>([]);
  const [fetchingMaterials, setFetchingMaterials] = useState(false);

  const fetchMyMaterials = async () => {
    setFetchingMaterials(true);
    try {
      const res = await fetch(`${API}/materials/custom/mine`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
      });
      if (res.ok) {
        const data = await res.json();
        setMyMaterials(data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setFetchingMaterials(false);
    }
  };

  useEffect(() => {
    fetchMyMaterials();
  }, []);


  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden shadow-xl mt-8">
      <div className="p-6 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50 dark:bg-slate-950/50">
        <div className="flex items-center gap-3">
          <Database className="w-5 h-5 text-cyan-400" />
          <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading">Database Management (Materials)</h2>
        </div>
      </div>
      <div className="p-6">
        
        {/* Bulk Upload Notice */}
        <div className="mb-8 bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-800/50 rounded-xl p-4 flex items-start gap-3">
          <Info className="w-5 h-5 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
          <div>
            <h3 className="text-indigo-900 dark:text-indigo-300 font-semibold text-sm">Want to add materials in bulk?</h3>
            <p className="text-indigo-700 dark:text-indigo-400 text-xs mt-1 leading-relaxed">
              To ensure data integrity, bulk uploading is handled by our team. If you have a large dataset, please contact us at <a href="mailto:matdatahub.support@gmail.com" className="font-bold underline hover:text-indigo-800 dark:hover:text-indigo-300">matdatahub.support@gmail.com</a>. 
              Attach your CSV/Excel file along with authentic primary sources (PDFs, source links, or spec sheets) for verification.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Left Column: Form */}
          <div className="lg:col-span-2">
            <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-slate-900 dark:text-white font-heading mb-4 flex items-center gap-2">
                <Database className="w-5 h-5 text-slate-500 dark:text-slate-400" /> Add Single Material
              </h3>
          <form onSubmit={async (e) => {
            e.preventDefault();
            setLoading(true); setMessage(""); setError("");
            const formData = new FormData(e.currentTarget);
            const mat: any = {};
            formData.forEach((value, key) => {
              if (value) mat[key] = isNaN(Number(value)) || key === "name" || key === "category" || key === "subcategory" || key === "description" || key === "standard" || key === "grade" || key === "source_url" ? value : Number(value);
            });
            try {
              const res = await fetch(`${API}/materials/custom`, {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  "Authorization": `Bearer ${localStorage.getItem("token")}`,
                },
                body: JSON.stringify(mat),
              });
              if (!res.ok) {
                const errData = await res.json();
                let errMsg = "Failed to upload material";
                if (errData.detail) {
                  if (typeof errData.detail === "string") {
                    errMsg = errData.detail;
                  } else if (Array.isArray(errData.detail)) {
                    errMsg = errData.detail.map((e: any) => `${e.loc[e.loc.length-1]}: ${e.msg}`).join(", ");
                  }
                }
                throw new Error(errMsg);
              }
              setMessage(`Successfully added ${mat.name}`);
              (e.target as HTMLFormElement).reset();
              fetchMyMaterials();
            } catch (err: any) {
              setError(`Upload Error: ${err.message}`);
            } finally {
              setLoading(false);
            }
          }}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <input type="text" name="name" placeholder="Name (Required)" required className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="text" name="category" placeholder="Category (Required)" required className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="url" name="source_url" placeholder="Source URL (Required)" required className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="text" name="subcategory" placeholder="Subcategory" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="text" name="grade" placeholder="Grade" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="number" step="any" name="yield_strength_min" placeholder="Yield Strength (Min)" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="number" step="any" name="tensile_strength_min" placeholder="Tensile Strength (Min)" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="number" step="any" name="elastic_modulus" placeholder="Elastic Modulus" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="number" step="any" name="density" placeholder="Density" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
              <input type="number" step="any" name="cost_per_kg_min" placeholder="Cost / kg (Min)" className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white" />
            </div>
            <textarea name="description" placeholder="Description" className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded px-3 py-2 text-slate-900 dark:text-white mb-4"></textarea>
            <button disabled={loading} type="submit" className="bg-cyan-600 hover:bg-cyan-500 text-slate-900 dark:text-white font-semibold py-2 px-6 rounded-2xl transition-colors">
              {loading ? "Adding..." : "Add Material"}
            </button>
          </form>
            </div>
          </div>
          
          {/* Right Column: Contributions */}
          <div className="lg:col-span-1">
            <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl p-6 h-full flex flex-col">
              <h3 className="text-lg font-semibold text-slate-900 dark:text-white font-heading mb-4 flex items-center justify-between">
                <span>Your Contributions</span>
                <span className="text-sm bg-cyan-100 text-cyan-700 dark:bg-cyan-900/30 dark:text-cyan-400 px-2 py-1 rounded-full">{myMaterials.length}</span>
              </h3>
              
              {fetchingMaterials ? (
                <div className="flex-1 flex items-center justify-center">
                  <Loader2 className="w-6 h-6 animate-spin text-slate-400" />
                </div>
              ) : myMaterials.length === 0 ? (
                <div className="flex-1 flex flex-col items-center justify-center text-slate-500 dark:text-slate-400 text-center py-10">
                  <Database className="w-8 h-8 mb-3 opacity-50" />
                  <p className="text-sm">No materials added yet.</p>
                </div>
              ) : (
                <ul className="flex-1 overflow-y-auto space-y-3 max-h-[400px] pr-2 custom-scrollbar">
                  {myMaterials.map((m: any, i) => (
                    <li key={m.id || i} className={`bg-white dark:bg-slate-900 border rounded-lg p-3 shadow-sm hover:shadow-md transition-shadow ${m.status === 'approved' ? 'border-emerald-200 dark:border-emerald-800/50' : m.status === 'rejected' ? 'border-red-200 dark:border-red-800/50' : 'border-slate-200 dark:border-slate-800'}`}>
                      <div className="flex justify-between items-start">
                        <p className="font-semibold text-sm text-slate-900 dark:text-white line-clamp-1">{m.name}</p>
                        <span className={`text-[9px] uppercase font-bold px-1.5 py-0.5 rounded ${m.status === 'approved' ? 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400' : m.status === 'rejected' ? 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400' : 'bg-amber-100 text-amber-600 dark:bg-amber-900/30 dark:text-amber-400'}`}>
                          {m.status || 'pending'}
                        </span>
                      </div>
                      <div className="flex justify-between items-center mt-2">
                        <span className="text-xs font-medium text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded">{m.category}</span>
                        <span className="text-[10px] text-slate-400 dark:text-slate-500">{m.created_at ? new Date(m.created_at).toLocaleDateString() : ''}</span>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
          
        </div>
        
      </div>
    </div>
  );
}
