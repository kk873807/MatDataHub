"use client";
import { useState, useEffect } from "react";
import { Shield, Key, Zap, CheckCircle2, AlertCircle, ArrowUpRight, LogOut, Clock } from "lucide-react";

export default function AccountDashboard() {
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [upgrading, setUpgrading] = useState(false);
  const [error, setError] = useState("");
  const [showKey, setShowKey] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [activeTab, setActiveTab] = useState('account');

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("Not logged in");
      setLoading(false);
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/auth/me", {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setProfile(data);
      } else {
        setError("Session expired. Please log in again.");
        localStorage.removeItem("token");
      }
    } catch (err) {
      setError("Network error fetching profile.");
    } finally {
      setLoading(false);
    }
  };

  const handleUpgrade = async (tier: "pro" | "advanced") => {
    const token = localStorage.getItem("token");
    if (!token) return;
    setUpgrading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/auth/upgrade", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}` 
        },
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

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const email = form.email.value;
    const password = form.password.value;
    const name = form.username ? form.username.value : undefined;

    // Strict Email Validation Regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError("Please enter a valid email address (e.g. name@domain.com).");
      return;
    }

    if (!isLogin) {
      const confirmPassword = form.confirmPassword.value;
      if (password !== confirmPassword) {
        setError("Passwords do not match.");
        return;
      }
      if (password.length < 8 || !/[A-Za-z]/.test(password) || !/[0-9]/.test(password)) {
        setError("Password must be at least 8 characters and contain both letters and numbers.");
        return;
      }
    }
    
    try {
      const endpoint = isLogin ? "/api/v1/auth/login" : "/api/v1/auth/register";
      const payload = isLogin ? { email, password } : { email, password, name };
      const res = await fetch(`http://127.0.0.1:8000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      
      if (res.ok) {
        const data = await res.json();
        localStorage.setItem("token", data.access_token);
        setError("");
        fetchProfile();
      } else {
        const err = await res.json();
        setError(err.detail || "Authentication failed");
      }
    } catch (err) {
      setError("Network error logging in");
    }
  };

  if (loading) return <div className="p-12 text-center text-slate-400">Loading profile...</div>;
  if (!profile) return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] p-6">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 w-full max-w-md shadow-2xl">
        <h2 className="text-2xl font-bold text-white mb-6 text-center">{isLogin ? "Sign In" : "Register"}</h2>
        {error && <div className="mb-4 p-3 bg-red-900/30 border border-red-500/30 text-red-400 text-sm rounded-lg text-center">{error}</div>}
        <form onSubmit={handleAuth} className="space-y-4">
          {!isLogin && (
            <div>
              <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Name</label>
              <input name="username" type="text" required={!isLogin} className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all" />
            </div>
          )}
          <div>
            <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Email</label>
            <input name="email" type="email" required defaultValue={isLogin ? "test@matdatahub.com" : ""} className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all" />
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Password</label>
            <input name="password" type="password" required defaultValue={isLogin ? "password123" : ""} className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all" />
            {!isLogin && (
              <p className="text-[10px] text-slate-500 mt-1">
                Use a strong password with at least 8 characters, including letters, numbers, and special characters.
              </p>
            )}
          </div>
          {!isLogin && (
            <div>
              <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Confirm Password</label>
              <input name="confirmPassword" type="password" required={!isLogin} className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all" />
            </div>
          )}
          <button type="submit" className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-lg transition-colors mt-4">
            {isLogin ? "Sign In" : "Register"}
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-slate-400">
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <button onClick={() => {setIsLogin(!isLogin); setError("");}} className="text-blue-400 hover:text-blue-300 font-semibold underline">
            {isLogin ? "Register here" : "Sign In"}
          </button>
        </p>
      </div>
    </div>
  );

  return (
    <main className="flex flex-col md:flex-row p-6 lg:p-10 w-full min-h-screen gap-8">
      {/* Sidebar */}
      <div className="w-full md:w-64 shrink-0 flex flex-col gap-2">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2 mb-6">
          <Shield className="w-6 h-6 text-blue-400" />
          Settings
        </h1>
        
        <button onClick={() => setActiveTab('account')} className={`text-left px-4 py-3 rounded-lg font-medium transition-colors ${activeTab === 'account' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}>Account Management</button>
        <button onClick={() => setActiveTab('billing')} className={`text-left px-4 py-3 rounded-lg font-medium transition-colors ${activeTab === 'billing' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}>Transaction & Billing</button>
        <button onClick={() => setActiveTab('help')} className={`text-left px-4 py-3 rounded-lg font-medium transition-colors ${activeTab === 'help' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}>Help Center & Legal</button>
        <button onClick={() => setActiveTab('shortcuts')} className={`text-left px-4 py-3 rounded-lg font-medium transition-colors ${activeTab === 'shortcuts' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}>Keyboard Shortcuts</button>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 w-full max-w-4xl space-y-8">
        
        {activeTab === 'account' && (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
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
                    localStorage.removeItem("token");
                    setProfile(null);
                    setIsLogin(true);
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
                  You have access to the MatDataHub REST API for automated queries. You must pass both your <strong>Client ID</strong> and <strong>Client Secret</strong> in the headers of your requests.
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
                        {showKey ? profile.api_secret : "mdh_secret_****************"}
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
                    <h3 className="text-2xl font-bold text-white mb-2 relative">Advanced</h3>
                    <p className="text-slate-400 text-sm mb-6 flex-1 relative">For enterprises and automation pipelines.</p>
                    
                    <ul className="space-y-3 mb-8 relative">
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
            
            {/* Danger Zone */}
            <div className="border border-red-900/50 rounded-2xl p-6 relative overflow-hidden mt-8">
                <h3 className="text-xl font-bold text-red-500 mb-2">Danger Zone</h3>
                <p className="text-slate-400 text-sm mb-6">Deactivating your account will remove your access immediately. This action cannot be undone.</p>
                <button className="bg-red-900/30 hover:bg-red-900/50 text-red-500 border border-red-900/50 font-bold py-2 px-6 rounded-lg transition-colors text-sm">
                    Deactivate Account
                </button>
            </div>
          </div>
        )}

        {activeTab === 'billing' && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h2 className="text-xl font-bold text-white mb-6">Transaction & Billing History</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-950/80 text-slate-400 text-xs uppercase tracking-wider">
                  <tr>
                    <th className="px-6 py-4 font-semibold">Date</th>
                    <th className="px-6 py-4 font-semibold">Description</th>
                    <th className="px-6 py-4 font-semibold">Amount</th>
                    <th className="px-6 py-4 font-semibold text-right">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/50">
                  <tr className="hover:bg-slate-800/30 transition-colors">
                    <td className="px-6 py-4 text-slate-300">Oct 1, 2023</td>
                    <td className="px-6 py-4 text-slate-300">Pro Plan (Annual)</td>
                    <td className="px-6 py-4 text-slate-300">$299.00</td>
                    <td className="px-6 py-4 text-right text-emerald-400">Paid</td>
                  </tr>
                  <tr className="hover:bg-slate-800/30 transition-colors">
                    <td className="px-6 py-4 text-slate-300">Sep 1, 2023</td>
                    <td className="px-6 py-4 text-slate-300">Free Tier Sign Up</td>
                    <td className="px-6 py-4 text-slate-300">$0.00</td>
                    <td className="px-6 py-4 text-right text-emerald-400">Paid</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'help' && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 animate-in fade-in slide-in-from-bottom-4 duration-500 space-y-6">
            <h2 className="text-xl font-bold text-white mb-2">Help Center & Legal</h2>
            
            <div className="space-y-4">
              <details className="bg-slate-950 border border-slate-800 rounded-lg p-4 cursor-pointer group">
                <summary className="font-bold text-white group-hover:text-blue-400 transition-colors">Privacy Policy</summary>
                <div className="mt-4 text-slate-400 text-sm space-y-2">
                  <p>We respect your privacy and are committed to protecting your personal data.</p>
                  <p>Your passwords and secrets are encrypted. We do not sell your data to third parties.</p>
                </div>
              </details>
              
              <details className="bg-slate-950 border border-slate-800 rounded-lg p-4 cursor-pointer group">
                <summary className="font-bold text-white group-hover:text-blue-400 transition-colors">Terms of Service</summary>
                <div className="mt-4 text-slate-400 text-sm space-y-2">
                  <p>By using MatDataHub, you agree to not abuse our APIs or scrape our database.</p>
                  <p>Be polite in community feedback. Violations will result in a permanent ban.</p>
                </div>
              </details>
            </div>
          </div>
        )}

        {activeTab === 'shortcuts' && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h2 className="text-xl font-bold text-white mb-6">Keyboard Shortcuts</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="flex justify-between items-center p-3 border-b border-slate-800">
                <span className="text-slate-300 text-sm">Global Search</span>
                <kbd className="bg-slate-800 text-slate-300 px-2 py-1 rounded text-xs font-mono">Ctrl + K</kbd>
              </div>
              <div className="flex justify-between items-center p-3 border-b border-slate-800">
                <span className="text-slate-300 text-sm">Navigate Dashboard</span>
                <kbd className="bg-slate-800 text-slate-300 px-2 py-1 rounded text-xs font-mono">G + D</kbd>
              </div>
              <div className="flex justify-between items-center p-3 border-b border-slate-800">
                <span className="text-slate-300 text-sm">Navigate Compare</span>
                <kbd className="bg-slate-800 text-slate-300 px-2 py-1 rounded text-xs font-mono">G + C</kbd>
              </div>
              <div className="flex justify-between items-center p-3 border-b border-slate-800">
                <span className="text-slate-300 text-sm">Toggle Sidebar</span>
                <kbd className="bg-slate-800 text-slate-300 px-2 py-1 rounded text-xs font-mono">[ ]</kbd>
              </div>
            </div>
          </div>
        )}

      </div>
    </main>
  );
}
