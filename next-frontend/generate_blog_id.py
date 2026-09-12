import os

code = '''"use client";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";

export default function BlogPost() {
  const params = useParams();
  
  return (
    <main className="min-h-screen bg-slate-50 dark:bg-slate-950 pt-10 pb-24">
      <div className="max-w-3xl mx-auto px-4 sm:px-6">
        <Link href="/blogs" className="inline-flex items-center gap-2 text-sm font-semibold text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 mb-8 transition-colors">
          <ArrowLeft className="w-4 h-4" /> Back to Blogs
        </Link>
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-8 md:p-12 shadow-sm">
          <h1 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white font-heading mb-6">Blog Article {params.id}</h1>
          <p className="text-slate-600 dark:text-slate-400 leading-relaxed mb-6">
            This is a placeholder for the blog article content. In a fully implemented system, this page would fetch the blog content matching the ID "{params.id}" from the database and render the full markdown or rich text here.
          </p>
          <div className="h-48 bg-slate-100 dark:bg-slate-800 rounded-2xl flex items-center justify-center text-slate-400 text-sm">
            [Content Area]
          </div>
        </div>
      </div>
    </main>
  );
}
'''

with open('src/app/blogs/[id]/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Created blogs/[id]/page.tsx")
