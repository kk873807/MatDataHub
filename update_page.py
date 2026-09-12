import os

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\page.tsx'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Import LoginModal
text = text.replace('import { API } from "@/lib/api";', 'import { API } from "@/lib/api";\nimport { LoginModal } from "@/components/LoginModal";')

# 2. Add State in LandingPage
state_add = """export default function LandingPage() {
  const [feedbacks, setFeedbacks] = useState<any[]>([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);

  useEffect(() => {
    // Check auth
    const token = localStorage.getItem("token");
    if (token) setIsLoggedIn(true);

    // Check query params for ?login=true
    if (window.location.search.includes('login=true')) {
      setShowLoginModal(true);
    }
  }, []);"""

text = text.replace('export default function LandingPage() {\n  const [feedbacks, setFeedbacks] = useState<any[]>([]);', state_add)

# 3. Fix Navbar
nav_old = """            <Link href="/account" className="text-sm font-semibold text-white bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-lg transition-all border border-slate-700">
              Sign In
            </Link>
            <Link href="/dashboard" className="text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-500 px-4 py-2 rounded-lg transition-all shadow-lg shadow-indigo-600/20 hidden sm:block">
              Go to Dashboard
            </Link>"""
            
nav_new = """            {isLoggedIn ? (
              <Link href="/dashboard" className="text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-500 px-4 py-2 rounded-lg transition-all shadow-lg shadow-indigo-600/20">
                Go to App Dashboard
              </Link>
            ) : (
              <button onClick={() => setShowLoginModal(true)} className="text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-500 px-5 py-2 rounded-lg transition-all shadow-lg shadow-indigo-600/20">
                Sign In
              </button>
            )}"""
text = text.replace(nav_old, nav_new)

# 4. Fix Hero CTA
hero_old = """              <Link href="/account" className="flex items-center gap-2 px-8 py-3.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold transition-all shadow-xl shadow-indigo-600/20 w-full sm:w-auto justify-center">
                Access Platform <ArrowRight className="w-4 h-4" />
              </Link>"""

hero_new = """              {isLoggedIn ? (
                <Link href="/dashboard" className="flex items-center gap-2 px-8 py-3.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold transition-all shadow-xl shadow-indigo-600/20 w-full sm:w-auto justify-center">
                  Access Platform <ArrowRight className="w-4 h-4" />
                </Link>
              ) : (
                <button onClick={() => setShowLoginModal(true)} className="flex items-center gap-2 px-8 py-3.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold transition-all shadow-xl shadow-indigo-600/20 w-full sm:w-auto justify-center">
                  Access Platform <ArrowRight className="w-4 h-4" />
                </button>
              )}"""
text = text.replace(hero_old, hero_new)

# 5. Fix Pricing CTAs (Start Free, Upgrade to Pro, Get Advanced)
pricing_old1 = '<Link href="/account" className="block text-center w-full py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold transition-colors">Start Free</Link>'
pricing_new1 = '<button onClick={() => setShowLoginModal(true)} className="block text-center w-full py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold transition-colors">Start Free</button>'
text = text.replace(pricing_old1, pricing_new1)

pricing_old2 = '<Link href="/account" className="block text-center w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold transition-colors">Upgrade to Pro</Link>'
pricing_new2 = '<button onClick={() => setShowLoginModal(true)} className="block text-center w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold transition-colors">Upgrade to Pro</button>'
text = text.replace(pricing_old2, pricing_new2)

pricing_old3 = '<Link href="/account" className="block text-center w-full py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold transition-colors">Get Advanced</Link>'
pricing_new3 = '<button onClick={() => setShowLoginModal(true)} className="block text-center w-full py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold transition-colors">Get Advanced</button>'
text = text.replace(pricing_old3, pricing_new3)

# 6. Inject the LoginModal component just before the closing </div> of LandingPage
text = text.replace('    </div>\n  );\n}', '      <LoginModal isOpen={showLoginModal} onClose={() => setShowLoginModal(false)} />\n    </div>\n  );\n}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
    print("page.tsx updated")
