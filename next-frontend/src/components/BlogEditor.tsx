"use client";
import { useState } from "react";
import { FileText, Plus, Loader2 } from "lucide-react";
import { API } from "@/lib/api";

export default function BlogEditor({ secret }: { secret: string }) {
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true); setMessage("");
    const fd = new FormData(e.currentTarget as HTMLFormElement);
    const payload = {
      title: fd.get("title"),
      date: new Date().toLocaleDateString("en-GB"),
      author: fd.get("author"),
      readTime: fd.get("readTime"),
      tag: fd.get("tag"),
      featured: fd.get("featured") === "true",
      excerpt: fd.get("excerpt"),
      content: fd.get("content")
    };
    try {
      const res = await fetch(${API}/blogs/, {
        method: "POST", headers: { "Content-Type": "application/json", "X-Admin-Secret": secret },
        body: JSON.stringify(payload)
      });
      if(res.ok) { setMessage("Blog posted successfully!"); (e.target as HTMLFormElement).reset(); setIsOpen(false); }
      else { setMessage("Failed to post blog."); }
    } catch (err) { setMessage("Error posting blog."); }
    setLoading(false);
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
      <div className="p-6 border-b border-slate-800 flex items-center justify-between bg-slate-950/50">
        <div className="flex items-center gap-3">
          <FileText className="w-5 h-5 text-emerald-400" />
          <h2 className="text-xl font-bold text-white">Content Management</h2>
        </div>
        <button onClick={() => setIsOpen(!isOpen)} className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-lg transition-colors text-sm flex items-center gap-2">
          <Plus className="w-4 h-4" /> {isOpen ? "Close Editor" : "Post New Blog"}
        </button>
      </div>
      {message && <div className="p-4 text-emerald-400 bg-emerald-900/20 text-center">{message}</div>}
      {isOpen ? (
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <input type="text" name="title" required placeholder="Blog Title" className="w-full bg-slate-950 border border-slate-800 rounded px-4 py-2 text-white" />
          <div className="grid grid-cols-3 gap-4">
            <input type="text" name="author" required placeholder="Author" className="bg-slate-950 border border-slate-800 rounded px-4 py-2 text-white" />
            <input type="text" name="readTime" required placeholder="Read Time (e.g. 5 min)" className="bg-slate-950 border border-slate-800 rounded px-4 py-2 text-white" />
            <input type="text" name="tag" required placeholder="Category Tag" className="bg-slate-950 border border-slate-800 rounded px-4 py-2 text-white" />
          </div>
          <label className="flex items-center gap-2 text-slate-300">
            <input type="checkbox" name="featured" value="true" /> Featured Blog?
          </label>
          <textarea name="excerpt" required placeholder="Short Excerpt" rows={2} className="w-full bg-slate-950 border border-slate-800 rounded px-4 py-2 text-white"></textarea>
          <textarea name="content" required placeholder="Markdown Content..." rows={10} className="w-full bg-slate-950 border border-slate-800 rounded px-4 py-2 text-white font-mono text-sm"></textarea>
          <button type="submit" disabled={loading} className="w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-lg">
            {loading ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : "Publish Blog"}
          </button>
        </form>
      ) : (
        <div className="p-6 text-center text-slate-400">
          <p>Click "Post New Blog" to write a Markdown article.</p>
        </div>
      )}
    </div>
  );
}