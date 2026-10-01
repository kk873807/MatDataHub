import re

with open(r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\admin\page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

import1 = 'import { ShieldAlert, Check, X, Lock, Users, MessageSquare, FileText, Plus, Database, ShieldCheck } from "lucide-react";'
if 'ShieldCheck' not in content:
    content = content.replace('import { ShieldAlert, Check, X, Lock, Users, MessageSquare, FileText, Plus, Database } from "lucide-react";', import1)

import2 = 'import { useState, useEffect } from "react";'
if 'useEffect' not in content:
    content = content.replace('import { useState } from "react";', import2)

# Insert state
if 'const [profile' not in content:
    content = content.replace('const [authed, setAuthed] = useState(false);', 'const [authed, setAuthed] = useState(false);\n  const [profile, setProfile] = useState<any>(null);')


# Replace handleLogin
bad_login = re.search(r'  const handleLogin =.*?^\s*};\n', content, re.MULTILINE | re.DOTALL).group(0)

good_login = '''  useEffect(() => {
    checkAdmin();
  }, []);

  const checkAdmin = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      setLoading(false);
      return;
    }
    
    try {
      const res = await fetch(`${API}/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
      if (res.ok) {
        const data = await res.json();
        setProfile(data);
        if (data.is_admin) {
          setAuthed(true);
          fetchAdminData(token);
        }
      }
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const handleClaimAdmin = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    try {
      const res = await fetch(`${API}/auth/make-me-admin`, {
        method: "POST",
        headers: { "X-Admin-Secret": secret, "Authorization": `Bearer ${token}` }
      });
      if (res.ok) {
        window.location.reload();
      } else {
        setError("Invalid system secret.");
      }
    } catch (e) {
      setError("Network error");
    }
  };
'''

content = content.replace(bad_login, good_login)

# Replace fetchAdminData
bad_fetch = re.search(r'  const fetchAdminData =.*?^\s*};\n', content, re.MULTILINE | re.DOTALL).group(0)
good_fetch = '''  const fetchAdminData = async (token: string) => {
    setLoading(true);
    try {
      const [reqRes, feedRes, contribRes, txnRes] = await Promise.all([
        fetch(`${API}/admin/upgrade-requests`, {
          headers: { "Authorization": `Bearer ${token}` }
        }),
        fetch(`${API}/feedback/`, {
          headers: { "Authorization": `Bearer ${token}` }
        }),
        fetch(`${API}/admin/user-contributions`, {
          headers: { "Authorization": `Bearer ${token}` }
        }),
        fetch(`${API}/admin/transactions`, {
          headers: { "Authorization": `Bearer ${token}` }
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
      
      if (contribRes.ok) {
        const c = await contribRes.json();
        setContributions(c.users || []);
      }
      
      if (txnRes.ok) {
        setTransactions(await txnRes.json());
      }
      
    } catch (err) {
      console.error(err);
      setError("Network Error");
    } finally {
      setLoading(false);
    }
  };\n'''

content = content.replace(bad_fetch, good_fetch)

# Update ALL fetch calls in the file to use Bearer token instead of X-Admin-Secret
# (Be careful not to replace the ones inside fetchAdminData which already have Bearer token)
content = content.replace('headers: { "X-Admin-Secret": secret }', 'headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }')

# Now replace the UI block
bad_ui = re.search(r'  if \(!authed\) \{.*?\s*return \(\n      <main className="flex flex-col items-center justify-center min-h-\[80vh\] p-6">.*?</main>\n    \);\n  }', content, re.MULTILINE | re.DOTALL).group(0)
good_ui = '''  if (loading) return <div className="p-12 text-center text-slate-500">Loading Admin Dashboard...</div>;

  if (!profile) {
    return (
      <main className="flex justify-center items-center min-h-[80vh] p-6">
        <div className="text-center space-y-4">
          <ShieldAlert className="w-12 h-12 text-red-500 mx-auto" />
          <h1 className="text-2xl font-bold">Access Denied</h1>
          <p className="text-slate-500">You must be logged in to view this page.</p>
          <button onClick={() => window.location.href='/?login=true'} className="px-6 py-2 bg-blue-600 text-white rounded-xl">Go to Login</button>
        </div>
      </main>
    );
  }

  if (!authed) {
    return (
      <main className="flex justify-center items-center min-h-[80vh] p-6">
        <form onSubmit={handleClaimAdmin} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 rounded-2xl w-full max-w-sm shadow-2xl flex flex-col gap-6">
          <div className="flex justify-center">
            <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 text-blue-600 rounded-full flex items-center justify-center">
              <ShieldCheck className="w-8 h-8" />
            </div>
          </div>
          <div className="text-center space-y-2">
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white font-heading">Claim Admin Rights</h1>
            <p className="text-slate-500 dark:text-slate-400 text-sm">Enter the root system secret to permanently make {profile.email} an admin.</p>
          </div>
          
          <div className="space-y-4">
            <div>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input 
                  type="password"
                  value={secret}
                  onChange={e => setSecret(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 focus:ring-2 focus:ring-blue-500 outline-none transition-shadow"
                  placeholder="System Secret (ADMIN_SECRET)"
                  autoFocus
                />
              </div>
            </div>
            
            {error && <p className="text-red-500 text-sm font-medium text-center">{error}</p>}
            
            <button 
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-slate-900 hover:bg-slate-800 dark:bg-blue-600 dark:hover:bg-blue-700 text-white rounded-xl font-bold transition-colors disabled:opacity-50"
            >
              Make Me Admin
            </button>
          </div>
        </form>
      </main>
    );
  }'''

content = content.replace(bad_ui, good_ui)

with open(r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\admin\page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Safely replaced everything!")
