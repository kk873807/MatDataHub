"use client";
import { useState } from "react";
import { useEffect } from "react";
import { ShieldAlert, Check, X, Lock, Users, MessageSquare, FileText, Plus, Database, ShieldCheck } from "lucide-react";
import { API } from "@/lib/api";
import MaterialManager from "@/components/MaterialManager";
import BlogEditor from "@/components/BlogEditor";

export default function AdminDashboard() {
  const [secret, setSecret] = useState("");
  const [authed, setAuthed] = useState(false);
  const [profile, setProfile] = useState<any>(null);
  const [requests, setRequests] = useState<any[]>([]);
  const [feedback, setFeedback] = useState<any[]>([]);
  const [contributions, setContributions] = useState<any[]>([]);
  const [transactions, setTransactions] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [expandedUsers, setExpandedUsers] = useState<Record<number, boolean>>({});
  const toggleExpand = (userId: number) => setExpandedUsers(prev => ({ ...prev, [userId]: !prev[userId] }));

  useEffect(() => {
    checkAdmin();
  }, []);

  const checkAdmin = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      setLoading(false);
      return;
    }
    
    try {
      const res = await fetch(`${API}/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
      if (res.ok) {
        const data = await res.json();
        setProfile(data);
        if (data.is_admin) {
          setAuthed(true);
          fetchAdminData(token);
        }
      }
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const handleClaimAdmin = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    try {
      const res = await fetch(`${API}/auth/make-me-admin`, {
        method: "POST",
        headers: { "X-Admin-Secret": secret, "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        window.location.reload();
      } else {
        setError("Invalid system secret.");
      }
    } catch (e) {
      setError("Network error");
    }
  };

  const fetchAdminData = async (token: string) => {
    setLoading(true);
    try {
      const [reqRes, feedRes, contribRes, txnRes] = await Promise.all([
        fetch(`${API}/admin/upgrade-requests`, {
          headers: { "Authorization": `Bearer ${token}` }
        }),
        fetch(`${API}/feedback/`, {
          headers: { "Authorization": `Bearer ${token}` }
        }),
        fetch(`${API}/admin/user-contributions`, {
          headers: { "Authorization": `Bearer ${token}` }
        }),
        fetch(`${API}/admin/transactions`, {
          headers: { "Authorization": `Bearer ${token}` }
        })
      ]);

      if (reqRes.ok) {
        setRequests(await reqRes.json());
      } else {
        setAuthed(false);
        setError("Invalid Admin Secret.");
      }

      if (feedRes.ok) {
        setFeedback(await feedRes.json());
      }
      
      if (contribRes.ok) {
        const c = await contribRes.json();
        setContributions(c.users || []);
      }
      
      if (txnRes.ok) {
        setTransactions(await txnRes.json());
      }
      
    } catch (err) {
      console.error(err);
      setError("Network Error");
    } finally {
      setLoading(false);
    }
  };

    const handleMaterialAction = async (contribId: number, action: "approve" | "reject") => {
    try {
      const res = await fetch(`${API}/admin/contributions/${contribId}/${action}`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
      });
      if (res.ok) {
        fetchAdminData(localStorage.getItem("token") || "");
      } else {
        const err = await res.json();
        alert(err.detail || "Failed to perform action");
      }
    } catch (err) {
      alert("Network error.");
    }
  };

  const handleAction = async (userId: number, action: "approve" | "reject") => {
    try {
      const res = await fetch(`${API}/admin/upgrade-requests/${userId}/${action}`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
      });
      if (res.ok) {
        // Refresh list
        fetchAdminData(localStorage.getItem("token") || "");
      } else {
        const err = await res.json();
        alert(err.detail || "Failed to perform action");
      }
    } catch (err) {
      alert("Network error.");
    }
  };

  const handleFeedbackAction = async (fbId: number, action: "delete" | "hide" | "resolve", userId?: number) => {
    try {
      let url = `${API}/feedback/${fbId}`;
      let method = "DELETE";
      if (action === "hide") { url += "/visibility"; method = "PATCH"; }
      if (action === "resolve") { url += "/resolve"; method = "POST"; }
      
      const res = await fetch(url, { method, headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` } });
      if (res.ok) fetchAdminData(localStorage.getItem("token") || "");
    } catch (err) {
      console.error(err);
    }
  };

  const handleBlockUser = async (userId: number) => {
    if (!confirm("Are you sure you want to block this user?")) return;
    try {
      const res = await fetch(`${API}/admin/users/${userId}/block`, {
        method: "POST", headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
      });
      if (res.ok) {
        alert("User blocked successfully.");
        fetchAdminData(localStorage.getItem("token") || "");
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleReply = async (fbId: number) => {
    const replyText = prompt("Enter official admin reply:");
    if (!replyText) return;
    try {
      const res = await fetch(`${API}/feedback/${fbId}/reply`, {
        method: "POST",
        headers: { "X-Admin-Secret": secret, "Content-Type": "application/json" },
        body: JSON.stringify({ reply_text: replyText })
      });
      if (res.ok) fetchAdminData(localStorage.getItem("token") || "");
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <div className="p-12 text-center text-slate-500">Loading Admin Dashboard...</div>;

  if (!profile) {
    return (
      <main className="flex justify-center items-center min-h-[80vh] p-6">
        <div className="text-center space-y-4">
          <ShieldAlert className="w-12 h-12 text-red-500 mx-auto" />
          <h1 className="text-2xl font-bold">Access Denied</h1>
          <p className="text-slate-500">You must be logged in to view this page.</p>
          <button onClick={() => window.location.href='/?login=true'} className="px-6 py-2 bg-blue-600 text-white rounded-xl">Go to Login</button>
        </div>
      </main>
    );
  }

  if (!authed) {
    return (
      <main className="flex justify-center items-center min-h-[80vh] p-6">
        <form onSubmit={handleClaimAdmin} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 rounded-2xl w-full max-w-sm shadow-2xl flex flex-col gap-6">
          <div className="flex justify-center">
            <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 text-blue-600 rounded-full flex items-center justify-center">
              <ShieldCheck className="w-8 h-8" />
            </div>
          </div>
          <div className="text-center space-y-2">
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white font-heading">Claim Admin Rights</h1>
            <p className="text-slate-500 dark:text-slate-400 text-sm">Enter the root system secret to permanently make {profile.email} an admin.</p>
          </div>
          
          <div className="space-y-4">
            <div>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input 
                  type="password"
                  value={secret}
                  onChange={e => setSecret(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 focus:ring-2 focus:ring-blue-500 outline-none transition-shadow"
                  placeholder="System Secret (ADMIN_SECRET)"
                  autoFocus
                />
              </div>
            </div>
            
            {error && <p className="text-red-500 text-sm font-medium text-center">{error}</p>}
            
            <button 
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-slate-900 hover:bg-slate-800 dark:bg-blue-600 dark:hover:bg-blue-700 text-white rounded-xl font-bold transition-colors disabled:opacity-50"
            >
              Make Me Admin
            </button>
          </div>
        </form>
      </main>
    );
  }

  return (
    <main className="flex flex-col p-6 lg:p-10 w-full min-h-screen">
      <div className="w-full max-w-6xl mx-auto space-y-8">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white font-heading flex items-center gap-3">
            <ShieldAlert className="w-8 h-8 text-red-500" />
            Admin Operations
          </h1>
          <button onClick={() => setAuthed(false)} className="text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white text-sm">Lock Session</button>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-500 dark:text-slate-400">Loading admin data...</div>
        ) : (
          <div className="space-y-8">
            
            <MaterialManager />
            
            {/* Billing & Transactions */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden shadow-xl">
              <div className="p-6 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50 dark:bg-slate-950/50">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-emerald-100 dark:bg-emerald-900/30 rounded-xl flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-emerald-600 dark:text-emerald-400"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>
                  </div>
                  <div>
                    <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading">Financial Ledger</h2>
                    <p className="text-sm text-slate-500 dark:text-slate-400">All Razorpay transactions & upgrades</p>
                  </div>
                </div>
                <span className="bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 py-1 px-3 rounded-full text-sm font-bold">
                  {transactions.length} Records
                </span>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 dark:bg-slate-950/80 text-slate-500 dark:text-slate-400 text-xs uppercase tracking-wider">
                    <tr>
                      <th className="px-6 py-4 font-semibold">Date</th>
                      <th className="px-6 py-4 font-semibold">User Email</th>
                      <th className="px-6 py-4 font-semibold">Tier</th>
                      <th className="px-6 py-4 font-semibold">Amount</th>
                      <th className="px-6 py-4 font-semibold">Razorpay ID</th>
                      <th className="px-6 py-4 font-semibold text-right">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {transactions.length === 0 ? (
                      <tr>
                        <td colSpan={6} className="px-6 py-8 text-center text-slate-500">No transactions recorded yet.</td>
                      </tr>
                    ) : (
                      transactions.map(txn => (
                        <tr key={txn.id} className="border-t border-slate-100 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-900/50">
                          <td className="px-6 py-4 whitespace-nowrap">{new Date(txn.created_at).toLocaleString()}</td>
                          <td className="px-6 py-4 font-medium">{txn.user_email}</td>
                          <td className="px-6 py-4 capitalize">{txn.tier_purchased}</td>
                          <td className="px-6 py-4 font-bold text-slate-900 dark:text-white">&#8377;{txn.amount.toLocaleString()}</td>
                          <td className="px-6 py-4 text-xs font-mono text-slate-500">{txn.payment_id || "N/A"}</td>
                          <td className="px-6 py-4 text-right">
                            <span className={`text-xs font-bold uppercase px-2 py-1 rounded-full ${txn.status === 'completed' ? 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30' : 'bg-red-100 text-red-600 dark:bg-red-900/30'}`}>
                              {txn.status}
                            </span>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {/* User Contributions */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden shadow-xl">
              <div className="p-6 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50 dark:bg-slate-950/50">
                <div className="flex items-center gap-3">
                  <Database className="w-5 h-5 text-cyan-500" />
                  <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading">User Material Contributions</h2>
                </div>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 dark:bg-slate-950/80 text-slate-500 dark:text-slate-400 text-xs uppercase tracking-wider">
                    <tr>
                      <th className="px-6 py-4 font-semibold">User</th>
                      <th className="px-6 py-4 font-semibold text-center">Total Added</th>
                      <th className="px-6 py-4 font-semibold">Materials (Latest 5)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/50">
                    {contributions.map((c: any) => (
                      <tr key={c.user.id} className="hover:bg-slate-100 dark:hover:bg-slate-800/30 transition-colors">
                        <td className="px-6 py-4">
                          <div className="font-bold text-slate-900 dark:text-white">{c.user.name}</div>
                          <div className="text-slate-500 dark:text-slate-400 text-xs">{c.user.email}</div>
                          <div className="mt-1 text-[10px] uppercase font-bold text-slate-500 bg-slate-200 dark:bg-slate-800 inline-block px-1 rounded">{c.user.tier}</div>
                        </td>
                        <td className="px-6 py-4 text-center">
                          <span className="text-lg font-bold text-cyan-600 dark:text-cyan-400 bg-cyan-100 dark:bg-cyan-900/30 px-3 py-1 rounded-full">
                            {c.materials.length}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex flex-wrap gap-2">
                            {c.materials.slice(0, 5).map((m: any) => (
                              <div key={m.id} className={`border rounded-lg p-2 text-xs flex flex-col ${m.status === 'approved' ? 'bg-emerald-50 dark:bg-emerald-900/30 border-emerald-200 dark:border-emerald-800' : m.status === 'rejected' ? 'bg-red-50 dark:bg-red-900/30 border-red-200 dark:border-red-800' : 'bg-slate-100 dark:bg-slate-800 border-slate-200 dark:border-slate-700'}`}>
                                <div>
                                  <span className="font-semibold block line-clamp-1 dark:text-white">{m.name}</span>
                                  <span className="text-slate-500 dark:text-slate-400 text-[10px]">{m.category}</span>
                                </div>
                                {m.status === 'pending' && (
                                  <div className="flex gap-1 mt-2">
                                    <button onClick={() => handleMaterialAction(m.id, 'approve')} className="bg-emerald-500 hover:bg-emerald-600 text-white rounded px-2 py-0.5 text-[10px] transition-colors">Approve</button>
                                    <button onClick={() => handleMaterialAction(m.id, 'reject')} className="bg-red-500 hover:bg-red-600 text-white rounded px-2 py-0.5 text-[10px] transition-colors">Reject</button>
                                  </div>
                                )}
                                {m.status !== 'pending' && (
                                  <span className={`text-[9px] uppercase font-bold mt-1 ${m.status === 'approved' ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'}`}>{m.status}</span>
                                )}
                              </div>
                            ))}
                            {c.materials.length > 5 && (
                              <div className="bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs flex items-center justify-center font-bold text-slate-500">
                                +{c.materials.length - 5} more
                              </div>
                            )}
                          </div>
                        </td>
                      </tr>
                    ))}
                    {contributions.length === 0 && (
                      <tr><td colSpan={3} className="px-6 py-12 text-center text-slate-500 dark:text-slate-400">No custom materials contributed yet.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
            
            {/* Upgrade Requests */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden shadow-xl">
              <div className="p-6 border-b border-slate-200 dark:border-slate-800 flex items-center gap-3 bg-slate-50 dark:bg-slate-950/50">
                <Users className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading">Pending Upgrade Requests</h2>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 dark:bg-slate-950/80 text-slate-500 dark:text-slate-400 text-xs uppercase tracking-wider">
                    <tr>
                      <th className="px-6 py-4 font-semibold">User</th>
                      <th className="px-6 py-4 font-semibold">Current Tier</th>
                      <th className="px-6 py-4 font-semibold">Requested Tier</th>
                      <th className="px-6 py-4 font-semibold">Timestamp</th>
                      <th className="px-6 py-4 font-semibold text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/50">
                    {requests.map((req) => (
                      <tr key={req.id} className="hover:bg-slate-100 dark:hover:bg-slate-800/30 transition-colors">
                        <td className="px-6 py-4">
                          <div className="font-bold text-slate-900 dark:text-white">{req.name}</div>
                          <div className="text-slate-500 dark:text-slate-400 text-xs">{req.email}</div>
                        </td>
                        <td className="px-6 py-4 text-slate-600 dark:text-slate-300 uppercase text-xs">{req.current_tier}</td>
                        <td className="px-6 py-4 font-bold text-amber-600 dark:text-amber-400 uppercase text-xs">{req.requested_tier}</td>
                        <td className="px-6 py-4 text-slate-500 dark:text-slate-400 text-xs">{new Date(req.requested_at).toLocaleString('en-GB')}</td>
                        <td className="px-6 py-4 text-right space-x-2">
                          <button onClick={() => handleAction(req.id, "reject")} className="bg-red-100 dark:bg-red-100 dark:bg-red-900/30 hover:bg-red-100 dark:bg-red-100 dark:bg-red-900/50 text-red-600 dark:text-red-400 px-3 py-1.5 rounded-2xl transition-colors inline-flex items-center gap-1">
                            <X className="w-3 h-3" /> Reject
                          </button>
                          <button onClick={() => handleAction(req.id, "approve")} className="bg-emerald-100  dark:bg-emerald-900/30 hover:bg-emerald-100  dark:bg-emerald-900/50 text-emerald-600 dark:text-emerald-400 px-3 py-1.5 rounded-2xl transition-colors inline-flex items-center gap-1">
                            <Check className="w-3 h-3" /> Approve
                          </button>
                        </td>
                      </tr>
                    ))}
                    {requests.length === 0 && (
                      <tr><td colSpan={5} className="px-6 py-12 text-center text-slate-500 dark:text-slate-400">No pending requests.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Feedback & Support */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden shadow-xl">
              <div className="p-6 border-b border-slate-200 dark:border-slate-800 flex items-center gap-3 bg-slate-50 dark:bg-slate-950/50">
                <MessageSquare className="w-5 h-5 text-blue-600 dark:text-blue-600 dark:text-blue-400" />
                <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading">System Feedback & Tickets</h2>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-50 dark:bg-slate-950/80 text-slate-500 dark:text-slate-400 text-xs uppercase tracking-wider">
                    <tr>
                      <th className="px-6 py-4 font-semibold">Category</th>
                      <th className="px-6 py-4 font-semibold">Content</th>
                      <th className="px-6 py-4 font-semibold">User</th>
                      <th className="px-6 py-4 font-semibold">Status</th>
                      <th className="px-6 py-4 font-semibold text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/50">
                    {feedback.map((fb) => (
                      <tr key={fb.id} className="hover:bg-slate-100 dark:hover:bg-slate-800/30 transition-colors">
                        <td className="px-6 py-4 text-slate-600 dark:text-slate-300 font-medium capitalize">{fb.category}</td>
                        <td className="px-6 py-4 text-slate-500 dark:text-slate-400 max-w-md">
                          <p className="line-clamp-2">{fb.message}</p>
                          {fb.admin_reply && <p className="text-xs text-blue-600 dark:text-blue-400 mt-1">Admin Reply: {fb.admin_reply}</p>}
                        </td>
                        <td className="px-6 py-4 text-slate-500 dark:text-slate-400 text-xs">
                          {fb.email || fb.name || "Anonymous"}
                          {fb.user_id && (
                            <button onClick={() => handleBlockUser(fb.user_id)} className="block text-red-500 hover:underline mt-1">Block User</button>
                          )}
                        </td>
                        <td className="px-6 py-4 text-slate-500 dark:text-slate-400 text-xs">
                          {fb.status === "hidden" ? <span className="text-red-600 dark:text-red-400">Hidden</span> : <span className="text-emerald-600 dark:text-emerald-400">Visible</span>}
                        </td>
                        <td className="px-6 py-4 text-right space-x-2 space-y-1">
                          <button onClick={() => handleReply(fb.id)} className="bg-blue-100 dark:bg-blue-100 dark:bg-blue-900/30 hover:bg-blue-100 dark:bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 px-2 py-1 rounded transition-colors text-xs">Reply</button>
                          <button onClick={() => handleFeedbackAction(fb.id, "hide")} className="bg-slate-700 hover:bg-slate-600 text-slate-900 dark:text-white px-2 py-1 rounded transition-colors text-xs">Toggle Hide</button>
                          <button onClick={() => handleFeedbackAction(fb.id, "delete")} className="bg-red-100 dark:bg-red-100 dark:bg-red-900/30 hover:bg-red-100 dark:bg-red-100 dark:bg-red-900/50 text-red-600 dark:text-red-400 px-2 py-1 rounded transition-colors text-xs">Delete</button>
                        </td>
                      </tr>
                    ))}
                    {feedback.length === 0 && (
                      <tr><td colSpan={5} className="px-6 py-12 text-center text-slate-500 dark:text-slate-400">No feedback entries found.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            <BlogEditor />

            {/* Admin Management */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden shadow-xl">
              <div className="p-6 border-b border-slate-200 dark:border-slate-800 flex items-center gap-3 bg-slate-50 dark:bg-slate-950/50">
                <ShieldCheck className="w-5 h-5 text-purple-600" />
                <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading">Admin Management</h2>
              </div>
              <div className="p-6 space-y-4">
                <p className="text-sm text-slate-500 dark:text-slate-400">Grant admin rights to another registered user by entering their email address. You can also revoke admin rights later.</p>
                <form onSubmit={async (e) => {
                  e.preventDefault();
                  const email = (e.currentTarget.elements.namedItem("target_email") as HTMLInputElement).value;
                  if (!email) return;
                  if (!confirm(`Grant admin rights to ${email}?`)) return;
                  try {
                    const res = await fetch(`${API}/admin/transfer`, {
                      method: "POST",
                      headers: { "Content-Type": "application/json", "Authorization": `Bearer ${localStorage.getItem("token")}` },
                      body: JSON.stringify({ target_email: email }),
                    });
                    const data = await res.json();
                    if (res.ok) { alert(data.message); (e.target as HTMLFormElement).reset(); }
                    else alert(data.detail || "Failed to transfer admin rights.");
                  } catch (err) { alert("Network error"); }
                }} className="flex gap-3 items-end">
                  <div className="flex-1">
                    <label className="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1">User Email</label>
                    <input type="email" name="target_email" required placeholder="user@example.com" className="w-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-purple-500" />
                  </div>
                  <button type="submit" className="bg-purple-600 hover:bg-purple-500 text-white font-semibold py-2 px-5 rounded-lg transition-colors whitespace-nowrap">Grant Admin</button>
                </form>
              </div>
            </div>

          </div>
        )}
      </div>
    </main>
  );
}
