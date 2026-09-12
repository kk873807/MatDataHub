"use client";
import { useState, useEffect } from "react";
import { MessageSquare, ThumbsUp, Image as ImageIcon, Send, Loader2, CheckCircle2 } from "lucide-react";
import { API } from "@/lib/api";

export default function FeedbackCommunityPage() {
  const [feedbacks, setFeedbacks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  const [form, setForm] = useState({ name: "", email: "", category: "Feature Request", message: "" });
  const [image, setImage] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [acceptedTc, setAcceptedTc] = useState(false);
  const [tcError, setTcError] = useState("");
  const [replyToId, setReplyToId] = useState<number | null>(null);

  useEffect(() => {
    fetch(`${API}/feedback/public`)
      .then(res => res.json())
      .then(data => setFeedbacks(Array.isArray(data) ? data : []))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!acceptedTc) {
      setTcError("You must accept the terms and conditions to submit feedback.");
      return;
    }
    setTcError("");
    setSubmitting(true);
    try {
      const payload = {
        name: form.name || "Anonymous Engineer",
        email: form.email,
        category: form.category,
        message: form.message,
        image_data: image,
        page_context: "Community Wall",
        parent_id: replyToId
      };
      
      await fetch(`${API}/feedback/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      
      // Refresh list
      const res = await fetch(`${API}/feedback/public`);
      const data = await res.json();
      setFeedbacks(Array.isArray(data) ? data : []);
      
      setForm({ name: "", email: "", category: "Feature Request", message: "" });
      setImage(null);
      setReplyToId(null);
      setAcceptedTc(false);
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="flex flex-col p-6 lg:p-10 w-full h-full overflow-y-auto">
      <div className="w-full max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-10">
        
        {/* Left Col: Wall */}
        <div className="lg:col-span-2 space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-slate-900 dark:text-white font-heading flex items-center gap-3">
              <MessageSquare className="w-8 h-8 text-blue-600 dark:text-blue-600 dark:text-blue-400" />
              Community Feedback
            </h1>
            <p className="text-slate-600 dark:text-slate-300 mt-2">See what other engineers are requesting and vote on new features.</p>
          </div>
          
          <div className="space-y-4 pt-4">
            {loading ? (
              <div className="flex justify-center p-10"><Loader2 className="w-8 h-8 animate-spin text-indigo-500" /></div>
            ) : feedbacks.length === 0 ? (
              <div className="text-center p-12 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl">
                <p className="text-slate-500 dark:text-slate-400">No feedback yet. Be the first to start the conversation!</p>
              </div>
            ) : (
              feedbacks.filter(fb => !fb.parent_id).map((fb) => (
                <div key={fb.id} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-xl relative group">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h4 className="font-bold text-slate-900 dark:text-white font-heading">{fb.name || 'Anonymous Engineer'}</h4>
                      <span className="text-xs font-semibold px-2 py-0.5 bg-indigo-100 dark:bg-indigo-100 dark:bg-indigo-900/30 text-blue-600 dark:text-blue-600 dark:text-blue-400 rounded-full border border-indigo-200 dark:border-indigo-700/50">{fb.category}</span>
                    </div>
                    <span className="text-xs text-slate-500 dark:text-slate-400">{new Date(fb.created_at).toLocaleDateString('en-GB')}</span>
                  </div>
                  <p className="text-slate-600 dark:text-slate-300 text-sm mb-4 leading-relaxed">{fb.message}</p>
                  
                  {fb.image_data && (
                    <img src={fb.image_data} alt="Attached screenshot" className="max-w-xs rounded-2xl border border-slate-200 dark:border-slate-700 mb-4 opacity-80 hover:opacity-100 transition-opacity" />
                  )}
                  
                  <div className="flex items-center gap-4 border-t border-slate-200 dark:border-slate-800 pt-3">
                    <button className="flex items-center gap-1.5 text-xs font-medium text-slate-500 dark:text-slate-400 hover:text-emerald-600 dark:text-emerald-400 transition-colors">
                      <ThumbsUp className="w-4 h-4" /> {fb.helpful_votes || 0} Votes
                    </button>
                    <button 
                      onClick={() => setReplyToId(fb.id)}
                      className="flex items-center gap-1.5 text-xs font-medium text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:text-blue-400 transition-colors"
                    >
                      <MessageSquare className="w-4 h-4" /> Reply
                    </button>
                    {fb.status === 'reviewed' && (
                      <span className="flex items-center gap-1.5 text-xs font-medium text-emerald-500">
                        <CheckCircle2 className="w-4 h-4" /> Reviewed by Team
                      </span>
                    )}
                  </div>
                  
                  {/* Nested Replies (very basic for now, filtering the flat list) */}
                  {feedbacks.filter(r => r.parent_id === fb.id).map(reply => (
                    <div key={reply.id} className="mt-4 pl-4 border-l-2 border-slate-200 dark:border-slate-700 bg-slate-100 dark:bg-slate-800/30 p-3 rounded-r-lg">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-bold text-slate-900 dark:text-white text-xs">{reply.name || "User"}</span>
                        <span className="text-slate-500 dark:text-slate-400 text-[10px]">{new Date(reply.created_at).toLocaleDateString('en-GB')}</span>
                      </div>
                      <p className="text-slate-600 dark:text-slate-300 text-xs">{reply.message}</p>
                    </div>
                  ))}
                  
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right Col: Form */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 h-fit sticky top-6">
          <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-2">{replyToId ? "Reply to Thread" : "Submit Feedback"}</h2>
          <p className="text-slate-500 dark:text-slate-400 text-sm mb-6">
            {replyToId ? "Join the conversation and share your thoughts." : "Have an idea or found a bug? Attach a screenshot and let us know."}
          </p>
          
          {replyToId && (
            <div className="mb-4 p-3 bg-blue-100 dark:bg-blue-100 dark:bg-blue-900/20 border border-blue-900/50 rounded-2xl flex justify-between items-center">
              <span className="text-blue-600 dark:text-blue-400 text-xs">Replying to feedback #{replyToId}</span>
              <button onClick={() => setReplyToId(null)} className="text-slate-500 dark:text-slate-400 hover:text-slate-600 dark:text-slate-300 dark:hover:text-slate-600 dark:text-slate-300 text-xs">Cancel</button>
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1 uppercase tracking-wider">Your Name (Optional)</label>
              <input type="text" value={form.name} onChange={e=>setForm({...form, name: e.target.value})} className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl px-3 py-2 text-slate-900 dark:text-white outline-none focus:border-indigo-500 text-sm" />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1 uppercase tracking-wider">Email (Required for spam prevention)</label>
              <input type="email" required value={form.email} onChange={e=>setForm({...form, email: e.target.value})} className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl px-3 py-2 text-slate-900 dark:text-white outline-none focus:border-indigo-500 text-sm" />
            </div>
            
            <div>
              <label className="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1 uppercase tracking-wider">Category</label>
              <select value={form.category} onChange={e=>setForm({...form, category: e.target.value})} className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl px-3 py-2 text-slate-900 dark:text-white outline-none focus:border-indigo-500 text-sm">
                <option>Feature Request</option>
                <option>Bug Report</option>
                <option>Data Correction</option>
                <option>General Feedback</option>
              </select>
            </div>
            
            <div>
              <label className="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1 uppercase tracking-wider">Message</label>
              <textarea required minLength={10} value={form.message} onChange={e=>setForm({...form, message: e.target.value})} className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl px-3 py-2 text-slate-900 dark:text-white outline-none focus:border-indigo-500 min-h-[100px] text-sm" />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-2 uppercase tracking-wider">Screenshot Attachment</label>
              <div className="flex items-center gap-3">
                <label className="flex items-center gap-2 px-3 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded cursor-pointer transition-colors border border-slate-200 dark:border-slate-700">
                  <ImageIcon className="w-4 h-4" /> Upload Image
                  <input type="file" accept="image/*" onChange={handleImageUpload} className="hidden" />
                </label>
                {image && <span className="text-xs text-emerald-600 dark:text-emerald-400 flex items-center gap-1"><CheckCircle2 className="w-3 h-3"/> Attached</span>}
              </div>
            </div>
            
            <div className="flex items-start gap-3 mt-4 pt-4 border-t border-slate-200 dark:border-slate-800">
              <input 
                type="checkbox" 
                id="tc" 
                checked={acceptedTc} 
                onChange={e => setAcceptedTc(e.target.checked)} 
                className="mt-1"
              />
              <label htmlFor="tc" className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed cursor-pointer">
                I agree to be polite, friendly, non-violent, non-sexual, and non-vulgar in my comments. 
                I understand that violating these Terms & Conditions will result in my account being blocked.
              </label>
            </div>
            {tcError && <p className="text-red-600 dark:text-red-400 text-xs font-semibold">{tcError}</p>}
            
            <button type="submit" disabled={submitting} className="w-full flex items-center justify-center gap-2 py-2.5 mt-4 bg-gradient-to-r from-blue-600 to-violet-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-bold rounded-2xl transition-colors">
              {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <><Send className="w-4 h-4"/> Post to Community</>}
            </button>
          </form>
        </div>

      </div>
    </main>
  );
}
