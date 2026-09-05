"use client";
import { useState, useEffect } from "react";
import { MessageSquare, ThumbsUp, Image as ImageIcon, Send, Loader2, CheckCircle2 } from "lucide-react";

export default function FeedbackCommunityPage() {
  const [feedbacks, setFeedbacks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  const [form, setForm] = useState({ name: "", email: "", category: "Feature Request", message: "" });
  const [image, setImage] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/feedback/public")
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
    setSubmitting(true);
    try {
      const payload = {
        name: form.name || "Anonymous Engineer",
        email: form.email,
        category: form.category,
        message: form.message,
        image_data: image,
        page_context: "Community Wall"
      };
      
      await fetch("http://127.0.0.1:8000/api/v1/feedback/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      
      // Refresh list
      const res = await fetch("http://127.0.0.1:8000/api/v1/feedback/public");
      const data = await res.json();
      setFeedbacks(Array.isArray(data) ? data : []);
      
      setForm({ name: "", email: "", category: "Feature Request", message: "" });
      setImage(null);
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
            <h1 className="text-3xl font-bold text-white flex items-center gap-3">
              <MessageSquare className="w-8 h-8 text-indigo-400" />
              Community Feedback
            </h1>
            <p className="text-slate-300 mt-2">See what other engineers are requesting and vote on new features.</p>
          </div>
          
          <div className="space-y-4 pt-4">
            {loading ? (
              <div className="flex justify-center p-10"><Loader2 className="w-8 h-8 animate-spin text-indigo-500" /></div>
            ) : feedbacks.length === 0 ? (
              <div className="text-center p-10 text-slate-500 bg-slate-900 rounded-xl border border-slate-800">No feedback submitted yet. Be the first!</div>
            ) : (
              feedbacks.map((fb, i) => (
                <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h4 className="font-bold text-white">{fb.name || 'Anonymous Engineer'}</h4>
                      <span className="text-xs font-semibold px-2 py-0.5 bg-indigo-900/30 text-indigo-400 rounded-full border border-indigo-700/50">{fb.category}</span>
                    </div>
                    <span className="text-xs text-slate-500">{new Date(fb.created_at).toLocaleDateString()}</span>
                  </div>
                  <p className="text-slate-300 text-sm mb-4 leading-relaxed">{fb.message}</p>
                  
                  {fb.image_data && (
                    <img src={fb.image_data} alt="Attached screenshot" className="max-w-xs rounded-lg border border-slate-700 mb-4 opacity-80 hover:opacity-100 transition-opacity" />
                  )}
                  
                  <div className="flex items-center gap-4 border-t border-slate-800 pt-3">
                    <button className="flex items-center gap-1.5 text-xs font-medium text-slate-400 hover:text-emerald-400 transition-colors">
                      <ThumbsUp className="w-4 h-4" /> {fb.helpful_votes || 0} Votes
                    </button>
                    {fb.status === 'reviewed' && (
                      <span className="flex items-center gap-1.5 text-xs font-medium text-emerald-500">
                        <CheckCircle2 className="w-4 h-4" /> Reviewed by Team
                      </span>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right Col: Form */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 h-fit sticky top-6">
          <h2 className="text-xl font-bold text-white mb-2">Submit Feedback</h2>
          <p className="text-slate-400 text-sm mb-6">Have an idea or found a bug? Attach a screenshot and let us know.</p>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1 uppercase tracking-wider">Your Name (Optional)</label>
              <input type="text" value={form.name} onChange={e=>setForm({...form, name: e.target.value})} className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white outline-none focus:border-indigo-500 text-sm" />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1 uppercase tracking-wider">Email (Required for spam prevention)</label>
              <input type="email" required value={form.email} onChange={e=>setForm({...form, email: e.target.value})} className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white outline-none focus:border-indigo-500 text-sm" />
            </div>
            
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1 uppercase tracking-wider">Category</label>
              <select value={form.category} onChange={e=>setForm({...form, category: e.target.value})} className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white outline-none focus:border-indigo-500 text-sm">
                <option>Feature Request</option>
                <option>Bug Report</option>
                <option>Data Correction</option>
                <option>General Feedback</option>
              </select>
            </div>
            
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1 uppercase tracking-wider">Message</label>
              <textarea required minLength={10} value={form.message} onChange={e=>setForm({...form, message: e.target.value})} className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white outline-none focus:border-indigo-500 min-h-[100px] text-sm" />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-2 uppercase tracking-wider">Screenshot Attachment</label>
              <div className="flex items-center gap-3">
                <label className="flex items-center gap-2 px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded cursor-pointer transition-colors border border-slate-700">
                  <ImageIcon className="w-4 h-4" /> Upload Image
                  <input type="file" accept="image/*" onChange={handleImageUpload} className="hidden" />
                </label>
                {image && <span className="text-xs text-emerald-400 flex items-center gap-1"><CheckCircle2 className="w-3 h-3"/> Attached</span>}
              </div>
            </div>
            
            <button type="submit" disabled={submitting} className="w-full flex items-center justify-center gap-2 py-2.5 mt-4 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-bold rounded-lg transition-colors">
              {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <><Send className="w-4 h-4"/> Post to Community</>}
            </button>
          </form>
        </div>

      </div>
    </main>
  );
}
