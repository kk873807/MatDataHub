"use client";
import { useState } from "react";
import { ShieldAlert, Check, X, Lock, Users, MessageSquare } from "lucide-react";

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
        fetch("http://127.0.0.1:8000/api/v1/admin/upgrade-requests", {
          headers: { "X-Admin-Secret": adminSecret }
        }),
        fetch("http://127.0.0.1:8000/api/v1/feedback/", {
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
      const res = await fetch(`http://127.0.0.1:8000/api/v1/admin/upgrade-requests/${userId}/${action}`, {
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
                        <td className="px-6 py-4 text-slate-500 text-xs">{new Date(req.requested_at).toLocaleString()}</td>
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
                      <th className="px-6 py-4 font-semibold">Type</th>
                      <th className="px-6 py-4 font-semibold">Content</th>
                      <th className="px-6 py-4 font-semibold">Email</th>
                      <th className="px-6 py-4 font-semibold">Timestamp</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/50">
                    {feedback.map((fb) => (
                      <tr key={fb.id} className="hover:bg-slate-800/30 transition-colors">
                        <td className="px-6 py-4 text-slate-300 font-medium capitalize">{fb.type}</td>
                        <td className="px-6 py-4 text-slate-400 max-w-md truncate">{fb.content}</td>
                        <td className="px-6 py-4 text-slate-500 text-xs">{fb.email || "Anonymous"}</td>
                        <td className="px-6 py-4 text-slate-500 text-xs">{new Date(fb.created_at).toLocaleString()}</td>
                      </tr>
                    ))}
                    {feedback.length === 0 && (
                      <tr><td colSpan={4} className="px-6 py-12 text-center text-slate-500">No feedback entries found.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>

          </div>
        )}
      </div>
    </main>
  );
}
