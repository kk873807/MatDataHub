import { useState } from "react";
import { useRouter } from "next/navigation";
import { X, Mail, Lock, ArrowRight } from "lucide-react";
import { API } from "@/lib/api";

export function LoginModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [isRegister, setIsRegister] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const endpoint = isRegister ? `${API}/auth/register` : `${API}/auth/login`;
      const payload = isRegister ? { email, password, name: name || email.split("@")[0] } : { email, password };
      
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Authentication failed");

      localStorage.setItem("token", data.access_token);
      onClose();
      // Redirect to dashboard
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4 animate-in fade-in duration-200">
      <div className="bg-slate-900 border border-slate-800 w-full max-w-md rounded-2xl shadow-2xl overflow-hidden relative animate-in zoom-in-95 duration-200">
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
        
        <div className="p-8">
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-white mb-2">{isRegister ? "Create an Account" : "Welcome Back"}</h2>
            <p className="text-slate-400 text-sm">
              {isRegister ? "Start your engineering journey today." : "Sign in to access your workspaces."}
            </p>
          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-500/50 text-red-500 text-sm p-3 rounded-lg mb-6">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {isRegister && (
              <div>
                <label className="block text-sm font-medium text-slate-400 mb-1">Full Name</label>
                <div className="relative">
                  <input 
                    type="text" 
                    value={name}
                    onChange={e => setName(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 pl-11 text-white focus:outline-none focus:border-indigo-500 transition-colors"
                    placeholder="John Doe"
                  />
                  <div className="absolute left-4 top-3.5 text-slate-500">
                    <Mail className="w-5 h-5" />
                  </div>
                </div>
              </div>
            )}
            
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-1">Email Address</label>
              <div className="relative">
                <input 
                  type="email" 
                  required
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 pl-11 text-white focus:outline-none focus:border-indigo-500 transition-colors"
                  placeholder="name@company.com"
                />
                <div className="absolute left-4 top-3.5 text-slate-500">
                  <Mail className="w-5 h-5" />
                </div>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-400 mb-1">Password</label>
              <div className="relative">
                <input 
                  type="password"
                  required 
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 pl-11 text-white focus:outline-none focus:border-indigo-500 transition-colors"
                  placeholder="••••••••"
                />
                <div className="absolute left-4 top-3.5 text-slate-500">
                  <Lock className="w-5 h-5" />
                </div>
              </div>
            </div>

            <button 
              type="submit" 
              disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3 rounded-xl flex items-center justify-center gap-2 transition-colors disabled:opacity-50 mt-6"
            >
              {loading ? "Please wait..." : isRegister ? "Create Account" : "Sign In"}
              {!loading && <ArrowRight className="w-4 h-4" />}
            </button>
          </form>

          <div className="mt-6 text-center">
            <button 
              type="button"
              onClick={() => {
                setIsRegister(!isRegister);
                setError("");
              }}
              className="text-sm text-slate-400 hover:text-white transition-colors"
            >
              {isRegister ? "Already have an account? Sign in" : "Don't have an account? Create one"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
