import os

code = """"use client";
import { Calendar, ArrowRight, User, Star, Clock } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import { API } from "@/lib/utils";

const HARDCODED_POSTS = [
  {
    id: "sustainable-materials",
    title: "The Future of Sustainable Materials in Manufacturing",
    excerpt: "Discover how AI is accelerating the discovery of eco-friendly polymers and reducing industrial carbon footprints globally.",
    date: "Oct 15, 2026",
    author: "Dr. Sarah Chen",
    category: "Sustainability",
    image: "https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&q=80&w=800",
  },
  {
    id: "high-entropy-alloys",
    title: "Understanding High-Entropy Alloys",
    excerpt: "A deep dive into the properties, applications, and predictive modeling of next-generation metal structures.",
    date: "Oct 02, 2026",
    author: "James Wilson",
    category: "Materials Science",
    image: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=800",
  },
  {
    id: "matdatahub-2",
    title: "MatDataHub 2.0: What's New",
    excerpt: "We're thrilled to announce our latest features, including the new AI Synthesizer and CBAM impact calculators.",
    date: "Sep 28, 2026",
    author: "Product Team",
    category: "Announcements",
    image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=800",
  }
];

export default function BlogsPage() {
  const [apiBlogs, setApiBlogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/blogs/`)
      .then(r => r.ok ? r.json() : [])
      .then(d => {
        setApiBlogs(d);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <main className="min-h-screen bg-white dark:bg-slate-950 pt-10 pb-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-white font-heading mb-6">Our Blogs</h1>
          <p className="text-lg text-slate-600 dark:text-slate-400">
            Insights, updates, and deep dives into materials science, AI engineering, and the future of manufacturing.
          </p>
        </div>

        <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-6">Latest Articles</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {HARDCODED_POSTS.map((post, i) => (
            <div key={i} className="group flex flex-col bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl overflow-hidden hover:shadow-xl hover:shadow-blue-900/5 transition-all">
              <div className="relative h-48 overflow-hidden">
                <img src={post.image} alt={post.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                <div className="absolute top-4 left-4">
                  <span className="px-3 py-1 bg-white/90 dark:bg-slate-900/90 backdrop-blur-sm text-blue-600 dark:text-blue-400 text-xs font-bold rounded-full">
                    {post.category}
                  </span>
                </div>
              </div>
              <div className="p-6 flex flex-col flex-1">
                <div className="flex items-center gap-4 text-xs text-slate-500 dark:text-slate-400 mb-4">
                  <span className="flex items-center gap-1.5"><Calendar className="w-4 h-4" /> {post.date}</span>
                  <span className="flex items-center gap-1.5"><User className="w-4 h-4" /> {post.author}</span>
                </div>
                <h2 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-3 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                  {post.title}
                </h2>
                <p className="text-sm text-slate-600 dark:text-slate-400 mb-6 flex-1 line-clamp-3">
                  {post.excerpt}
                </p>
                <Link href={`/blogs/${post.id}`} className="inline-flex items-center gap-2 text-sm font-bold text-blue-600 dark:text-blue-400 group-hover:gap-3 transition-all">
                  Read Article <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          ))}
        </div>

        {apiBlogs.length > 0 && (
          <>
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-6">Community & Archive</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {apiBlogs.map((blog, i) => (
                <div 
                  key={i} 
                  className={`bg-white dark:bg-slate-900 border ${blog.featured ? 'border-indigo-500/50 shadow-[0_0_15px_rgba(99,102,241,0.1)]' : 'border-slate-200 dark:border-slate-800 hover:border-slate-600'} p-6 rounded-3xl transition-all group flex flex-col h-full relative overflow-hidden`}
                >
                  {blog.featured && <div className="absolute top-0 right-0 w-16 h-16 bg-indigo-500/10 rounded-bl-full blur-xl"></div>}
                  
                  <div className="flex justify-between items-start mb-4">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400 bg-indigo-100 dark:bg-indigo-900/30 border border-indigo-200 dark:border-indigo-800/50 px-2 py-1 rounded flex items-center gap-1">
                      {blog.featured && <Star className="w-3 h-3 text-amber-600 dark:text-amber-400" fill="currentColor" />}
                      {blog.tag}
                    </span>
                    <div className="flex items-center gap-1 text-slate-500 dark:text-slate-400 text-xs font-medium">
                      <Clock className="w-3 h-3" /> {blog.readTime}
                    </div>
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 dark:text-white font-heading mb-3 group-hover:text-indigo-600 dark:text-indigo-300 transition-colors leading-tight">{blog.title}</h3>
                  <p className="text-sm text-slate-500 dark:text-slate-400 mb-6 flex-1 line-clamp-3 leading-relaxed">{blog.excerpt}</p>
                  <div className="flex justify-between items-center border-t border-slate-200 dark:border-slate-800/50 pt-4 mt-auto">
                    <span className="text-xs text-slate-500 dark:text-slate-400 font-medium">By {blog.author}</span>
                    <Link href={`/blogs/api-${blog.id}`} className="text-sm font-semibold text-blue-600 dark:text-blue-400 flex items-center gap-1 group-hover:gap-2 transition-all">
                      Read <ArrowRight className="w-4 h-4"/>
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </main>
  );
}
"""

with open('src/app/blogs/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Created blogs/page.tsx successfully with single quotes wrapper!")
