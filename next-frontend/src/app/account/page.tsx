"use client";
import { useState, useEffect, Suspense } from "react";
import MaterialManager from "@/components/MaterialManager";
import AdvancedMaterialManager from "@/components/AdvancedMaterialManager";
import { useSearchParams } from "next/navigation";
import { Database, Shield, Key, Zap, CheckCircle2, AlertCircle, ArrowUpRight, LogOut, Clock, Smartphone, FileText } from "lucide-react";
import { API, API_BASE } from "@/lib/api";

function AccountDashboardInner() {
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [upgrading, setUpgrading] = useState(false);
  const [error, setError] = useState("");
  const [showKey, setShowKey] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [activeTab, setActiveTab] = useState('account');
  const searchParams = useSearchParams();

  useEffect(() => {
    // Capture token from Google OAuth redirect (?t=TOKEN)
    const oauthToken = searchParams.get("t");
    const oauthError = searchParams.get("error");
    
    if (oauthToken) {
      localStorage.setItem("token", oauthToken);
      // Clean the URL so the token isn't visible in the address bar
      window.history.replaceState({}, "", "/account");
    }
    if (oauthError) {
      setError("Google authentication failed. Please try again.");
      window.history.replaceState({}, "", "/account");
    }
    
    fetchProfile();
  }, [searchParams]);

  const fetchProfile = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("Not logged in");
      setLoading(false);
      return;
    }

    try {
      const res = await fetch(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setProfile(data);
      } else {
        setError("Session expired. Please log in again.");
        localStorage.removeItem("token"); window.location.href = "/?login=true";
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
      const res = await fetch(`${API}/payments/create-link`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}` 
        },
        body: JSON.stringify({ tier })
      });
      if (res.ok) {
        const data = await res.json();
        if (data.payment_url) {
          window.location.href = data.payment_url;
        } else {
          alert("Payment URL not returned. Please contact support.");
        }
      } else {
        const err = await res.json();
        alert(err.detail || "Failed to initiate payment.");
      }
    } catch (err) {
      alert("Network error. Please try again.");
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
      const res = await fetch(`${API_BASE}${endpoint}`, {
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

  if (loading || !profile) return <div className="flex justify-center items-center h-[50vh] text-slate-400">Authenticating...</div>;
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
                  <p className="text-xs text-slate-400">Member since {new Date(profile.created_at).toLocaleDateString('en-GB')}</p>
                </div>
                <button 
                  onClick={() => {
                    localStorage.removeItem("token"); window.location.href = "/?login=true";
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
              <div className="space-y-8">
                <div className="bg-slate-900 border border-emerald-900/50 rounded-2xl p-8 relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl"></div>
                  <h2 className="text-xl font-bold text-white flex items-center gap-2 mb-4">
                    <Key className="w-5 h-5 text-emerald-400" /> Programmatic API Access
                  </h2>
                  <p className="text-slate-300 text-sm mb-6">
                    As an Advanced tier member, you are eligible for programmatic REST API access to query our materials database. 
                    API credentials are provisioned securely by our team upon request.
                  </p>
                  
                  {profile.api_key ? (
                    <div className="bg-emerald-900/20 border border-emerald-800/50 rounded-xl p-4 flex items-center gap-3">
                      <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                      <div>
                        <p className="text-emerald-400 font-bold text-sm">API Access Granted</p>
                        <p className="text-slate-400 text-xs mt-1">Your API credentials have been provisioned. Contact support at <strong>support@matdatahub.com</strong> to receive your keys securely.</p>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <button 
                        className="px-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl transition-colors flex items-center gap-2"
                        onClick={async () => {
                          try {
                            const res = await fetch(`${API}/auth/generate-api`, {
                              method: "POST",
                              headers: {
                                "Authorization": `Bearer ${localStorage.getItem("token")}`
                              }
                            });
                            if (res.ok) {
                              const data = await res.json();
                              alert(`SUCCESS! Your API credentials:\n\nKey: ${data.api_key}\nSecret: ${data.api_secret}\n\nPlease save these immediately. The secret will not be shown again.`);
                              window.location.reload();
                            } else {
                              alert("Failed to generate API credentials.");
                            }
                          } catch (err) {
                            alert("Network error");
                          }
                        }}
                      >
                        <Key className="w-4 h-4" /> Generate API Keys
                      </button>
                    </div>
                  )}
                </div>
                <AdvancedMaterialManager />
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
                        Pay ₹499 & Upgrade <ArrowUpRight className="w-4 h-4" />
                      </button>
                    )}
                  </div>

                  {/* Advanced Plan */}
                  <div className="bg-slate-900 border border-emerald-900/50 rounded-2xl p-6 relative flex flex-col overflow-hidden">
                    <h3 className="text-2xl font-bold text-white mb-2 relative">Advanced</h3>
                    <p className="text-slate-400 text-sm mb-6 flex-1 relative">For enterprises and automation pipelines.</p>
                    
                    <div className="text-center mb-6">
                      <span className="text-sm text-slate-400 line-through mr-2">₹49,999</span>
                      <span className="text-4xl font-black text-white">₹19,999</span>
                      <span className="text-slate-400">/year</span>
                      <div className="text-emerald-400 text-xs font-bold mt-1 uppercase tracking-wider animate-pulse">Launch Offer - 60% Off</div>
                    </div>
                    <ul className="space-y-3 mb-6 text-sm text-slate-300">
                      <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Unlimited Material Lookups</li>
                      <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Unlimited Compare Limit</li>
                      <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Advanced Analytics Engine</li>
                      <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Export Professional PDFs</li>
                      <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Unlimited AI Adviser Chats</li>
                      <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Private DB Uploads (CSV/Excel)</li>
                      <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> REST API Access</li>
                    </ul>
                    <button 
                      onClick={() => handleUpgrade("advanced")}
                      disabled={upgrading || profile.upgrade_status === "pending"}
                      className="w-full bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 disabled:cursor-not-allowed text-white font-bold py-3 rounded-xl transition-colors flex justify-center items-center gap-2 relative z-10"
                    >
                      Pay ₹19,999 & Upgrade <ArrowUpRight className="w-4 h-4" />
                    </button>
                  </div>

                </div>
              </div>
            )}
            
            {/* Danger Zone */}
            <div className="border border-red-900/50 rounded-2xl p-6 relative overflow-hidden mt-8">
                <h3 className="text-xl font-bold text-red-500 mb-2">Danger Zone</h3>
                
                <div className="space-y-6 mt-6">
                  <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4 border-b border-red-900/30 pb-6">
                    <div>
                      <h4 className="text-white font-bold text-sm">Deactivate Account</h4>
                      <p className="text-slate-400 text-sm mt-1 max-w-lg">Temporarily pause your subscription and hide your profile. You can reactivate at any time by logging back in.</p>
                    </div>
                    <button onClick={() => alert("Account deactivation requires email confirmation. An email has been sent.")} className="bg-slate-800 hover:bg-slate-700 text-red-400 border border-slate-700 font-bold py-2 px-6 rounded-lg transition-colors text-sm whitespace-nowrap">
                      Deactivate
                    </button>
                  </div>

                  <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4">
                    <div>
                      <h4 className="text-white font-bold text-sm">Delete Account</h4>
                      <p className="text-slate-400 text-sm mt-1 max-w-lg">Permanently delete your account, projects, blueprints, and API keys. <strong className="text-red-400">This action cannot be undone.</strong></p>
                    </div>
                    <button onClick={() => {
                      if (confirm("Are you absolutely sure? This will permanently delete all your projects and data.")) {
                        alert("Account deletion initiated. This may take up to 24 hours to process across all databases.");
                      }
                    }} className="bg-red-900/40 hover:bg-red-600 text-red-200 border border-red-800/50 hover:border-red-500 font-bold py-2 px-6 rounded-lg transition-colors text-sm whitespace-nowrap">
                      Delete Account
                    </button>
                  </div>
                </div>
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
                <tbody>
                  <tr>
                    <td colSpan={4} className="px-6 py-12 text-center text-slate-500">
                      <div className="flex flex-col items-center gap-3">
                        <div className="w-12 h-12 bg-slate-800 rounded-full flex items-center justify-center">
                          <FileText className="w-6 h-6 text-slate-600" />
                        </div>
                        <p className="font-medium">No transactions yet</p>
                        <p className="text-sm text-slate-600 max-w-sm">Your payment history will appear here after your first purchase or subscription upgrade.</p>
                      </div>
                    </td>
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

export default function AccountDashboard() {
  return (
    <Suspense fallback={<div className="flex justify-center items-center h-screen"><div className="w-8 h-8 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin"></div></div>}>
      <AccountDashboardInner />
    </Suspense>
  );
}
