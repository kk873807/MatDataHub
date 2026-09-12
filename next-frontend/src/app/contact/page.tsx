import { Mail, MapPin } from "lucide-react";

export default function ContactPage() {
  return (
    <div className="max-w-4xl mx-auto p-12 text-slate-300">
      <h1 className="text-4xl font-bold text-white mb-6">Contact Us</h1>
      <p className="mb-10 text-lg">Have questions about Enterprise features, API access, or custom integrations? We're here to help.</p>
      
      <div className="grid md:grid-cols-2 gap-8">
        <div className="bg-slate-900 border border-slate-800 p-8 rounded-2xl">
          <Mail className="w-8 h-8 text-indigo-400 mb-4" />
          <h2 className="text-xl font-bold text-white mb-2">Email Support</h2>
          <p className="text-sm text-slate-400 mb-4">Our engineering team usually responds within 24 hours.</p>
          <a href="mailto:support@matdatahub.com" className="text-indigo-400 hover:text-indigo-300 font-bold">support@matdatahub.com</a>
        </div>
        
        <div className="bg-slate-900 border border-slate-800 p-8 rounded-2xl">
          <MapPin className="w-8 h-8 text-emerald-400 mb-4" />
          <h2 className="text-xl font-bold text-white mb-2">Global Headquarters</h2>
          <p className="text-sm text-slate-400 mb-4">We are a globally distributed team of material scientists and software engineers.</p>
          <p className="text-slate-300 font-medium">New Delhi, India</p>
        </div>
      </div>
    </div>
  );
}
