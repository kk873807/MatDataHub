"use client";
import { useState, useEffect } from "react";
import { Shield, Key, Zap, CheckCircle2, AlertCircle, ArrowUpRight, LogOut, Clock } from "lucide-react";

export default function AccountDashboard() {
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [upgrading, setUpgrading] = useState(false);
  const [error, setError] = useState("");
  const [showKey, setShowKey] = useState(false);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      // Fetch from auth/me (we don't need token since backend is mocked for local dev)
      const res = await fetch("http://127.0.0.1:8000/api/v1/auth/me");
      if (res.ok) {
        const data = await res.json();
        setProfile(data);
      } else {
        setError("Failed to load profile. Are you logged in?");
      }
    } catch (err) {
      setError("Network error fetching profile.");
    } finally {
      setLoading(false);
    }
  };

  const handleUpgrade = async (tier: "pro" | "advanced") => {
    setUpgrading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/auth/upgrade", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tier })
      });
      if (res.ok) {
        await fetchProfile(); // Refresh profile to show 'pending' status
        alert(`Upgrade to ${tier.toUpperCase()} requested! An admin will review it shortly.`);
      } else {
        const err = await res.json();
        alert(err.detail || "Failed to request upgrade.");
      }
    } catch (err) {
      alert("Network error requesting upgrade.");
    } finally {
      setUpgrading(false);
    }
  };

  if (loading) return <div className="p-12 text-center text-slate-400">Loading profile...</div>;
  if (!profile) return <div className="p-12 text-center text-red-400">{error}</div>;

  return (
    <main className="flex flex-col p-6 lg:p-10 w-full min-h-screen">
      <div className="w-full max-w-5xl mx-auto space-y-8">
        <h1 className="text-3xl font-bold text-white flex items-center gap-3">
          <Shield className="w-8 h-8 text-blue-400" />
          Account & Security
        </h1>

        {/* Current Status Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-8 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl"></div>
            <h2 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-2">Current Tier</h2>
            <div className="flex items-end gap-4 mb-4">
              <span className="text-4xl font-extrabold text-white capitalize">{profile.tier}</span>
              {profile.tier === "advanced" && <span className="text-emerald-400 text-sm font-bold bg-emerald-900/30 px-2 py-1 rounded">Maximum Access</span>}
            </div>
            <p className="text-slate-300 text-sm">
              Logged in as <span className="font-semibold text-white">{profile.email}</span>
            </p>
            
            {profile.upgrade_status === "pending" && (
              <div className="mt-6 bg-amber-900/20 border border-amber-900/50 rounded-lg p-4 flex items-start gap-3">
                <Clock className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-sm font-bold text-amber-400">Upgrade Request Pending</h4>
                  <p className="text-xs text-amber-300/70 mt-1">
                    Your request for the <span className="uppercase font-bold">{profile.requested_tier}</span> tier is currently under review by an administrator.
                  </p>
                </div>
              </div>
            )}
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 flex flex-col justify-center items-center text-center space-y-4">
            <div className="w-16 h-16 rounded-full bg-slate-800 flex items-center justify-center text-2xl font-bold text-white">
              {profile.name ? profile.name.charAt(0).toUpperCase() : profile.email.charAt(0).toUpperCase()}
            </div>
            <div>
              <h3 className="text-white font-bold">{profile.name || "User"}</h3>
              <p className="text-xs text-slate-400">Member since {new Date(profile.created_at).getFullYear()}</p>
            </div>
            <button 
              onClick={() => {
                alert("Signed out successfully (Demo Mode).");
                window.location.href = "/";
              }}
              className="text-xs text-red-400 hover:text-red-300 flex items-center gap-1 mt-2 transition-colors"
            >
              <LogOut className="w-3 h-3" /> Sign Out
            </button>
          </div>
        </div>

        {/* API Access (Advanced Only) */}
        {profile.tier === "advanced" && (
          <div className="bg-slate-900 border border-emerald-900/50 rounded-2xl p-8 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl"></div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2 mb-4">
              <Key className="w-5 h-5 text-emerald-400" /> Programmatic API Access
            </h2>
            <p className="text-slate-300 text-sm mb-6">
              You have access to the MatDataHub REST API for automated queries. You must pass both your <strong>Client ID</strong> and <strong>Client Secret</strong> in the headers of your requests (<code>X-API-Key</code> and <code>X-API-Secret</code>).
            </p>
            
            <div className="space-y-4">
              <div className="flex flex-col gap-1">
                <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Client ID (API Key)</label>
                <div className="flex gap-4 items-center">
                  <div className="flex-1 bg-slate-950 border border-slate-800 rounded-lg p-3 font-mono text-sm text-emerald-400 overflow-x-auto">
                    {profile.api_key || "Not generated yet"}
                  </div>
                  <button onClick={() => navigator.clipboard.writeText(profile.api_key)} className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-3 rounded-lg text-sm transition-colors whitespace-nowrap">
                    Copy ID
                  </button>
                </div>
              </div>

              <div className="flex flex-col gap-1">
                <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Client Secret (API Secret)</label>
                <div className="flex gap-4 items-center">
                  <div className="flex-1 bg-slate-950 border border-slate-800 rounded-lg p-3 font-mono text-sm text-red-400 overflow-x-auto">
                    {showKey ? profile.api_secret : "mdh_secret_••••••••••••••••••••••••••••••••••••••••••••••••"}
                  </div>
                  <button 
                    onClick={() => setShowKey(!showKey)}
                    className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-3 rounded-lg text-sm transition-colors whitespace-nowrap"
                  >
                    {showKey ? "Hide Secret" : "Reveal Secret"}
                  </button>
                </div>
              </div>
            </div>

            <div className="mt-6 p-4 bg-red-950/20 border border-red-900/30 rounded-lg flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-400 shrink-0" />
              <p className="text-xs text-red-300/80">
                <strong className="text-red-400 block mb-1">Security Warning</strong>
                Your Client Secret grants unlimited access to your account's quota. Treat it like a password. If compromised, malicious actors could drain your API limit.
              </p>
            </div>
          </div>
        )}

        {/* Upgrade Plans */}
        {profile.tier !== "advanced" && (
          <div>
            <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
              <Zap className="w-5 h-5 text-amber-400" /> Upgrade Your Plan
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              {/* Pro Plan */}
              <div className={`bg-slate-900 border ${profile.tier === "pro" ? "border-blue-500" : "border-slate-800"} rounded-2xl p-6 relative flex flex-col`}>
                {profile.tier === "pro" && <div className="absolute top-0 right-0 bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-bl-lg rounded-tr-xl">Current Plan</div>}
                <h3 className="text-2xl font-bold text-white mb-2">Pro</h3>
                <p className="text-slate-400 text-sm mb-6 flex-1">Perfect for engineers who need deeper material comparisons and exports.</p>
                
                <ul className="space-y-3 mb-8">
                  <li className="flex items-center gap-2 text-sm text-slate-300"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Compare up to 5 materials</li>
                  <li className="flex items-center gap-2 text-sm text-slate-300"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Export comparison results to CSV</li>
                  <li className="flex items-center gap-2 text-sm text-slate-300"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Access to AI Material Adviser</li>
                  <li className="flex items-center gap-2 text-sm text-slate-300"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Find alternative equivalent materials</li>
                </ul>
                
                {profile.tier === "free" && (
                  <button 
                    onClick={() => handleUpgrade("pro")}
                    disabled={upgrading || profile.upgrade_status === "pending"}
                    className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:cursor-not-allowed text-white font-bold py-3 rounded-xl transition-colors flex justify-center items-center gap-2"
                  >
                    Request Pro Access <ArrowUpRight className="w-4 h-4" />
                  </button>
                )}
              </div>

              {/* Advanced Plan */}
              <div className="bg-slate-900 border border-emerald-900/50 rounded-2xl p-6 relative flex flex-col overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-emerald-900/10 to-transparent"></div>
                <h3 className="text-2xl font-bold text-white mb-2 relative">Advanced</h3>
                <p className="text-slate-400 text-sm mb-6 flex-1 relative">For enterprises and automation pipelines requiring high-volume data access.</p>
                
                <ul className="space-y-3 mb-8 relative">
                  <li className="flex items-center gap-2 text-sm text-slate-300"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Everything in Pro</li>
                  <li className="flex items-center gap-2 text-sm text-slate-300"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Unlimited material comparisons</li>
                  <li className="flex items-center gap-2 text-sm text-slate-300"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> 10,000 API requests per day</li>
                  <li className="flex items-center gap-2 text-sm text-slate-300"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Programmatic REST API Key</li>
                </ul>
                
                <button 
                  onClick={() => handleUpgrade("advanced")}
                  disabled={upgrading || profile.upgrade_status === "pending"}
                  className="w-full bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 disabled:cursor-not-allowed text-white font-bold py-3 rounded-xl transition-colors flex justify-center items-center gap-2 relative z-10"
                >
                  Request Advanced Access <ArrowUpRight className="w-4 h-4" />
                </button>
              </div>

            </div>
          </div>
        )}

      </div>
    </main>
  );
}
