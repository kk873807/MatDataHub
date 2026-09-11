"use client";
import { useState } from "react";
import { ShieldAlert, Check, X, Lock, Users, MessageSquare, FileText, Plus } from "lucide-react";
import { API } from "@/lib/api";
import MaterialManager from "@/components/MaterialManager";
import BlogEditor from "@/components/BlogEditor";

export default function AdminDashboard() {
  const [secret, setSecret] = useState("");
  const [authed, setAuthed] = useState(false);
  const [requests, setRequests] = useState<any[]>([]);
  const [feedback, setFeedback] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (!secret) return;
    setAuthed(true);
    fetchAdminData(secret);
  };

  const fetchAdminData = async (adminSecret: string) => {
    setLoading(true);
    try {
      const [reqRes, feedRes] = await Promise.all([
        fetch(`${API}/admin/upgrade-requests`, {
          headers: { "X-Admin-Secret": adminSecret }
        }),
        fetch(`${API}/feedback/`, {
          headers: { "X-Admin-Secret": adminSecret }
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
    } catch (err) {
      setError("Network error fetching admin data.");
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (userId: number, action: "approve" | "reject") => {
    try {
      const res = await fetch(`${API}/admin/upgrade-requests/${userId}/${action}`, {
        method: "POST",
        headers: { "X-Admin-Secret": secret }
      });
      if (res.ok) {
        // Refresh list
        fetchAdminData(secret);
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
      
      const res = await fetch(url, { method, headers: { "X-Admin-Secret": secret } });
      if (res.ok) fetchAdminData(secret);
    } catch (err) {
      console.error(err);
    }
  };

  const handleBlockUser = async (userId: number) => {
    if (!confirm("Are you sure you want to block this user?")) return;
    try {
      const res = await fetch(`${API}/admin/users/${userId}/block`, {
        method: "POST", headers: { "X-Admin-Secret": secret }
      });
      if (res.ok) {
        alert("User blocked successfully.");
        fetchAdminData(secret);
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
      if (res.ok) fetchAdminData(secret);
    } catch (err) {
      console.error(err);
    }
  };

  if (!authed) {
    return (
      <main className="flex flex-col items-center justify-center min-h-[80vh] p-6">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 w-full max-w-md shadow-2xl">
          <div className="w-16 h-16 bg-red-900/30 rounded-full flex items-center justify-center mx-auto mb-6">
            <ShieldAlert className="w-8 h-8 text-red-500" />
          </div>
          <h1 className="text-2xl font-bold text-white text-center mb-2">Admin Portal</h1>
          <p className="text-slate-400 text-sm text-center mb-8">Restricted access. Enter your administrative secret to proceed.</p>
          
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <input 
                type="password" 
                value={secret} 
                onChange={e => setSecret(e.target.value)} 
                placeholder="ADMIN_SECRET"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-3 text-white focus:border-red-500 transition-colors outline-none"
                required
              />
            </div>
            {error && <p className="text-red-400 text-sm text-center">{error}</p>}
            <button type="submit" className="w-full bg-red-600 hover:bg-red-500 text-white font-bold py-3 rounded-lg transition-colors flex justify-center items-center gap-2">
              <Lock className="w-4 h-4" /> Authenticate
            </button>
          </form>
        </div>
      </main>
    );
  }

  return (
    <main className="flex flex-col p-6 lg:p-10 w-full min-h-screen">
      <div className="w-full max-w-6xl mx-auto space-y-8">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            <ShieldAlert className="w-8 h-8 text-red-500" />
            Admin Operations
          </h1>
          <button onClick={() => setAuthed(false)} className="text-slate-400 hover:text-white text-sm">Lock Session</button>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-400">Loading admin data...</div>
        ) : (
          <div className="space-y-8">
            
            <MaterialManager secret={secret} />
            
            {/* Upgrade Requests */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
              <div className="p-6 border-b border-slate-800 flex items-center gap-3 bg-slate-950/50">
                <Users className="w-5 h-5 text-blue-400" />
                <h2 className="text-xl font-bold text-white">Pending Upgrade Requests</h2>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-950/80 text-slate-400 text-xs uppercase tracking-wider">
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
                      <tr key={req.id} className="hover:bg-slate-800/30 transition-colors">
                        <td className="px-6 py-4">
                          <div className="font-bold text-white">{req.name}</div>
                          <div className="text-slate-500 text-xs">{req.email}</div>
                        </td>
                        <td className="px-6 py-4 text-slate-300 uppercase text-xs">{req.current_tier}</td>
                        <td className="px-6 py-4 font-bold text-amber-400 uppercase text-xs">{req.requested_tier}</td>
                        <td className="px-6 py-4 text-slate-500 text-xs">{new Date(req.requested_at).toLocaleString('en-GB')}</td>
                        <td className="px-6 py-4 text-right space-x-2">
                          <button onClick={() => handleAction(req.id, "reject")} className="bg-red-900/30 hover:bg-red-900/50 text-red-400 px-3 py-1.5 rounded-lg transition-colors inline-flex items-center gap-1">
                            <X className="w-3 h-3" /> Reject
                          </button>
                          <button onClick={() => handleAction(req.id, "approve")} className="bg-emerald-900/30 hover:bg-emerald-900/50 text-emerald-400 px-3 py-1.5 rounded-lg transition-colors inline-flex items-center gap-1">
                            <Check className="w-3 h-3" /> Approve
                          </button>
                        </td>
                      </tr>
                    ))}
                    {requests.length === 0 && (
                      <tr><td colSpan={5} className="px-6 py-12 text-center text-slate-500">No pending requests.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Feedback & Support */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
              <div className="p-6 border-b border-slate-800 flex items-center gap-3 bg-slate-950/50">
                <MessageSquare className="w-5 h-5 text-indigo-400" />
                <h2 className="text-xl font-bold text-white">System Feedback & Tickets</h2>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-950/80 text-slate-400 text-xs uppercase tracking-wider">
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
                      <tr key={fb.id} className="hover:bg-slate-800/30 transition-colors">
                        <td className="px-6 py-4 text-slate-300 font-medium capitalize">{fb.category}</td>
                        <td className="px-6 py-4 text-slate-400 max-w-md">
                          <p className="line-clamp-2">{fb.message}</p>
                          {fb.admin_reply && <p className="text-xs text-blue-400 mt-1">Admin Reply: {fb.admin_reply}</p>}
                        </td>
                        <td className="px-6 py-4 text-slate-500 text-xs">
                          {fb.email || fb.name || "Anonymous"}
                          {fb.user_id && (
                            <button onClick={() => handleBlockUser(fb.user_id)} className="block text-red-500 hover:underline mt-1">Block User</button>
                          )}
                        </td>
                        <td className="px-6 py-4 text-slate-500 text-xs">
                          {fb.status === "hidden" ? <span className="text-red-400">Hidden</span> : <span className="text-emerald-400">Visible</span>}
                        </td>
                        <td className="px-6 py-4 text-right space-x-2 space-y-1">
                          <button onClick={() => handleReply(fb.id)} className="bg-blue-900/30 hover:bg-blue-900/50 text-blue-400 px-2 py-1 rounded transition-colors text-xs">Reply</button>
                          <button onClick={() => handleFeedbackAction(fb.id, "hide")} className="bg-slate-700 hover:bg-slate-600 text-white px-2 py-1 rounded transition-colors text-xs">Toggle Hide</button>
                          <button onClick={() => handleFeedbackAction(fb.id, "delete")} className="bg-red-900/30 hover:bg-red-900/50 text-red-400 px-2 py-1 rounded transition-colors text-xs">Delete</button>
                        </td>
                      </tr>
                    ))}
                    {feedback.length === 0 && (
                      <tr><td colSpan={5} className="px-6 py-12 text-center text-slate-500">No feedback entries found.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            <BlogEditor secret={secret} />

          </div>
        )}
      </div>
    </main>
  );
}
