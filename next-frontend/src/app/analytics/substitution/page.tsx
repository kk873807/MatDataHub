"use client";
import { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { ArrowLeft, Replace, Loader2, Lock, ShieldAlert } from "lucide-react";
import { useSearchParams } from "next/navigation";
import { API } from "@/lib/api";

function SmartSubstitutionContent() {
  const searchParams = useSearchParams();
  const [allMaterials, setAllMaterials] = useState<any[]>([]);
  const [baseId, setBaseId] = useState("");

  useEffect(() => {
    const base = searchParams.get("base");
    if (base) setBaseId(base);
  }, [searchParams]);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchOpen, setSearchOpen] = useState(false);

  // Auto-fill search query when baseId is set from URL and materials load
  useEffect(() => {
    if (baseId && allMaterials.length > 0 && !searchQuery) {
      const mat = allMaterials.find(m => m.id.toString() === baseId);
      if (mat) setSearchQuery(mat.name);
    }
  }, [baseId, allMaterials]);
  const [weights, setWeights] = useState({
    cost: 50,
    density: 50,
    tensile: 50,
    carbon: 50
  });
  
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [isLocked, setIsLocked] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [userTier, setUserTier] = useState("free");
  const [isAdmin, setIsAdmin] = useState(false);

  // Auth check on mount
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setIsAuthenticated(false);
      return;
    }
    fetch(`${API}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(async r => {
        if (r.ok) {
          const data = await r.json();
          setIsAuthenticated(true);
          setUserTier(data.tier || "free");
          setIsAdmin(data.is_admin || false);
        } else {
          setIsAuthenticated(false);
        }
      })
      .catch(() => setIsAuthenticated(false));
  }, []);

  useEffect(() => {
    fetch(`${API}/materials?per_page=2000`)
      .then(res => res.json())
      .then(data => setAllMaterials(data.materials || []));
  }, []);

  const runSubstitution = async () => {
    if (!baseId) return;
    setLoading(true);
    setIsLocked(false);
    
    try {
      // Map frontend weight keys to what the backend SubstitutionEngine expects
      const normalizedWeights = {
        cost: weights.cost / 100,
        density: weights.density / 100,
        tensile_strength: weights.tensile / 100,
        embodied_carbon: weights.carbon / 100
      };

      const token = localStorage.getItem("token");
      const res = await fetch(`${API}/materials/substitute`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {})
        },
        body: JSON.stringify({
          base_material_id: parseInt(baseId),
          weights: normalizedWeights
        })
      });

      if (res.ok) {
        setResults(await res.json());
      } else if (res.status === 403) {
        setIsLocked(true);
      } else if (res.status === 401) {
        setIsAuthenticated(false);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (isAuthenticated === null) {
    return <div className="flex items-center justify-center h-screen"><Loader2 className="w-8 h-8 animate-spin text-purple-500" /></div>;
  }

  // Sign In Required screen
  if (isAuthenticated === false) {
    return (
      <main className="flex flex-col p-6 lg:p-10 w-full h-full">
        <div className="w-full max-w-5xl mx-auto space-y-6">
          <Link href="/analytics" className="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back to Analytics
          </Link>
          
          <div className="p-10 mt-10 rounded-3xl bg-white dark:bg-slate-900 border border-purple-500/30 text-center relative overflow-hidden flex flex-col items-center justify-center">
            <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 to-transparent"></div>
            <div className="w-20 h-20 bg-purple-950 rounded-full flex items-center justify-center mb-6 relative z-10 border border-purple-500/50">
              <Lock className="w-10 h-10 text-purple-500" />
            </div>
            
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white font-heading mb-4 relative z-10">Sign In Required</h2>
            <p className="text-slate-600 dark:text-slate-300 relative z-10 max-w-2xl mx-auto mb-8 text-lg">
              You must be signed in to use the Smart AI Substitution engine. 
            </p>
            
            <Link href="/account" className="relative z-10 px-8 py-4 bg-purple-600 hover:bg-purple-700 text-white rounded-xl font-bold transition-all shadow-lg hover:scale-105">
              Sign In or Register
            </Link>
          </div>
        </div>
      </main>
    );
  }

  // Free tier — Upgrade Required (pre-gate before showing any UI)
  if (!isAdmin && !["pro", "advanced"].includes(userTier)) {
    return (
      <main className="flex flex-col p-6 lg:p-10 w-full h-full">
        <div className="w-full max-w-5xl mx-auto space-y-6">
          <Link href="/analytics" className="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back to Analytics
          </Link>
          
          <div className="p-10 mt-10 rounded-3xl bg-white dark:bg-slate-900 border border-yellow-500/30 text-center relative overflow-hidden flex flex-col items-center justify-center">
            <div className="absolute inset-0 bg-gradient-to-br from-yellow-900/20 to-transparent"></div>
            <div className="w-20 h-20 bg-yellow-950 rounded-full flex items-center justify-center mb-6 relative z-10 border border-yellow-500/50">
              <Lock className="w-10 h-10 text-yellow-500" />
            </div>
            
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white font-heading mb-4 relative z-10">Upgrade Required</h2>
            <p className="text-slate-600 dark:text-slate-300 relative z-10 max-w-2xl mx-auto mb-8 text-lg">
              Smart AI Substitution is a Pro feature. Upgrade your account to unlock intelligent material replacement suggestions.
            </p>
            
            <Link href="/account" className="relative z-10 px-8 py-4 bg-yellow-600 hover:bg-yellow-700 text-slate-900 dark:text-white rounded-xl font-bold transition-all shadow-lg hover:scale-105">
              Upgrade Account
            </Link>
          </div>
        </div>
      </main>
    );
  }
  return (
    <main className="flex flex-col p-6 lg:p-10 w-full h-full overflow-y-auto">
      <div className="w-full max-w-5xl mx-auto space-y-8">
        
        <Link href="/analytics" className="inline-flex items-center gap-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white transition-colors">
          <ArrowLeft className="w-4 h-4" /> Back to Analytics
        </Link>

        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white font-heading flex items-center gap-3">
            <Replace className="w-8 h-8 text-purple-400" />
            Smart AI Substitution
          </h1>
          <p className="text-slate-600 dark:text-slate-300 mt-2">Discover optimal alternative materials based on weighted design priorities.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Controls Panel */}
          <div className="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 space-y-6">
            <div className="relative">
              <label className="block text-sm font-semibold text-slate-200 mb-2">Base Material</label>
              <div 
                className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl px-4 py-3 text-slate-500 dark:text-slate-400 cursor-text flex items-center justify-between outline-none focus-within:border-purple-500"
              >
                <input 
                  type="text" 
                  placeholder="Search material to replace..." 
                  className="bg-transparent border-none outline-none w-full text-slate-900 dark:text-white placeholder:text-slate-500 dark:text-slate-400"
                  value={searchQuery}
                  onChange={(e) => {
                    setSearchQuery(e.target.value);
                    setSearchOpen(true);
                  }}
                  onFocus={() => setSearchOpen(true)}
                />
              </div>
              {searchOpen && (
                <div className="absolute z-10 w-full mt-1 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-700 rounded-2xl shadow-xl max-h-60 overflow-y-auto">
                  {allMaterials.filter(m => m.name.toLowerCase().includes(searchQuery.toLowerCase())).slice(0, 50).map(m => (
                    <div 
                      key={m.id} 
                      className={`px-4 py-2 hover:bg-slate-100 dark:hover:bg-slate-800 cursor-pointer ${baseId === m.id.toString() ? 'bg-slate-100 dark:bg-slate-800 text-purple-400' : 'text-slate-600 dark:text-slate-300'}`}
                      onClick={() => {
                        setBaseId(m.id.toString());
                        setSearchQuery(m.name);
                        setSearchOpen(false);
                      }}
                    >
                      {m.name}
                    </div>
                  ))}
                  {allMaterials.filter(m => m.name.toLowerCase().includes(searchQuery.toLowerCase())).length === 0 && (
                    <div className="px-4 py-2 text-slate-500 dark:text-slate-400 text-sm">No materials found.</div>
                  )}
                </div>
              )}
            </div>

            <div className="space-y-4 pt-2 border-t border-slate-200 dark:border-slate-800">
              <h3 className="text-sm font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Optimization Weights</h3>
              
              <div>
                <div className="flex justify-between text-xs text-slate-600 dark:text-slate-300 mb-1">
                  <span>Reduce Cost</span>
                  <span>{weights.cost}%</span>
                </div>
                <input type="range" min="0" max="100" value={weights.cost} onChange={e => setWeights({...weights, cost: parseInt(e.target.value)})} className="w-full accent-purple-500" />
              </div>

              <div>
                <div className="flex justify-between text-xs text-slate-600 dark:text-slate-300 mb-1">
                  <span>Reduce Weight (Density)</span>
                  <span>{weights.density}%</span>
                </div>
                <input type="range" min="0" max="100" value={weights.density} onChange={e => setWeights({...weights, density: parseInt(e.target.value)})} className="w-full accent-purple-500" />
              </div>

              <div>
                <div className="flex justify-between text-xs text-slate-600 dark:text-slate-300 mb-1">
                  <span>Maximize Strength (Tensile)</span>
                  <span>{weights.tensile}%</span>
                </div>
                <input type="range" min="0" max="100" value={weights.tensile} onChange={e => setWeights({...weights, tensile: parseInt(e.target.value)})} className="w-full accent-purple-500" />
              </div>

              <div>
                <div className="flex justify-between text-xs text-slate-600 dark:text-slate-300 mb-1">
                  <span>Minimize Carbon (ESG)</span>
                  <span>{weights.carbon}%</span>
                </div>
                <input type="range" min="0" max="100" value={weights.carbon} onChange={e => setWeights({...weights, carbon: parseInt(e.target.value)})} className="w-full accent-purple-500" />
              </div>
            </div>

            <button 
              onClick={runSubstitution}
              disabled={!baseId || loading}
              className="w-full py-3 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-2xl font-bold transition-colors"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : "Run AI Substitution"}
            </button>
          </div>

          {/* Results Panel */}
          <div className="lg:col-span-2">
            {isLocked ? (
              <div className="p-8 h-full rounded-2xl bg-white dark:bg-slate-900 border border-yellow-500/30 text-center relative overflow-hidden flex flex-col items-center justify-center">
                <div className="absolute inset-0 bg-gradient-to-br from-yellow-900/20 to-transparent"></div>
                <Lock className="w-12 h-12 text-yellow-400 mx-auto mb-4 relative z-10" />
                <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-2 relative z-10">Upgrade Required</h2>
                <p className="text-slate-600 dark:text-slate-300 relative z-10 max-w-md mx-auto mb-6">
                  Smart AI Substitution is a Pro feature. Upgrade your account to unlock this workflow.
                </p>
                <Link href="/account" className="relative z-10 px-8 py-3 bg-yellow-600 hover:bg-yellow-700 text-slate-900 dark:text-white rounded-2xl font-bold transition-colors shadow-lg shadow-yellow-900/50">
                  Upgrade Account
                </Link>
              </div>
            ) : results.length > 0 ? (
              <div className="space-y-4">
                <h3 className="font-bold text-slate-900 dark:text-white font-heading">Top Alternative Recommendations</h3>
                {results.map((res, i) => (
                  <div key={res.id} className="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 relative overflow-hidden">
                    {i === 0 && <div className="absolute top-0 right-0 bg-purple-600 text-white text-[10px] font-bold px-3 py-1 rounded-bl-lg">BEST MATCH</div>}
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h4 className="text-lg font-bold text-slate-900 dark:text-white font-heading">{res.name}</h4>
                        <div className="text-sm text-purple-400 font-semibold">{Math.round(res.match_score)}% Match Score</div>
                      </div>
                      <Link href={`/materials/${res.id}`} className="px-3 py-1 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded text-xs text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:text-white transition-colors">
                        View Details
                      </Link>
                    </div>
                    <div className="grid grid-cols-4 gap-4 pt-3 border-t border-slate-200 dark:border-slate-800">
                      <div>
                        <div className="text-[10px] text-slate-500 dark:text-slate-400 uppercase">Cost</div>
                        <div className="text-sm font-medium text-slate-200">₹{res.cost}/kg</div>
                      </div>
                      <div>
                        <div className="text-[10px] text-slate-500 dark:text-slate-400 uppercase">Density</div>
                        <div className="text-sm font-medium text-slate-200">{res.density} g/cm³</div>
                      </div>
                      <div>
                        <div className="text-[10px] text-slate-500 dark:text-slate-400 uppercase">Tensile</div>
                        <div className="text-sm font-medium text-slate-200">{res.tensile} MPa</div>
                      </div>
                      <div>
                        <div className="text-[10px] text-slate-500 dark:text-slate-400 uppercase">Carbon</div>
                        <div className="text-sm font-medium text-slate-200">{res.carbon} kgCO2</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-8 h-full rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex flex-col items-center justify-center text-center">
                <ShieldAlert className="w-10 h-10 text-slate-700 dark:text-slate-200 mb-4" />
                <h3 className="text-lg font-bold text-slate-500 dark:text-slate-400">Ready to Analyze</h3>
                <p className="text-sm text-slate-500 dark:text-slate-400 mt-2 max-w-sm">
                  Select a base material and configure your design priorities to discover optimal engineering alternatives.
                </p>
              </div>
            )}
          </div>

        </div>
      </div>
    </main>
  );
}

export default function SmartSubstitution() {
  return (
    <Suspense fallback={<div className="p-12 text-center text-slate-500 dark:text-slate-400">Loading...</div>}>
      <SmartSubstitutionContent />
    </Suspense>
  );
}
