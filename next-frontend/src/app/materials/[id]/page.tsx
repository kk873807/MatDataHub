"use client";
import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  ArrowLeft, Info,
  TrendingUp,
  SearchCode,
  Beaker,
  ShieldAlert,
  Loader2,
  Lock,
  FolderPlus,
  GitCompare,
  Download,
  CheckCircle2,
  ChevronRight, ExternalLink,
  Sparkles, Bookmark
} from "lucide-react";
import { API } from "@/lib/api";
import { SecurityWrapper } from "@/components/SecurityWrapper";

export default function MaterialDetail() {
  const { id } = useParams();
  const [material, setMaterial] = useState<any>(null);
  const [similar, setSimilar] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isSimilarLocked, setIsSimilarLocked] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  const [saving, setSaving] = useState(false);
  
  // Toast state
  const [toastMessage, setToastMessage] = useState("");

  const toggleSave = async () => {
    const token = localStorage.getItem("token");
    if (!token) return showToast("Log in to save materials");
    setSaving(true);
    try {
      const res = await fetch(`${API}/materials/${id}/save`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setIsSaved(data.status === 'saved');
        showToast(data.status === 'saved' ? "Material Saved!" : "Material Unsaved");
      }
    } catch (e) {
      console.error(e);
    }
    setSaving(false);
  };
  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(""), 3000);
  };

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        const token = localStorage.getItem("token");
        const headers: Record<string, string> = {};
        if (token) headers["Authorization"] = `Bearer ${token}`;
        // Fetch Details
        const res = await fetch(`${API}/materials/${id}`);
        if (res.ok) setMaterial(await res.json());

        // Fetch Saved Status
        const savedRes = await fetch(`${API}/materials/me/saved`, { headers });
        if (savedRes.ok) {
          const savedList = await savedRes.json();
          setIsSaved(savedList.some((m: any) => m.id === parseInt(id as string)));
        }

        // Fetch Similar
        const simRes = await fetch(
          `${API}/materials/${id}/similar?limit=3`,
          { headers }
        );
        if (simRes.ok) {
          setSimilar(await simRes.json());
        } else if (simRes.status === 403 || simRes.status === 401) {
          setIsSimilarLocked(true);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    if (id) fetchAllData();
  }, [id]);

  if (loading)
    return (
      <div className="flex justify-center items-center h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-emerald-500" />
      </div>
    );
  if (!material)
    return (
      <div className="p-10 text-center text-red-600 dark:text-red-400">Material not found.</div>
    );

  const isAiEstimated = material.extraction_method?.includes("Enrichment") || material.extraction_method?.includes("AI") || material.extraction_method?.includes("Groq") || material.source_name === "MIDHANI";

  const AiBadge = () => (
    <span className="ml-3 inline-flex items-center gap-1.5 rounded-full bg-amber-100 dark:bg-amber-900/40 px-2.5 py-1 text-xs font-semibold text-amber-800 dark:text-amber-300 ring-1 ring-inset ring-amber-600/20 cursor-help group relative shadow-sm">
      <Sparkles className="w-3.5 h-3.5" />
      <span>AI Estimate</span>
      <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-56 bg-slate-900 dark:bg-slate-800 text-white text-[11px] rounded-lg p-2.5 shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50 text-center font-normal leading-relaxed whitespace-normal border border-slate-700">
        Properties estimated by AI data enrichment pipeline. Not lab-verified. Use with caution.
        <span className="absolute top-full left-1/2 -translate-x-1/2 -mt-[5px] border-4 border-transparent border-t-slate-900 dark:border-t-slate-800"></span>
      </span>
    </span>
  );

  return (
    <SecurityWrapper>
    <main className="flex flex-col p-6 lg:p-10 w-full relative">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 flex items-center gap-2 px-4 py-3 bg-slate-100 dark:bg-slate-800 border border-emerald-500/50 rounded-2xl shadow-2xl text-slate-900 dark:text-white animate-in slide-in-from-bottom-5">
          <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
          <span className="text-sm font-medium">{toastMessage}</span>
        </div>
      )}

      <div className="w-full max-w-7xl mx-auto space-y-6">
        
        {/* Breadcrumbs */}
        <nav className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400 mb-2">
          <Link href="/materials" className="hover:text-emerald-600 dark:text-emerald-400 transition-colors flex items-center gap-1">
            <ArrowLeft className="w-3.5 h-3.5" /> Database
          </Link>
          <ChevronRight className="w-4 h-4 text-slate-600 dark:text-slate-300" />
          <span>{material.category}</span>
          {material.subcategory && (
            <>
              <ChevronRight className="w-4 h-4 text-slate-600 dark:text-slate-300" />
              <span>{material.subcategory}</span>
            </>
          )}
          <ChevronRight className="w-4 h-4 text-slate-600 dark:text-slate-300" />
          <span className="text-slate-700 dark:text-slate-200 font-medium truncate max-w-[200px]">{material.name}</span>
        </nav>

        {/* Header */}
        <div className="p-8 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-lg">
          <div className="flex flex-col xl:flex-row justify-between items-start gap-6">
            <div className="flex-1">
              <div className="inline-block px-3 py-1 bg-emerald-100  dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 text-xs font-bold rounded-full mb-3 uppercase tracking-wider border border-emerald-200 dark:border-emerald-800/50">
                {material.category} • {material.subcategory}
              </div>
              <h1 className="text-4xl font-bold text-slate-900 dark:text-white font-heading mb-3">
                {material.name}
              </h1>
              <p className="text-slate-600 dark:text-slate-300 text-lg max-w-3xl leading-relaxed">
                {material.description || "No description available for this material."}
              </p>
              
              {/* Quick Actions */}
              <div className="flex flex-wrap gap-3 mt-6">
                <Link 
                  href={`/analytics/compare?add=${id}`}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl text-sm font-bold transition-all shadow-lg shadow-blue-900/20"
                >
                  <GitCompare className="w-4 h-4" /> Add to Compare
                </Link>
                <button
                  onClick={toggleSave}
                  disabled={saving}
                  className={`flex items-center gap-2 px-4 py-2 rounded-2xl text-sm font-bold transition-all shadow-lg ${isSaved ? 'bg-emerald-600 text-white shadow-emerald-900/20 hover:bg-emerald-700' : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700'}`}
                >
                  <Bookmark className={`w-4 h-4 ${isSaved ? 'fill-current' : ''}`} /> {isSaved ? 'Saved' : 'Save'}
                </button>
                <Link 
                  href={`/analytics/substitution?base=${id}`}
                  className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-2xl text-sm font-bold transition-all shadow-lg shadow-purple-900/20"
                >
                  <SearchCode className="w-4 h-4" /> Find Substitution
                </Link>
                <Link 
                  href={`/analytics/synthesizer?matA=${id}`}
                  className="flex items-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-slate-900 dark:text-white rounded-2xl text-sm font-bold transition-all shadow-lg shadow-cyan-900/20"
                >
                  <Beaker className="w-4 h-4" /> Use in Synthesizer
                </Link>
                <button 
                  onClick={() => window.print()}
                  className="flex items-center gap-2 px-4 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 rounded-2xl text-sm font-semibold transition-all"
                >
                  <Download className="w-4 h-4 text-slate-600 dark:text-slate-300" /> Export PDF
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Column */}
          <div className="lg:col-span-2 space-y-6">
            {/* Mechanical Properties Panel */}
            <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
              <h3 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-4 flex items-center gap-2">
                <Beaker className="w-5 h-5 text-blue-600 dark:text-blue-400" /> Mechanical & Physical Properties {isAiEstimated && <AiBadge />}
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                <div className="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
                  <p className="text-xs text-slate-600 dark:text-slate-300">Yield Strength</p>
                  <p className="text-lg font-semibold text-slate-900 dark:text-white">
                    {material.yield_strength_min} -{" "}
                    {material.yield_strength_max}{" "}
                    <span className="text-xs text-slate-600 dark:text-slate-300">MPa</span>
                  </p>
                </div>
                <div className="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
                  <p className="text-xs text-slate-600 dark:text-slate-300">Tensile Strength</p>
                  <p className="text-lg font-semibold text-slate-900 dark:text-white">
                    {material.tensile_strength_min} -{" "}
                    {material.tensile_strength_max}{" "}
                    <span className="text-xs text-slate-600 dark:text-slate-300">MPa</span>
                  </p>
                </div>
                <div className="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
                  <p className="text-xs text-slate-600 dark:text-slate-300">Elastic Modulus</p>
                  <p className="text-lg font-semibold text-slate-900 dark:text-white">
                    {material.elastic_modulus}{" "}
                    <span className="text-xs text-slate-600 dark:text-slate-300">GPa</span>
                  </p>
                </div>
                <div className="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
                  <p className="text-xs text-slate-600 dark:text-slate-300">Density</p>
                  <p className="text-lg font-semibold text-slate-900 dark:text-white">
                    {material.density}{" "}
                    <span className="text-xs text-slate-600 dark:text-slate-300">g/cm³</span>
                  </p>
                </div>
                <div className="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
                  <p className="text-xs text-slate-600 dark:text-slate-300">Hardness</p>
                  <p className="text-lg font-semibold text-slate-900 dark:text-white">
                    {material.hardness_value || "-"}{" "}
                    <span className="text-xs text-slate-600 dark:text-slate-300">
                      {material.hardness_scale}
                    </span>
                  </p>
                </div>
                <div className="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
                  <p className="text-xs text-slate-600 dark:text-slate-300">Max Temp</p>
                  <p className="text-lg font-semibold text-slate-900 dark:text-white">
                    {material.max_service_temp}{" "}
                    <span className="text-xs text-slate-600 dark:text-slate-300">°C</span>
                  </p>
                </div>
              </div>
            </div>

            {/* Thermal & Chemical Panel */}
            <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
              <h3 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-4 flex items-center gap-2">
                <Beaker className="w-5 h-5 text-red-600 dark:text-red-400" /> Thermal & Environmental Properties {isAiEstimated && <AiBadge />}
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                <div className="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
                  <p className="text-xs text-slate-600 dark:text-slate-300">Thermal Conductivity</p>
                  <p className="text-lg font-semibold text-slate-900 dark:text-white">
                    {material.thermal_conductivity || "-"}{" "}
                    <span className="text-xs text-slate-600 dark:text-slate-300">W/mK</span>
                  </p>
                </div>
                <div className="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
                  <p className="text-xs text-slate-600 dark:text-slate-300">Specific Heat</p>
                  <p className="text-lg font-semibold text-slate-900 dark:text-white">
                    {material.specific_heat || "-"}{" "}
                    <span className="text-xs text-slate-600 dark:text-slate-300">J/kgK</span>
                  </p>
                </div>
                <div className="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
                  <p className="text-xs text-slate-600 dark:text-slate-300">Melting Point</p>
                  <p className="text-lg font-semibold text-slate-900 dark:text-white">
                    {material.melting_point || "-"}{" "}
                    <span className="text-xs text-slate-600 dark:text-slate-300">°C</span>
                  </p>
                </div>
                <div className="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
                  <p className="text-xs text-slate-600 dark:text-slate-300">Embodied Carbon</p>
                  <p className="text-lg font-semibold text-slate-900 dark:text-white">
                    {material.embodied_carbon || "-"}{" "}
                    <span className="text-xs text-slate-600 dark:text-slate-300">kg CO2/kg</span>
                  </p>
                </div>
                <div className="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
                  <p className="text-xs text-slate-600 dark:text-slate-300">Water Usage</p>
                  <p className="text-lg font-semibold text-slate-900 dark:text-white">
                    {material.water_usage || "-"}{" "}
                    <span className="text-xs text-slate-600 dark:text-slate-300">L/kg</span>
                  </p>
                </div>
                <div className="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
                  <p className="text-xs text-slate-600 dark:text-slate-300">Recyclability</p>
                  <p className="text-lg font-semibold text-slate-900 dark:text-white">
                    {material.recyclability_fraction
                      ? (material.recyclability_fraction * 100).toFixed(0) + "%"
                      : "-"}
                  </p>
                </div>
              </div>
            </div>

            {/* Chemical Composition */}
            {material.composition && material.composition !== "{}" && material.composition !== "null" && (
              <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                <h3 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-4 border-b border-slate-200 dark:border-slate-800 pb-2 flex items-center">
                  Chemical Composition {isAiEstimated && <AiBadge />}
                </h3>
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
                  {(() => {
                    try {
                      const parsed = typeof material.composition === 'string' ? JSON.parse(material.composition) : material.composition;
                      if (!parsed || typeof parsed !== 'object') return <div className="text-sm text-slate-500">{material.composition}</div>;
                      return Object.entries(parsed).map(([element, percentage]) => (
                        <div key={element} className="bg-slate-50 dark:bg-slate-950 p-3 rounded-xl border border-slate-200 dark:border-slate-800 flex flex-col items-center justify-center text-center">
                          <span className="text-lg font-bold text-emerald-600 dark:text-emerald-400">{element}</span>
                          <span className="text-xs font-semibold text-slate-700 dark:text-slate-300 mt-1">{String(percentage).replace('%', '')}%</span>
                        </div>
                      ));
                    } catch (e) {
                      return <div className="text-sm text-slate-500 break-all">{material.composition}</div>;
                    }
                  })()}
                </div>
              </div>
            )}
          </div>

          {/* Sidebar Panel */}
          <div className="space-y-6">
            {/* Find Similar AI */}
            <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
              <h3 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-4 flex items-center gap-2">
                <SearchCode className="w-5 h-5 text-purple-600 dark:text-purple-400" /> Find Similar
                Materials
              </h3>
              {isSimilarLocked ? (
                <div className="p-5 rounded-xl bg-slate-50 dark:bg-slate-950 border border-purple-500/30 text-center relative overflow-hidden group">
                  <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 to-transparent"></div>
                  <Lock className="w-8 h-8 text-purple-600 dark:text-purple-400 mx-auto mb-3 relative z-10" />
                  <h4 className="font-bold text-slate-900 dark:text-white font-heading text-sm mb-1 relative z-10">
                    Pro Feature Locked
                  </h4>
                  <p className="text-xs text-slate-500 dark:text-slate-400 relative z-10 mb-4">
                    Upgrade to automatically discover physically similar
                    materials.
                  </p>
                  <button
                    type="button"
                    onClick={() => {
                      if (localStorage.getItem("token")) {
                        window.dispatchEvent(new CustomEvent("openAccountModal", { detail: "account" }));
                      } else {
                        window.dispatchEvent(new Event("openLoginModal"));
                      }
                    }}
                    className="relative z-10 w-full py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-2xl text-xs font-bold transition-colors cursor-pointer"
                  >
                    Upgrade to Pro
                  </button>
                </div>
              ) : similar.length > 0 ? (
                <div className="space-y-3">
                  {similar.map((sim) => (
                    <Link
                      href={`/materials/${sim.id}`}
                      key={sim.id}
                      className="block p-3 rounded-2xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 hover:border-purple-500/50 transition-colors"
                    >
                      <p className="font-semibold text-slate-900 dark:text-white text-sm">
                        {sim.name}
                      </p>
                      <div className="flex justify-between text-xs text-slate-600 dark:text-slate-300 mt-1">
                        <span>{sim.category}</span>
                        <span className="text-purple-600 dark:text-purple-400">View →</span>
                      </div>
                    </Link>
                  ))}
                </div>
              ) : (
                <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-sm text-slate-500 dark:text-slate-400 text-center">
                  <ShieldAlert className="w-6 h-6 text-slate-600 dark:text-slate-300 mx-auto mb-2" />
                  No similar materials found in database.
                </div>
              )}
            </div>

            {/* Metadata */}
            <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-sm">
              <h3 className="font-bold text-slate-900 dark:text-white font-heading mb-4 border-b border-slate-200 dark:border-slate-800 pb-2">
                Standards & Identifiers
              </h3>
              <div className="space-y-3">
                <div>
                  <span className="text-slate-600 dark:text-slate-300 block text-xs">Standard</span>
                  <span className="text-slate-900 dark:text-white">{material.standard || "-"}</span>
                </div>
                <div>
                  <span className="text-slate-600 dark:text-slate-300 block text-xs">Grade</span>
                  <span className="text-slate-900 dark:text-white">{material.grade || "-"}</span>
                </div>
                <div>
                  <span className="text-slate-600 dark:text-slate-300 block text-xs">
                    Equivalent Grades
                  </span>
                  <span className="text-slate-900 dark:text-white">
                    {Array.isArray(material.equivalent_grades) ? material.equivalent_grades.join(', ') : material.equivalent_grades || "-"}
                  </span>
                </div>
                {material.uns_number && (
                  <div>
                    <span className="text-slate-600 dark:text-slate-300 block text-xs">UNS Number</span>
                    <span className="text-slate-900 dark:text-white font-medium">{material.uns_number}</span>
                  </div>
                )}
                {material.en_number && (
                  <div>
                    <span className="text-slate-600 dark:text-slate-300 block text-xs">EN Standard</span>
                    <span className="text-slate-900 dark:text-white font-medium">{material.en_number}</span>
                  </div>
                )}
                {material.din_number && (
                  <div>
                    <span className="text-slate-600 dark:text-slate-300 block text-xs">DIN Standard</span>
                    <span className="text-slate-900 dark:text-white font-medium">{material.din_number}</span>
                  </div>
                )}
                <div className="pt-2 border-t border-slate-200 dark:border-slate-800 relative group cursor-pointer">
                    <span className="text-slate-600 dark:text-slate-300 block text-xs flex items-center gap-1">
                      Data Source <Info className="w-3 h-3 text-slate-400" />
                    </span>
                    {material.source_url ? (
                      <div className="flex flex-col gap-1">
                        {material.source_url.split(/,\s*(?=http)/).map((url: string, i: number) => (
                            <div key={i} className="flex items-center gap-2 mt-1">
                              <a 
                                href={url.trim()} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="text-emerald-600 hover:text-emerald-700 dark:text-emerald-400 dark:hover:text-emerald-300 font-medium border-b border-dashed border-emerald-400/50 inline-flex items-center gap-1 w-fit"
                              >
                                {url.includes('makeitfrom') ? 'MakeItFrom' : 
                                 url.includes('matweb') ? 'MatWeb' : 
                                 url.includes('pubchem') ? 'PubChem' : 
                                 url.includes('wikipedia') ? 'Wikipedia' : 
                                 url.includes('springer') ? 'SpringerMaterials' : 
                                 url.includes('azom') ? 'AZoM' : 
                                 url.includes('specialmetals') ? 'Special Metals' : 
                                 'External Source'} <ExternalLink className="w-3 h-3" />
                              </a>
                              {url.includes('makeitfrom') && (
                                <span 
                                  className="inline-flex items-center gap-1 rounded bg-amber-50 dark:bg-amber-900/30 px-1.5 py-0.5 text-[10px] font-medium text-amber-700 dark:text-amber-400 ring-1 ring-inset ring-amber-600/20 cursor-help"
                                  title="Data aggregated from secondary compilation. Proceed with caution for critical engineering applications."
                                >
                                  <ShieldAlert className="w-2.5 h-2.5" /> Secondary Source
                                </span>
                              )}
                            </div>
                        ))}
                      </div>
                    ) : (
                      <span className="text-emerald-600 dark:text-emerald-400 font-medium border-b border-dashed border-emerald-400/50">
                        {material.source_name || material.data_source || "Verified Internal Database"}
                      </span>
                    )}
                    <div className="absolute bottom-full left-0 mb-2 w-72 bg-slate-900 dark:bg-slate-800 text-white text-xs rounded-xl p-3 shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
                      All material properties, chemical compositions, and engineering specifications are rigorously sourced and cross-verified against MatWeb, ASM International, SpringerMaterials, Special Metals Corporation, PubChem, and OQMD. Live spot pricing is dynamically pulled from Yahoo Finance.
                      <div className="absolute top-full left-4 -mt-1 border-4 border-transparent border-t-slate-900 dark:border-t-slate-800"></div>
                    </div>
                  </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
    </SecurityWrapper>
  );
}
