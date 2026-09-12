const fs = require('fs');

const code = \"use client";
import { ArrowRight, User, Star, Clock, Sparkles } from "lucide-react";
import Link from "next/link";
import { HARDCODED_POSTS } from "@/lib/blogs";
import { useState } from "react";

export default function BlogsPage() {
  const [hoveredIdx, setHoveredIdx] = useState(-1);

  return (
    <main className="min-h-screen bg-slate-50 dark:bg-slate-950 pt-24 pb-24 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute top-0 inset-x-0 h-96 bg-gradient-to-b from-blue-500/10 to-transparent pointer-events-none" />
      <div className="absolute top-20 -left-40 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none mix-blend-multiply dark:mix-blend-lighten animate-blob" />
      <div className="absolute top-40 -right-40 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none mix-blend-multiply dark:mix-blend-lighten animate-blob animation-delay-2000" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 relative z-10">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-sm font-bold uppercase tracking-wider mb-4 shadow-sm border border-blue-200 dark:border-blue-800/50">
            <Sparkles className="w-4 h-4" /> Editorial
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 dark:text-white font-heading mb-6 tracking-tight">Engineering Insights</h1>
          <p className="text-lg text-slate-600 dark:text-slate-400 leading-relaxed">Deep dives into materials science, aerospace modeling, economic impacts, and compliance standards.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {HARDCODED_POSTS.map((post, idx) => (
            <Link 
              key={idx} 
              href={\/blogs/\\} 
              onMouseEnter={() => setHoveredIdx(idx)}
              onMouseLeave={() => setHoveredIdx(-1)}
              className="group bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:border-indigo-500/50 rounded-3xl overflow-hidden shadow-sm hover:shadow-2xl hover:shadow-indigo-500/10 transition-all duration-300 flex flex-col transform hover:-translate-y-1"
            >
              <div className="h-48 md:h-56 overflow-hidden relative">
                <img 
                  src={post.image} 
                  alt={post.title} 
                  className={\w-full h-full object-cover transition-transform duration-700 ease-out \\}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/0 to-black/0" />
                <div className="absolute top-4 right-4">
                  {post.featured && (
                    <span className="px-3 py-1 bg-amber-500/90 backdrop-blur-sm text-white text-[10px] font-black uppercase tracking-wider rounded-full flex items-center gap-1 shadow-lg">
                      <Star className="w-3 h-3" fill="currentColor"/> Featured
                    </span>
                  )}
                </div>
                <div className="absolute bottom-4 left-4">
                   <span className="px-3 py-1 bg-white/90 dark:bg-slate-900/90 backdrop-blur-md text-indigo-600 dark:text-indigo-400 text-xs font-bold uppercase tracking-wider rounded-full shadow-sm">
                    {post.tag}
                  </span>
                </div>
              </div>

              <div className="p-6 md:p-8 flex-1 flex flex-col relative bg-white dark:bg-slate-900">
                <h3 className="text-xl md:text-2xl font-bold text-slate-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors mb-3 leading-tight font-heading">
                  {post.title}
                </h3>
                <p className="text-slate-600 dark:text-slate-400 text-sm mb-6 flex-1 line-clamp-3 leading-relaxed">
                  {post.excerpt}
                </p>
                <div className="flex items-center justify-between mt-auto pt-6 border-t border-slate-100 dark:border-slate-800/60">
                  <div className="flex items-center gap-4 text-xs font-semibold text-slate-500 dark:text-slate-400">
                    <div className="flex items-center gap-1.5">
                      <User className="w-4 h-4 text-slate-400" /> {post.author}
                    </div>
                    <div className="flex items-center gap-1.5">
                      <Clock className="w-4 h-4 text-slate-400" /> {post.readTime}
                    </div>
                  </div>
                  <div className="w-8 h-8 rounded-full bg-slate-50 dark:bg-slate-800 group-hover:bg-indigo-50 dark:group-hover:bg-indigo-900/30 flex items-center justify-center transition-colors">
                    <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors" />
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}
\;

fs.writeFileSync('src/app/blogs/page.tsx', code);
