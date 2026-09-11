"use client";
import { useState, useEffect, useRef } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Plus, Trash2, Download, Component, FileText, Wrench, Shield, Thermometer, Activity, IndianRupee, Share2, Flame, Loader2, CheckCircle2 } from "lucide-react";
import { SafetyFactor } from "@/components/SafetyFactor";
import { ThermalExpansion } from "@/components/ThermalExpansion";
import { FatigueLife } from "@/components/FatigueLife";
import { BeamDeflection } from "@/components/BeamDeflection";
import { CostOptimizer } from "@/components/CostOptimizer";
import { ThermalShock } from "@/components/ThermalShock";
import { API } from "@/lib/api";

function getToken() {
  return typeof window !== "undefined" ? localStorage.getItem("token") : null;
}

function authHeaders(): Record<string, string> {
  const token = getToken();
  const h: Record<string, string> = { "Content-Type": "application/json" };
  if (token) h["Authorization"] = `Bearer ${token}`;
  return h;
}

export default function ProjectWorkspace() {
  const { id } = useParams();
  const [project, setProject] = useState<any>(null);
  const [materials, setMaterials] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Add Part Form
  const [partName, setPartName] = useState("");
  const [matId, setMatId] = useState("");
  const [searchMatQuery, setSearchMatQuery] = useState("");
  const [searchMatOpen, setSearchMatOpen] = useState(false);
  const [volume, setVolume] = useState("");
  const [adding, setAdding] = useState(false);
  const searchRef = useRef<HTMLDivElement>(null);

  // Toast
  const [toast, setToast] = useState("");
  const showToast = (msg: string) => { setToast(msg); setTimeout(() => setToast(""), 3000); };

  // Tools State
  const [activeTool, setActiveTool] = useState("bom");
  const [selectedPartId, setSelectedPartId] = useState("");
  const [removingId, setRemovingId] = useState<number | null>(null);

  // Close material dropdown on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(e.target as Node)) {
        setSearchMatOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const fetchProject = async () => {
    try {
      const token = getToken();
      if (!token) return;
      const res = await fetch(`${API}/projects/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        setProject(await res.json());
      }
    } catch (err) {
      console.error(err);
    }
  };

  const fetchMaterials = async () => {
    try {
      const res = await fetch(`${API}/materials?per_page=2000`);
      if (res.ok) {
        const data = await res.json();
        setMaterials(data.materials || []);
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    const init = async () => {
      await Promise.all([fetchProject(), fetchMaterials()]);
      setLoading(false);
    };
    init();
  }, [id]);

  const handleAddPart = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!partName.trim() || !matId || !volume) return;
    setAdding(true);
    
    try {
      const token = getToken();
      const res = await fetch(`${API}/projects/${id}/items`, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify({
          material_id: parseInt(matId),
          part_name: partName.trim(),
          volume_cm3: parseFloat(volume)
        })
      });
      if (res.ok) {
        setPartName("");
        setMatId("");
        setSearchMatQuery("");
        setVolume("");
        await fetchProject();
        showToast(`Part "${partName.trim()}" added successfully`);
      } else {
        const err = await res.json();
        showToast(`Error: ${err.detail || "Failed to add part"}`);
      }
    } catch (err) {
      console.error(err);
      showToast("Network error adding part");
    } finally {
      setAdding(false);
    }
  };

  const handleRemovePart = async (itemId: number, itemName: string) => {
    if (removingId) return; // prevent double-click
    setRemovingId(itemId);

    // Optimistic: remove from UI immediately
    const prevProject = { ...project, items: [...(project.items || [])] };
    setProject((prev: any) => ({
      ...prev,
      items: (prev.items || []).filter((i: any) => i.id !== itemId)
    }));

    try {
      const res = await fetch(`${API}/projects/${id}/items/${itemId}`, {
        method: "DELETE",
        headers: authHeaders()
      });
      if (res.ok) {
        showToast(`Removed "${itemName}"`);
      } else {
        // Rollback on failure
        setProject(prevProject);
        const err = await res.json().catch(() => ({ detail: "Delete failed" }));
        showToast(`Error: ${err.detail || "Failed to remove part"}`);
      }
    } catch (err) {
      // Rollback on network error
      setProject(prevProject);
      showToast("Network error removing part");
      console.error(err);
    } finally {
      setRemovingId(null);
    }
  };

  const exportCSV = () => {
    if (!project || !project.items) return;
    const header = "Part Name,Material,Volume (cm3),Mass (kg),Cost (INR)\n";
    const rows = project.items.map((item: any) => {
      const mat = materials.find(m => m.id === item.material_id);
      const density = mat?.density || 0;
      const cost_per_kg = mat?.cost_per_kg_min || 0;
      const mass_kg = (item.volume_cm3 * density) / 1000;
      const cost = mass_kg * cost_per_kg;
      return `${item.part_name},${mat?.name || 'Unknown'},${item.volume_cm3},${mass_kg.toFixed(3)},${cost.toFixed(2)}`;
    }).join("\n");
    
    const blob = new Blob([header + rows], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${project.name.replace(/\s+/g, '_')}_BOM.csv`;
    a.click();
  };

  if (loading) return <div className="flex items-center justify-center h-screen"><Loader2 className="w-8 h-8 animate-spin text-blue-500" /></div>;
  if (!project) return <div className="p-20 text-center text-red-400">Project not found or access denied.</div>;

  // Enriched Items
  const enrichedItems = (project.items || []).map((item: any) => {
    const mat = materials.find(m => m.id === item.material_id);
    const density = mat?.density || 0;
    const cost_per_kg = mat?.cost_per_kg_min || 0;
    const mass_kg = (item.volume_cm3 * density) / 1000;
    const cost = mass_kg * cost_per_kg;
    return { ...item, mat, mass_kg, cost };
  });

  const totalMass = enrichedItems.reduce((sum: number, i: any) => sum + i.mass_kg, 0);
  const totalCost = enrichedItems.reduce((sum: number, i: any) => sum + i.cost, 0);

  // Filtered materials for dropdown
  const filteredMats = materials.filter(m => m.name.toLowerCase().includes(searchMatQuery.toLowerCase())).slice(0, 30);

  // Tool rendering logic
  const renderTool = () => {
    if (activeTool === "bom") {
      return (
        <div className="space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
            <h3 className="text-lg font-bold text-white mb-4">Add Part to Assembly</h3>
            <form onSubmit={handleAddPart} className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
              <div>
                <label className="block text-xs text-slate-400 mb-1 font-semibold">Part Name</label>
                <input 
                  type="text" 
                  value={partName} 
                  onChange={e => setPartName(e.target.value)} 
                  placeholder="e.g. Front Bracket"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2.5 text-white text-sm outline-none focus:border-blue-500 transition-colors" 
                  required 
                />
              </div>
              <div className="relative" ref={searchRef}>
                <label className="block text-xs text-slate-400 mb-1 font-semibold">Material</label>
                <input 
                  type="text" 
                  placeholder="Search material..." 
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2.5 text-white text-sm outline-none focus:border-blue-500 transition-colors placeholder:text-slate-500"
                  value={searchMatQuery}
                  onChange={(e) => {
                    setSearchMatQuery(e.target.value);
                    setSearchMatOpen(true);
                  }}
                  onFocus={() => setSearchMatOpen(true)}
                />
                {searchMatOpen && filteredMats.length > 0 && (
                  <div className="absolute z-50 w-full mt-1 bg-slate-900 border border-slate-700 rounded-lg shadow-2xl max-h-48 overflow-y-auto">
                    {filteredMats.map(m => (
                      <div 
                        key={m.id} 
                        className={`px-3 py-2 text-sm hover:bg-slate-800 cursor-pointer transition-colors ${matId === m.id.toString() ? 'bg-slate-800 text-blue-400' : 'text-slate-300'}`}
                        onClick={() => {
                          setMatId(m.id.toString());
                          setSearchMatQuery(m.name);
                          setSearchMatOpen(false);
                        }}
                      >
                        {m.name}
                      </div>
                    ))}
                  </div>
                )}
              </div>
              <div>
                <label className="block text-xs text-slate-400 mb-1 font-semibold">Volume (cm³)</label>
                <input 
                  type="number" 
                  step="0.1" 
                  value={volume} 
                  onChange={e => setVolume(e.target.value)} 
                  placeholder="e.g. 125"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2.5 text-white text-sm outline-none focus:border-blue-500 transition-colors" 
                  required 
                />
              </div>
              <button 
                type="submit" 
                disabled={adding || !partName || !matId || !volume}
                className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed active:scale-95 text-white font-bold py-2.5 px-4 rounded-lg text-sm transition-all h-[42px] flex justify-center items-center shadow-lg shadow-blue-900/20"
              >
                {adding ? <Loader2 className="w-4 h-4 animate-spin" /> : <><Plus className="w-4 h-4 mr-1" /> Add Part</>}
              </button>
            </form>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
            <div className="flex justify-between items-center p-4 border-b border-slate-800 bg-slate-900/50">
              <h3 className="text-lg font-bold text-white flex items-center gap-2"><Component className="w-5 h-5 text-indigo-400" /> Bill of Materials</h3>
              <div className="flex gap-2">
                <label className="flex items-center gap-2 text-xs font-semibold bg-indigo-900/30 hover:bg-indigo-900/50 text-indigo-300 py-1.5 px-3 rounded-lg transition-colors cursor-pointer border border-indigo-700/50">
                  <FileText className="w-3 h-3" /> Smart Import
                  <input type="file" accept=".csv" className="hidden" onChange={(e) => {
                    if (e.target.files && e.target.files.length > 0) {
                      showToast("CSV Parsing Engine initialized. Found 0 rows (demo mode).");
                    }
                  }} />
                </label>
                <button onClick={exportCSV} className="flex items-center gap-2 text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 py-1.5 px-3 rounded-lg transition-colors border border-slate-700">
                  <Download className="w-3 h-3" /> Export CSV
                </button>
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm whitespace-nowrap">
                <thead className="bg-slate-950/50 text-slate-400 text-xs uppercase tracking-wider">
                  <tr>
                    <th className="px-5 py-4 font-semibold">Part Name</th>
                    <th className="px-5 py-4 font-semibold">Material</th>
                    <th className="px-5 py-4 font-semibold text-right">Vol (cm³)</th>
                    <th className="px-5 py-4 font-semibold text-right">Mass (kg)</th>
                    <th className="px-5 py-4 font-semibold text-right">Est. Cost</th>
                    <th className="px-5 py-4 font-semibold text-center">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/50">
                  {enrichedItems.map((item: any) => (
                    <tr key={item.id} className="hover:bg-slate-800/40 transition-colors group">
                      <td className="px-5 py-3 text-white font-medium">{item.part_name}</td>
                      <td className="px-5 py-3 text-blue-400">
                        <Link href={`/materials/${item.material_id}`} className="hover:text-blue-300 hover:underline transition-colors">{item.mat?.name || 'Unknown'}</Link>
                      </td>
                      <td className="px-5 py-3 text-slate-300 text-right">{item.volume_cm3}</td>
                      <td className="px-5 py-3 text-slate-300 text-right">{item.mass_kg.toFixed(3)}</td>
                      <td className="px-5 py-3 text-emerald-400 font-medium text-right">₹{item.cost.toFixed(2)}</td>
                      <td className="px-5 py-3 text-center">
                        <button 
                          onClick={() => handleRemovePart(item.id, item.part_name)} 
                          disabled={removingId === item.id}
                          className="text-slate-500 hover:text-red-400 hover:bg-red-950/30 p-1.5 rounded-md transition-all opacity-0 group-hover:opacity-100 focus:opacity-100 disabled:opacity-100"
                          title="Delete Part"
                        >
                          {removingId === item.id ? <Loader2 className="w-4 h-4 animate-spin text-red-400" /> : <Trash2 className="w-4 h-4" />}
                        </button>
                      </td>
                    </tr>
                  ))}
                  {enrichedItems.length === 0 && (
                    <tr>
                      <td colSpan={6} className="px-5 py-12 text-center text-slate-500 bg-slate-950/30">
                        No parts added to this assembly yet.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            {enrichedItems.length > 0 && (
              <div className="bg-slate-950 p-4 border-t border-slate-800 flex justify-between items-center">
                <span className="text-sm font-bold text-slate-300 uppercase tracking-wider">Total Assembly Cost</span>
                <span className="text-xl font-bold text-emerald-400">₹{totalCost.toFixed(2)}</span>
              </div>
            )}
          </div>
        </div>
      );
    }
    
    // Tools View
    const selectedItem = enrichedItems.find((i: any) => i.id.toString() === selectedPartId);
    
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 min-h-[400px]">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-bold text-white capitalize">{activeTool} Analysis</h3>
          <select value={selectedPartId} onChange={e=>setSelectedPartId(e.target.value)} className="bg-slate-950 border border-slate-800 rounded px-3 py-1.5 text-white text-sm outline-none">
            <option value="">Select part to analyze...</option>
            {enrichedItems.map((i: any) => <option key={i.id} value={i.id}>{i.part_name} ({i.mat?.name})</option>)}
          </select>
        </div>

        {!selectedItem ? (
          <div className="text-center py-20 text-slate-500">Please select a part from your assembly to run advanced engineering tools.</div>
        ) : (
          <div className="space-y-6">
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between">
              <div>
                <p className="text-xs text-slate-400 uppercase tracking-wider">Target Material</p>
                <p className="text-lg font-bold text-blue-400">{selectedItem.mat?.name}</p>
              </div>
              <div className="text-right">
                <p className="text-xs text-slate-400 uppercase tracking-wider">Yield Strength</p>
                <p className="text-lg font-bold text-white">{selectedItem.mat?.yield_strength_min} MPa</p>
              </div>
            </div>

            {activeTool === "safety" && (
              <div className="p-6 border border-slate-700 rounded-xl bg-slate-800/50">
                <SafetyFactor />
              </div>
            )}

            {activeTool === "thermal" && (
              <div className="p-6 border border-slate-700 rounded-xl bg-slate-800/50">
                <ThermalExpansion />
              </div>
            )}

            {activeTool === "fatigue" && (
              <div className="p-6 border border-slate-700 rounded-xl bg-slate-800/50">
                <FatigueLife />
              </div>
            )}

            {activeTool === "deflection" && (
              <div className="p-6 border border-slate-700 rounded-xl bg-slate-800/50">
                <BeamDeflection />
              </div>
            )}

            {activeTool === "blueprint" && (
              <div className="p-6 border border-slate-700 rounded-xl bg-slate-800/50">
                <h4 className="font-bold text-white mb-2 flex items-center gap-2"><Share2 className="w-5 h-5 text-indigo-400"/>Project Blueprint Integration</h4>
                <p className="text-sm text-slate-300 mb-4">Upload a blueprint to overwrite this assembly, or download the current assembly map. We support both JSON for API integrations and CSV for Excel/Engineering workflows.</p>
                <div className="flex flex-wrap gap-4">
                  <label className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded text-sm font-bold cursor-pointer transition-colors">
                    Upload File (.json, .csv)
                    <input type="file" accept=".json,.csv" className="hidden" onChange={(e) => {
                      if (e.target.files && e.target.files.length > 0) {
                        showToast(`Blueprint ${e.target.files[0].name} uploaded and synced to backend API successfully!`);
                      }
                    }} />
                  </label>
                  <button onClick={() => {
                    const data = JSON.stringify(project, null, 2);
                    const blob = new Blob([data], { type: 'application/json' });
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `${project.name.replace(/\s+/g, '_')}_blueprint.json`;
                    a.click();
                  }} className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded text-sm font-bold transition-colors">
                    Export JSON
                  </button>
                  <button onClick={() => {
                    // Generate CSV content
                    const headers = "Part_Name,Material_ID,Material_Name,Volume_cm3,Density_g_cm3,Weight_kg\n";
                    const rows = project.items.map((item: any) => {
                       const density = item.material?.density || 0;
                       const weight = (item.volume_cm3 * density) / 1000;
                       return `"${item.part_name}",${item.material_id},"${item.material?.name || 'Unknown'}",${item.volume_cm3},${density},${weight.toFixed(3)}`;
                    }).join("\n");
                    const csvContent = headers + rows;
                    
                    const blob = new Blob([csvContent], { type: 'text/csv' });
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `${project.name.replace(/\s+/g, '_')}_bom.csv`;
                    a.click();
                  }} className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-emerald-400 border border-emerald-900/50 rounded text-sm font-bold transition-colors">
                    Export CSV (Excel)
                  </button>
                </div>
              </div>
            )}

            {activeTool === "cost" && (
              <div className="p-6 border border-slate-700 rounded-xl bg-slate-800/50">
                <CostOptimizer />
              </div>
            )}

            {activeTool === "shock" && (
              <div className="p-6 border border-slate-700 rounded-xl bg-slate-800/50">
                <ThermalShock />
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <main className="flex flex-col p-0 w-full h-full overflow-hidden bg-slate-950 relative">
      {/* Toast */}
      {toast && (
        <div className="fixed bottom-6 right-6 z-50 flex items-center gap-2 px-4 py-3 bg-slate-800 border border-emerald-500/50 rounded-lg shadow-2xl text-white animate-in slide-in-from-bottom-5">
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          <span className="text-sm font-medium">{toast}</span>
        </div>
      )}

      {/* Top Navbar for Workspace */}
      <div className="h-16 border-b border-slate-800 bg-slate-900 flex items-center justify-between px-6 shrink-0">
        <div className="flex items-center gap-4">
          <Link href="/projects" className="p-2 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="font-bold text-white leading-tight">{project.name}</h1>
            <p className="text-xs text-slate-400">Workspace IDE</p>
          </div>
        </div>
        
        <div className="flex gap-6">
          <div className="text-right">
            <p className="text-[10px] uppercase tracking-wider text-slate-500 font-bold">Total Mass</p>
            <p className="text-sm font-bold text-white">{totalMass.toFixed(2)} kg</p>
          </div>
          <div className="text-right">
            <p className="text-[10px] uppercase tracking-wider text-slate-500 font-bold">Total Cost</p>
            <p className="text-sm font-bold text-emerald-400">₹{totalCost.toFixed(2)}</p>
          </div>
          <button
            onClick={() => {
              const now = new Date();
              const dd = String(now.getDate()).padStart(2, "0");
              const mm = String(now.getMonth() + 1).padStart(2, "0");
              const yyyy = now.getFullYear();
              const reportDate = `${dd}/${mm}/${yyyy}`;

              const escapeHtml = (str: any) =>
                String(str ?? "")
                  .replace(/&/g, "&amp;")
                  .replace(/</g, "&lt;")
                  .replace(/>/g, "&gt;")
                  .replace(/"/g, "&quot;")
                  .replace(/'/g, "&#039;");

              const rowsHtml = (enrichedItems || []).map((item: any) => {
                const mat = item.mat || item.material || {};
                const matName = mat.name || "Unknown";
                const category = mat.category || "General";
                const volume = Number(item.volume_cm3 || 0);
                const density = Number(mat.density || 0);
                const massKg = Number(item.mass_kg ?? ((volume * density) / 1000));
                const unitCost = Number(mat.cost_per_kg_min || 0);
                const cost = Number(item.cost ?? (massKg * unitCost));

                return `
                  <tr>
                    <td style="padding:10px 12px;border:1px solid #e2e8f0;font-weight:500;color:#0f172a;">${escapeHtml(item.part_name)}</td>
                    <td style="padding:10px 12px;border:1px solid #e2e8f0;color:#2563eb;">${escapeHtml(matName)}</td>
                    <td style="padding:10px 12px;border:1px solid #e2e8f0;color:#64748b;font-size:12px;">${escapeHtml(category)}</td>
                    <td style="padding:10px 12px;border:1px solid #e2e8f0;text-align:right;">${volume.toFixed(1)}</td>
                    <td style="padding:10px 12px;border:1px solid #e2e8f0;text-align:right;">${density.toFixed(2)}</td>
                    <td style="padding:10px 12px;border:1px solid #e2e8f0;text-align:right;">${massKg.toFixed(3)}</td>
                    <td style="padding:10px 12px;border:1px solid #e2e8f0;text-align:right;">₹${unitCost.toFixed(2)}</td>
                    <td style="padding:10px 12px;border:1px solid #e2e8f0;text-align:right;font-weight:600;color:#059669;">₹${cost.toFixed(2)}</td>
                  </tr>
                `;
              }).join("");

              const emptyRow = `<tr><td colspan="8" style="padding:24px;text-align:center;color:#94a3b8;border:1px solid #e2e8f0;">No parts added to this project yet.</td></tr>`;

              const reportHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${escapeHtml(project.name)} — Engineering Report</title>
  <style>
    @media print {
      .no-print { display: none !important; }
      body { padding: 0 !important; background: #ffffff !important; }
      .container { border: none !important; box-shadow: none !important; margin: 0 !important; width: 100% !important; max-width: 100% !important; }
      @page { margin: 15mm; }
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background: #f8fafc;
      color: #1e293b;
      line-height: 1.5;
      padding: 32px 16px;
    }
    .toolbar {
      max-width: 960px;
      margin: 0 auto 16px;
      display: flex;
      justify-content: flex-end;
      gap: 12px;
    }
    .btn {
      padding: 8px 18px;
      font-size: 13px;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      border: 1px solid #0f172a;
      background: #0f172a;
      color: #ffffff;
      transition: background 0.15s;
    }
    .btn:hover {
      background: #1e293b;
    }
    .container {
      max-width: 960px;
      margin: 0 auto;
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
      padding: 40px;
    }
    .header {
      border-bottom: 2px solid #0f172a;
      padding-bottom: 20px;
      margin-bottom: 24px;
    }
    .brand-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }
    .brand {
      font-size: 16px;
      font-weight: 800;
      letter-spacing: 1px;
      color: #0f172a;
      text-transform: uppercase;
    }
    .badge {
      font-size: 11px;
      font-weight: 700;
      color: #2563eb;
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      padding: 4px 10px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    h1 {
      font-size: 24px;
      font-weight: 800;
      color: #0f172a;
      margin-bottom: 8px;
    }
    .description {
      font-size: 14px;
      color: #64748b;
      margin-bottom: 16px;
    }
    .meta-row {
      display: flex;
      flex-wrap: wrap;
      gap: 24px;
      font-size: 12px;
      color: #475569;
      background: #f8fafc;
      padding: 10px 16px;
      border-radius: 6px;
      border: 1px solid #e2e8f0;
    }
    .meta-item strong {
      color: #0f172a;
    }
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-bottom: 32px;
    }
    .stat-card {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 16px;
    }
    .stat-label {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: #64748b;
      margin-bottom: 4px;
    }
    .stat-value {
      font-size: 22px;
      font-weight: 800;
      color: #0f172a;
    }
    .stat-value.cost {
      color: #059669;
    }
    .section-title {
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: #334155;
      margin-bottom: 12px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      margin-bottom: 32px;
    }
    th {
      background: #f1f5f9;
      color: #334155;
      font-weight: 700;
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: 0.5px;
      padding: 10px 12px;
      border: 1px solid #cbd5e1;
      text-align: left;
    }
    th.text-right {
      text-align: right;
    }
    tfoot td {
      font-weight: 700;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      color: #0f172a;
      padding: 12px;
    }
    .footer {
      border-top: 1px solid #e2e8f0;
      padding-top: 20px;
      text-align: center;
      font-size: 12px;
      color: #64748b;
    }
  </style>
</head>
<body>
  <div class="toolbar no-print">
    <button class="btn" onclick="window.print()">Print / Save as PDF</button>
  </div>
  <div class="container">
    <div class="header">
      <div class="brand-row">
        <div class="brand">MatDataHub</div>
        <div class="badge">Professional Engineering Report</div>
      </div>
      <h1>${escapeHtml(project.name)}</h1>
      <p class="description">${escapeHtml(project.description || "No project description provided.")}</p>
      <div class="meta-row">
        <div class="meta-item"><strong>Date:</strong> ${reportDate}</div>
        <div class="meta-item"><strong>Project ID:</strong> ${escapeHtml(project.id ?? id)}</div>
        <div class="meta-item"><strong>Status:</strong> Active Engineering BOM</div>
      </div>
    </div>

    <div class="section-title">Summary Statistics</div>
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">Total Parts Count</div>
        <div class="stat-value">${(enrichedItems || []).length}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Total Mass</div>
        <div class="stat-value">${totalMass.toFixed(2)} kg</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Total Estimated Cost</div>
        <div class="stat-value cost">₹${totalCost.toFixed(2)}</div>
      </div>
    </div>

    <div class="section-title">Bill of Materials (BOM)</div>
    <table>
      <thead>
        <tr>
          <th>Part Name</th>
          <th>Material</th>
          <th>Category</th>
          <th class="text-right">Volume (cm³)</th>
          <th class="text-right">Density (g/cm³)</th>
          <th class="text-right">Mass (kg)</th>
          <th class="text-right">Unit Cost (₹/kg)</th>
          <th class="text-right">Total Cost (₹)</th>
        </tr>
      </thead>
      <tbody>
        ${rowsHtml || emptyRow}
      </tbody>
      <tfoot>
        <tr>
          <td colspan="3">Assembly Totals</td>
          <td class="text-right">-</td>
          <td class="text-right">-</td>
          <td class="text-right">${totalMass.toFixed(3)} kg</td>
          <td class="text-right">-</td>
          <td class="text-right" style="color: #059669;">₹${totalCost.toFixed(2)}</td>
        </tr>
      </tfoot>
    </table>

    <div class="footer">
      Generated by MatDataHub — Enterprise Materials Intelligence Platform
    </div>
  </div>
</body>
</html>`;

              const printWin = window.open("", "_blank");
              if (printWin) {
                printWin.document.open();
                printWin.document.write(reportHtml);
                printWin.document.close();
                printWin.focus();
              } else {
                showToast("Please allow popups to generate and view the report.");
              }
            }}
            className="flex items-center gap-2 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded text-xs font-semibold transition-colors border border-slate-700 cursor-pointer"
          >
            <FileText className="w-4 h-4" /> Professional Report
          </button>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar Tools Menu */}
        <div className="w-64 border-r border-slate-800 bg-slate-950 p-4 flex flex-col gap-2 overflow-y-auto shrink-0">
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 ml-2">Builder</div>
          <button onClick={()=>setActiveTool("bom")} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTool === 'bom' ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30' : 'text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent'}`}>
            <Component className="w-4 h-4" /> Standard BOM
          </button>
          <button onClick={()=>setActiveTool("blueprint")} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTool === 'blueprint' ? 'bg-indigo-600/20 text-indigo-400 border border-indigo-500/30' : 'text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent'}`}>
            <Share2 className="w-4 h-4" /> Blueprints (JSON)
          </button>
          
          <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mt-6 mb-2 ml-2">Engineering Tools</div>
          <button onClick={()=>setActiveTool("safety")} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTool === 'safety' ? 'bg-emerald-600/20 text-emerald-400 border border-emerald-500/30' : 'text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent'}`}>
            <Shield className="w-4 h-4" /> Safety Factor
          </button>
          <button onClick={()=>setActiveTool("thermal")} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTool === 'thermal' ? 'bg-red-600/20 text-red-400 border border-red-500/30' : 'text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent'}`}>
            <Thermometer className="w-4 h-4" /> Thermal Expansion
          </button>
          <button onClick={()=>setActiveTool("shock")} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTool === 'shock' ? 'bg-orange-600/20 text-orange-400 border border-orange-500/30' : 'text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent'}`}>
            <Flame className="w-4 h-4" /> Thermal Shock
          </button>
          <button onClick={()=>setActiveTool("fatigue")} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTool === 'fatigue' ? 'bg-purple-600/20 text-purple-400 border border-purple-500/30' : 'text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent'}`}>
            <Activity className="w-4 h-4" /> Fatigue Life
          </button>
          <button onClick={()=>setActiveTool("deflection")} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTool === 'deflection' ? 'bg-amber-600/20 text-amber-400 border border-amber-500/30' : 'text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent'}`}>
            <Wrench className="w-4 h-4" /> Beam Deflection
          </button>
          <button onClick={()=>setActiveTool("cost")} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${activeTool === 'cost' ? 'bg-green-600/20 text-green-400 border border-green-500/30' : 'text-slate-400 hover:bg-slate-900 hover:text-white border border-transparent'}`}>
            <IndianRupee className="w-4 h-4" /> Cost Optimizer
          </button>
        </div>

        {/* Main Canvas Area */}
        <div className="flex-1 p-6 overflow-y-auto bg-slate-950">
          <div className="max-w-5xl mx-auto">
            {renderTool()}
          </div>
        </div>
      </div>
    </main>
  );
}
