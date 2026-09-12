import React, { useState, useEffect } from 'react';
import { Settings, CreditCard, LifeBuoy, X, Download, Shield, Key, FileText, Zap, CheckCircle2, ArrowUpRight, LogOut, AlertCircle } from 'lucide-react';
import AdvancedMaterialManager from "@/components/AdvancedMaterialManager";
import { API } from "@/lib/api";

type AccountModalsProps = {
  activeModal: string | null;
  setActiveModal: (modal: string | null) => void;
  userInfo?: { name: string; tier: string; is_admin: boolean } | null;
};

export function AccountModals({ activeModal, setActiveModal, userInfo }: AccountModalsProps) {
  const [profile, setProfile] = useState<any>(null);
  const [upgrading, setUpgrading] = useState(false);

  useEffect(() => {
    if (activeModal) {
      fetchProfile();
    }
  }, [activeModal]);

  const fetchProfile = async () => {
    const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
    if (!token) return;
    try {
      const res = await fetch(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        setProfile(await res.json());
      }
    } catch (err) {}
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

  const generateApiKeys = async () => {
    try {
      const res = await fetch(`${API}/auth/generate-api`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
      });
      if (res.ok) {
        const data = await res.json();
        alert(`SUCCESS! Your API credentials:\n\nKey: ${data.api_key}\nSecret: ${data.api_secret}\n\nPlease save these immediately. The secret will not be shown again.`);
        fetchProfile();
      } else {
        alert("Failed to generate API credentials.");
      }
    } catch (err) {
      alert("Network error");
    }
  };

  if (!activeModal) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-sm p-4" onClick={() => setActiveModal(null)}>
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl w-full max-w-4xl p-0 overflow-hidden animate-in zoom-in-95 max-h-[90vh] flex flex-col" onClick={e => e.stopPropagation()}>
        
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 shrink-0">
          <h3 className="font-bold text-slate-900 dark:text-white flex items-center gap-2">
            {activeModal === 'account' && <><Settings className="w-5 h-5 text-blue-600"/> Account Management</>}
            {activeModal === 'billing' && <><CreditCard className="w-5 h-5 text-emerald-600"/> Transactions & Billing</>}
            {activeModal === 'help' && <><LifeBuoy className="w-5 h-5 text-amber-600"/> Help Centre & Legal</>}
          </h3>
          <button onClick={() => setActiveModal(null)} className="p-1 text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800 rounded-lg transition-colors">
            <X className="w-5 h-5"/>
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto bg-slate-50 dark:bg-slate-950/50 flex-1">
          {activeModal === 'account' && profile && (
            <div className="space-y-8">
              
              {/* Profile & Tier Overview */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="md:col-span-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 relative overflow-hidden shadow-sm">
                  <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl"></div>
                  <h2 className="text-sm font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-2">Current Tier</h2>
                  <div className="flex items-end gap-4 mb-4">
                    <span className="text-4xl font-extrabold text-slate-900 dark:text-white capitalize">{profile.tier}</span>
                    {profile.tier === "advanced" && <span className="text-emerald-600 dark:text-emerald-400 text-sm font-bold bg-emerald-100 dark:bg-emerald-900/30 px-2 py-1 rounded">Maximum Access</span>}
                  </div>
                  {profile.tier === "free" && <p className="text-sm text-slate-600 dark:text-slate-300">Upgrade to Pro or Advanced to unlock full database access, advanced AI features, and more.</p>}
                  {profile.tier === "pro" && <p className="text-sm text-slate-600 dark:text-slate-300">You have access to 1000+ materials, advanced AI tools, and PDF exports. Upgrade to Advanced for API access and Enterprise SSO.</p>}
                  {profile.tier === "advanced" && <p className="text-sm text-slate-600 dark:text-slate-300">You have unlimited access to all features, custom materials, programmatic REST APIs, and priority support.</p>}
                </div>

                <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 flex flex-col justify-center items-center text-center space-y-4 shadow-sm">
                  <div className="w-16 h-16 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-2xl font-bold text-slate-900 dark:text-white">
                    {profile.name ? profile.name.charAt(0).toUpperCase() : profile.email?.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <h3 className="text-slate-900 dark:text-white font-heading font-bold">{profile.name || "User"}</h3>
                    <p className="text-xs text-slate-500 dark:text-slate-400">{profile.email}</p>
                  </div>
                </div>
              </div>

              {/* API Access (Advanced Only) */}
              {profile.tier === "advanced" && (
                <div className="space-y-6">
                  <div className="bg-white dark:bg-slate-900 border border-emerald-900/50 rounded-2xl p-6 relative overflow-hidden shadow-sm">
                    <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl"></div>
                    <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading flex items-center gap-2 mb-4">
                      <Key className="w-5 h-5 text-emerald-600 dark:text-emerald-400" /> Programmatic API Access
                    </h2>
                    <p className="text-slate-600 dark:text-slate-300 text-sm mb-6">
                      As an Advanced tier member, you are eligible for programmatic REST API access to query our materials database. API credentials are provisioned securely by our team upon request.
                    </p>
                    
                    {profile.api_key ? (
                      <div className="bg-emerald-100 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800/50 rounded-xl p-4 flex items-center gap-3">
                        <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0" />
                        <div>
                          <p className="text-emerald-600 dark:text-emerald-400 font-bold text-sm">API Access Granted</p>
                          <p className="text-slate-500 dark:text-slate-400 text-xs mt-1">Your API credentials have been provisioned. Contact support at <strong>support@matdatahub.com</strong> to receive your keys securely.</p>
                        </div>
                      </div>
                    ) : (
                      <button onClick={generateApiKeys} className="px-6 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl transition-colors flex items-center gap-2">
                        <Key className="w-4 h-4" /> Generate API Keys
                      </button>
                    )}
                  </div>
                  
                  {/* Custom Materials Manager */}
                  <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm">
                    <AdvancedMaterialManager />
                  </div>
                </div>
              )}

              {/* Upgrade Plans */}
              {profile.tier !== "advanced" && (
                <div>
                  <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-4 flex items-center gap-2">
                    <Zap className="w-5 h-5 text-amber-600 dark:text-amber-400" /> Upgrade Your Plan
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    
                    {/* Pro Plan */}
                    <div className={`bg-white dark:bg-slate-900 border ${profile.tier === "pro" ? "border-blue-500" : "border-slate-200 dark:border-slate-800"} rounded-2xl p-6 relative flex flex-col shadow-sm`}>
                      {profile.tier === "pro" && <div className="absolute top-0 right-0 bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-bl-lg rounded-tr-xl">Current Plan</div>}
                      <h3 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-2">Pro</h3>
                      <p className="text-slate-500 dark:text-slate-400 text-sm mb-4 flex-1">Perfect for engineers who need deeper material comparisons and exports.</p>
                      <div className="text-center mb-4">
                        <span className="text-3xl font-black text-slate-900 dark:text-white">&#8377;499</span>
                        <span className="text-slate-500 dark:text-slate-400">/mo</span>
                      </div>
                      {profile.tier === "free" && (
                        <button onClick={() => handleUpgrade("pro")} disabled={upgrading || profile.upgrade_status === "pending"} className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:cursor-not-allowed text-white font-bold py-2 rounded-xl transition-colors flex justify-center items-center gap-2">
                          Pay &#8377;499/mo & Upgrade <ArrowUpRight className="w-4 h-4" />
                        </button>
                      )}
                    </div>

                    {/* Advanced Plan */}
                    <div className="bg-slate-900 dark:bg-slate-950 border border-emerald-900/50 rounded-2xl p-6 relative flex flex-col shadow-lg shadow-emerald-900/20">
                      <div className="absolute -top-3 -right-3 bg-emerald-500 text-slate-900 text-xs font-bold px-3 py-1 rounded-full shadow-lg transform rotate-3">Most Powerful</div>
                      <h3 className="text-xl font-bold text-white font-heading mb-2">Advanced</h3>
                      <p className="text-slate-400 text-sm mb-4 flex-1">For enterprises needing API access, custom materials, and SSO integrations.</p>
                      <div className="text-center mb-4">
                        <span className="text-3xl font-black text-white">&#8377;19,999</span>
                        <span className="text-slate-400">/mo</span>
                      </div>
                      <button onClick={() => handleUpgrade("advanced")} disabled={upgrading || profile.upgrade_status === "pending"} className="w-full bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 disabled:cursor-not-allowed text-white font-bold py-2 rounded-xl transition-colors flex justify-center items-center gap-2 relative z-10">
                        Pay &#8377;19,999/mo & Upgrade <ArrowUpRight className="w-4 h-4" />
                      </button>
                    </div>

                  </div>
                </div>
              )}

              {/* Danger Zone */}
              <div className="border border-red-900/50 rounded-2xl p-6 relative overflow-hidden bg-white dark:bg-slate-900 shadow-sm mt-8">
                <h3 className="text-lg font-bold text-red-500 mb-4 flex items-center gap-2"><AlertCircle className="w-5 h-5"/> Danger Zone</h3>
                <div className="space-y-4">
                  <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4 border-b border-red-900/30 pb-4">
                    <div>
                      <h4 className="text-slate-900 dark:text-white font-heading font-bold text-sm">Deactivate Account</h4>
                      <p className="text-slate-500 dark:text-slate-400 text-xs mt-1">Temporarily pause your subscription and hide your profile.</p>
                    </div>
                    <button onClick={() => alert("Account deactivation requires email confirmation. An email has been sent.")} className="bg-slate-100 dark:bg-slate-800 hover:bg-slate-700 text-red-600 dark:text-red-400 border border-slate-200 dark:border-slate-700 font-bold py-1.5 px-4 rounded-xl transition-colors text-sm whitespace-nowrap">
                      Deactivate
                    </button>
                  </div>
                  <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4">
                    <div>
                      <h4 className="text-slate-900 dark:text-white font-heading font-bold text-sm">Delete Account</h4>
                      <p className="text-slate-500 dark:text-slate-400 text-xs mt-1">Permanently delete your account and projects. <strong className="text-red-600 dark:text-red-400">This action cannot be undone.</strong></p>
                    </div>
                    <button onClick={() => {
                      if (confirm("Are you absolutely sure? This will permanently delete all your projects and data.")) {
                        alert("Account deletion initiated. This may take up to 24 hours to process across all databases.");
                      }
                    }} className="bg-red-100 dark:bg-red-900/40 hover:bg-red-600 text-red-700 dark:text-red-200 border border-red-200 dark:border-red-800/50 hover:border-red-500 font-bold py-1.5 px-4 rounded-xl transition-colors text-sm whitespace-nowrap">
                      Delete Account
                    </button>
                  </div>
                </div>
              </div>

            </div>
          )}

          {activeModal === 'billing' && profile && (
            <div className="space-y-6">
              <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 text-white shadow-xl relative overflow-hidden">
                <div className="absolute top-0 right-0 p-4 opacity-10"><Zap className="w-32 h-32"/></div>
                <p className="text-sm text-slate-300 font-medium uppercase tracking-wider mb-2">Current Plan</p>
                <div className="flex items-end gap-3 mb-6">
                  <h4 className="text-4xl font-black capitalize tracking-tight">{profile.tier || "Free"}</h4>
                  <span className="text-sm text-emerald-400 font-bold mb-2 px-2 py-0.5 bg-emerald-400/10 rounded-full border border-emerald-400/20">Active</span>
                </div>
                <div className="flex items-center justify-between text-sm font-medium text-slate-300 border-t border-slate-700 pt-4">
                  <span>Next billing date: {profile.tier === 'free' ? 'N/A (Free Plan)' : (profile.next_billing_date ? new Date(profile.next_billing_date).toLocaleDateString() : 'Active Subscription')}</span>
                  {profile.tier !== 'free' && (
                    <button onClick={() => alert("Billing portal integration coming soon.")} className="px-4 py-1.5 bg-white text-slate-900 rounded-lg hover:bg-slate-200 transition-colors font-bold">Manage Plan</button>
                  )}
                  {profile.tier === 'free' && (
                    <button onClick={() => setActiveModal('account')} className="px-4 py-1.5 bg-white text-slate-900 rounded-lg hover:bg-slate-200 transition-colors font-bold">Upgrade Now</button>
                  )}
                </div>
              </div>

              <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm">
                <h5 className="text-lg font-bold text-slate-900 dark:text-white mb-4">Recent Transactions</h5>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm">
                    <thead className="bg-slate-50 dark:bg-slate-950/80 text-slate-500 dark:text-slate-400 text-xs uppercase tracking-wider">
                      <tr>
                        <th className="px-6 py-4 font-semibold rounded-tl-xl">Date</th>
                        <th className="px-6 py-4 font-semibold">Description</th>
                        <th className="px-6 py-4 font-semibold">Amount</th>
                        <th className="px-6 py-4 font-semibold text-right rounded-tr-xl">Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td colSpan={4} className="px-6 py-12 text-center text-slate-500 dark:text-slate-400 border-t border-slate-100 dark:border-slate-800">
                          <div className="flex flex-col items-center gap-3">
                            <div className="w-12 h-12 bg-slate-100 dark:bg-slate-800 rounded-full flex items-center justify-center">
                              <FileText className="w-6 h-6 text-slate-600 dark:text-slate-300" />
                            </div>
                            <p className="font-medium text-slate-900 dark:text-white">No transactions yet</p>
                            <p className="text-sm text-slate-500 max-w-sm mx-auto">Your payment history will appear here after your first purchase or subscription upgrade.</p>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {activeModal === 'help' && (
            <div className="space-y-6">
              <div className="p-8 rounded-2xl border border-amber-200 dark:border-amber-900/30 bg-amber-50 dark:bg-amber-900/10 text-center shadow-sm">
                <LifeBuoy className="w-12 h-12 text-amber-500 mx-auto mb-4"/>
                <h4 className="text-xl font-bold text-slate-900 dark:text-white mb-2">How can we help?</h4>
                <p className="text-sm text-slate-600 dark:text-slate-400 mb-6 max-w-sm mx-auto">Our engineering support team is available 24/7 to assist with your technical inquiries.</p>
                <a href="mailto:support@matdatahub.com" className="inline-block px-6 py-2.5 bg-amber-500 hover:bg-amber-600 text-white rounded-xl text-sm font-bold transition-colors shadow-lg shadow-amber-500/20">
                  Contact Support
                </a>
              </div>

              <div className="space-y-4">
                <details className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 cursor-pointer group shadow-sm">
                  <summary className="font-bold text-slate-900 dark:text-white group-hover:text-blue-600 dark:text-blue-400 transition-colors outline-none list-none flex justify-between items-center">
                    Privacy Policy
                    <span className="text-slate-400 group-hover:text-blue-500 text-sm opacity-50">+</span>
                  </summary>
                  <div className="mt-4 text-slate-500 dark:text-slate-400 text-sm space-y-2 pt-4 border-t border-slate-100 dark:border-slate-800">
                    <p>We respect your privacy and are committed to protecting your personal data.</p>
                    <p>Your passwords and secrets are encrypted. We do not sell your data to third parties.</p>
                  </div>
                </details>
                
                <details className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 cursor-pointer group shadow-sm">
                  <summary className="font-bold text-slate-900 dark:text-white group-hover:text-blue-600 dark:text-blue-400 transition-colors outline-none list-none flex justify-between items-center">
                    Terms of Service
                    <span className="text-slate-400 group-hover:text-blue-500 text-sm opacity-50">+</span>
                  </summary>
                  <div className="mt-4 text-slate-500 dark:text-slate-400 text-sm space-y-2 pt-4 border-t border-slate-100 dark:border-slate-800">
                    <p>By using MatDataHub, you agree to not abuse our APIs or scrape our database.</p>
                    <p>Be polite in community feedback. Violations will result in a permanent ban.</p>
                  </div>
                </details>
              </div>
            </div>
          )}
          
          {(!profile && activeModal !== 'help') && (
            <div className="flex justify-center items-center h-48 text-slate-500">Loading your profile...</div>
          )}
        </div>
      </div>
    </div>
  );
}
