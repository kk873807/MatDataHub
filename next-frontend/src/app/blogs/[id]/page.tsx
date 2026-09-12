"use client";
import { ArrowLeft, Clock, Share2, ArrowRight } from "lucide-react";
import Link from "next/link";
import { useParams, notFound } from "next/navigation";
import { HARDCODED_POSTS } from "@/lib/blogs";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function BlogPost() {
  const params = useParams();
  const id = parseInt(params.id as string, 10);
  
  if (isNaN(id) || id < 0 || id >= HARDCODED_POSTS.length) {
    return notFound();
  }
  
  const blog = HARDCODED_POSTS[id];
  
  const handleShare = async () => {
    try {
      if (navigator.share) {
        await navigator.share({
          title: blog.title,
          url: window.location.href,
        });
      } else {
        await navigator.clipboard.writeText(window.location.href);
        alert('Link copied to clipboard!');
      }
    } catch (err) {
      console.error('Error sharing:', err);
    }
  };
  
  return (
    <main className="min-h-screen bg-slate-50 dark:bg-slate-950 pt-24 pb-24 relative overflow-hidden">
      
      {/* Animated Background Elements */}
      <div className="absolute top-0 inset-x-0 h-[500px] bg-gradient-to-b from-indigo-500/10 to-transparent pointer-events-none" />
      <div className="absolute top-40 right-0 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl pointer-events-none mix-blend-multiply dark:mix-blend-lighten animate-blob" />
      <div className="absolute top-60 -left-20 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl pointer-events-none mix-blend-multiply dark:mix-blend-lighten animate-blob animation-delay-4000" />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 relative z-10">
        <Link href="/blogs" className="inline-flex items-center gap-2 text-sm font-bold text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400 mb-10 transition-colors bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm px-4 py-2 rounded-full border border-slate-200 dark:border-slate-800">
          <ArrowLeft className="w-4 h-4" /> Back to all articles
        </Link>
        
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-[2.5rem] shadow-xl shadow-slate-200/50 dark:shadow-none overflow-hidden relative">
          
          <div className="h-64 md:h-96 w-full relative">
            <img src={blog.image} alt={blog.title} className="w-full h-full object-cover" />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/40 to-transparent" />
            
            <div className="absolute bottom-0 left-0 w-full p-8 md:p-12">
              <div className="flex flex-wrap gap-3 items-center mb-6">
                <span className="text-[10px] font-black uppercase tracking-wider text-white bg-indigo-600 px-3 py-1.5 rounded-full shadow-lg">{blog.tag}</span>
                <span className="text-sm text-slate-200 font-medium flex items-center gap-1.5"><Clock className="w-4 h-4 text-indigo-400"/> {blog.readTime} read</span>
                <span className="text-sm text-slate-400 font-medium">•</span>
                <span className="text-sm text-slate-300 font-medium">{blog.date}</span>
              </div>
              
              <h1 className="text-3xl md:text-5xl font-extrabold text-white font-heading leading-tight max-w-3xl drop-shadow-lg">{blog.title}</h1>
            </div>
          </div>
          
          <div className="p-8 md:p-12">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 border-b border-slate-100 dark:border-slate-800 pb-10 mb-10">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 rounded-full bg-gradient-to-br from-indigo-100 to-blue-100 dark:from-indigo-900/50 dark:to-blue-900/50 flex items-center justify-center text-indigo-600 dark:text-indigo-400 font-bold text-xl border border-indigo-200 dark:border-indigo-500/30 shadow-inner">
                  {blog.author.charAt(0)}
                </div>
                <div>
                  <p className="text-base font-bold text-slate-900 dark:text-white">{blog.author}</p>
                  <p className="text-sm text-slate-500 dark:text-slate-400 font-medium">MatDataHub Engineering</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <span className="text-sm font-semibold text-slate-500 dark:text-slate-400 mr-2">Share article</span>
                <button onClick={handleShare} className="w-10 h-10 rounded-full bg-slate-50 dark:bg-slate-800 flex items-center justify-center text-slate-600 dark:text-slate-400 hover:bg-indigo-50 hover:text-indigo-600 dark:hover:bg-indigo-900/30 dark:hover:text-indigo-400 transition-colors border border-slate-200 dark:border-slate-700">
                  <Share2 className="w-4 h-4" />
                </button>
              </div>
            </div>
            
            <div className="prose prose-lg prose-slate dark:prose-invert prose-indigo max-w-none 
              prose-headings:font-bold prose-headings:font-heading prose-headings:tracking-tight
              prose-h2:text-3xl prose-h2:mt-12 prose-h2:mb-6 prose-h2:text-slate-900 dark:prose-h2:text-white
              prose-p:text-slate-600 dark:prose-p:text-slate-300 prose-p:leading-relaxed prose-p:mb-8 
              prose-li:text-slate-600 dark:prose-li:text-slate-300 prose-li:my-2 
              prose-strong:text-slate-900 dark:prose-strong:text-white prose-strong:font-bold 
              prose-table:w-full prose-table:text-sm prose-table:border-collapse prose-table:my-10 
              prose-th:bg-slate-50 dark:prose-th:bg-slate-900/50 prose-th:p-4 prose-th:border prose-th:border-slate-200 dark:prose-th:border-slate-700 prose-th:text-slate-900 dark:prose-th:text-white prose-th:font-bold
              prose-td:p-4 prose-td:border prose-td:border-slate-200 dark:prose-td:border-slate-800 prose-td:text-slate-600 dark:prose-td:text-slate-400 
              prose-blockquote:border-l-4 prose-blockquote:border-indigo-500 prose-blockquote:pl-6 prose-blockquote:italic prose-blockquote:text-slate-700 dark:prose-blockquote:text-slate-300 prose-blockquote:bg-indigo-50/50 dark:prose-blockquote:bg-indigo-900/10 prose-blockquote:py-2 prose-blockquote:my-8 prose-blockquote:rounded-r-xl">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {blog.content}
              </ReactMarkdown>
            </div>
            
            {/* Feature Call To Action */}
            <div className="mt-16 pt-12 border-t border-slate-100 dark:border-slate-800 text-center">
              <h4 className="text-xl md:text-2xl text-slate-900 dark:text-white font-heading font-bold mb-6">Ready to apply these engineering insights?</h4>
              <Link href={(blog as any).featureLink || '/analytics'} className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 text-white font-bold rounded-2xl transition-all shadow-lg hover:shadow-indigo-500/25 transform hover:-translate-y-1">
                {(blog as any).featureName || 'Try MatDataHub Analytics'} <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </div>
          
        </div>
      </div>
    </main>
  );
}
