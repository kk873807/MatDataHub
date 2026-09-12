"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  Database, Home, BarChart3, Bot, Workflow, 
  BookOpen, User, ShieldAlert, Crown, Shield, Menu, X, FileText, HelpCircle, MessageSquare, ChevronDown, Settings, CreditCard, LifeBuoy, Keyboard, LogOut } from "lucide-react";
import { API } from "@/lib/api";
import { ThemeToggle } from "./ThemeToggle";
import { LoginModal } from "./LoginModal";

type NavItem = {
  name: string;
  href?: string;
  icon: any;
  subItems?: { name: string; href: string }[];
};

const appNavItems: NavItem[] = [
  { name: "Dashboard", href: "/dashboard", icon: Home },
  { name: "Materials", href: "/materials", icon: Database },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
  { name: "Workspaces", href: "/projects", icon: Workflow },
  { name: "Blog", href: "/blog", icon: FileText },
  { 
    name: "Help & Support", 
    icon: HelpCircle,
    subItems: [
      { name: "FAQs", href: "/faq" },
      { name: "Support Centre", href: "/contact" }
    ]
  },
  { name: "Feedback", href: "/feedback", icon: MessageSquare },
];

export function TopNav() {
  const pathname = usePathname();
  const isLanding = pathname === "/";
  const [userInfo, setUserInfo] = useState<{ name: string; tier: string; is_admin: boolean } | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [authChecked, setAuthChecked] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setIsLoggedIn(true);
      fetch(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(r => r.ok ? r.json() : null)
        .then(data => {
          if (data) setUserInfo({ name: data.name || data.email, tier: data.tier, is_admin: data.is_admin || false });
        })
        .catch(() => {});
    }
    setAuthChecked(true);
    const handleOpenModal = () => setShowLoginModal(true);
    window.addEventListener('openLoginModal', handleOpenModal);
    return () => window.removeEventListener('openLoginModal', handleOpenModal);
  }, [pathname]);

  const tierColor = userInfo?.is_admin
    ? "bg-red-100 text-red-600 dark:bg-red-100 dark:bg-red-900/40 dark:text-red-600 dark:text-red-400 border-red-200 dark:border-red-200 dark:border-red-800/50"
    : userInfo?.tier === "advanced"
    ? "bg-emerald-100 text-emerald-600  dark:bg-emerald-900/40 dark:text-emerald-600 dark:text-emerald-400 border-emerald-200 dark:border-emerald-200 dark:border-emerald-800/50"
    : userInfo?.tier === "pro"
    ? "bg-blue-100 text-blue-600 dark:bg-blue-100 dark:bg-blue-900/40 dark:text-blue-600 dark:text-blue-400 border-blue-200 dark:border-blue-200 dark:border-blue-800/50"
    : "bg-slate-100 text-slate-600 dark:text-slate-300 dark:bg-slate-800 dark:text-slate-400 border-slate-200 dark:border-slate-700";

  const tierLabel = userInfo?.is_admin ? "Admin" : (userInfo?.tier || "free").charAt(0).toUpperCase() + (userInfo?.tier || "free").slice(1);

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };


  return (
    <>
      <nav className="sticky top-0 w-full border-b border-slate-200 dark:border-slate-800/50 bg-white/80 dark:bg-slate-950/80 backdrop-blur-xl z-50 transition-colors">
        <div className="max-w-[1600px] mx-auto px-4 md:px-6 h-16 flex items-center justify-between">
          
          <div className="flex items-center gap-6">
            <Link href="/" className="flex items-center gap-2 group">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-600 to-violet-600 flex items-center justify-center shadow-lg shadow-blue-500/20 group-hover:shadow-blue-500/40 transition-all">
                <Database className="w-4 h-4 text-white" />
              </div>
              <span className="font-bold text-xl tracking-tight text-slate-900 dark:text-white" style={{ fontFamily: "var(--font-red-hat)" }}>MatDataHub</span>
            </Link>

            {!isLanding && (
              <div className="hidden lg:flex items-center gap-1 ml-4">
                {appNavItems.map((item) => {
                  if (item.subItems) {
                    return (
                      <div key={item.name} className="relative group">
                        <button className="flex items-center gap-1.5 px-3 py-2 rounded-full text-sm font-medium transition-all text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-white">
                          <item.icon className="w-4 h-4" />
                          {item.name}
                          <ChevronDown className="w-3 h-3 ml-0.5 opacity-50" />
                        </button>
                        <div className="absolute top-full left-0 mt-2 w-48 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all flex flex-col p-2 z-50">
                          {item.subItems.map(sub => (
                            <Link key={sub.name} href={sub.href} className="px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors">
                              {sub.name}
                            </Link>
                          ))}
                        </div>
                      </div>
                    );
                  }

                  const isActive = item.href && (pathname === item.href || (item.href !== "/" && pathname?.startsWith(item.href)));
                  return (
                    <Link
                      key={item.name}
                      href={item.href!}
                      className={`flex items-center gap-2 px-3 py-2 rounded-full text-sm font-medium transition-all ${
                        isActive 
                          ? "bg-slate-900 text-white dark:bg-slate-800 dark:text-blue-400" 
                          : "text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-white"
                      }`}
                    >
                      <item.icon className="w-4 h-4" />
                      {item.name}
                    </Link>
                  );
                })}
              </div>
            )}
          </div>

          <div className="flex items-center gap-4">
            
            {isLanding && (
              <div className="hidden md:flex items-center gap-6 mr-2">
                <Link href="#problem" className="text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-600 dark:text-blue-400 transition-colors">Problem</Link>
                <Link href="#solution" className="text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-600 dark:text-blue-400 transition-colors">Platform</Link>
                <Link href="#pricing" className="text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-600 dark:text-blue-400 transition-colors">Pricing</Link>
                <Link href="#blog" className="text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-600 dark:text-blue-400 transition-colors">Blog</Link>
              </div>
            )}

            <ThemeToggle />

            {authChecked && (
              isLoggedIn ? (
                <div className="flex items-center gap-3">
                  {!isLanding && (
                    <div className="hidden md:flex items-center gap-3">
                      
                      {userInfo?.is_admin && <Link href="/admin" className="p-2 rounded-full text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors" title="Admin"><ShieldAlert className="w-5 h-5" /></Link>}
                    </div>
                  )}
                  {isLanding ? (
                    <Link href="/dashboard" className="text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 px-5 py-2.5 rounded-full transition-all shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40">
                      Go to App
                    </Link>
                  ) : (
                    <div className="relative group">
                      <button className="flex items-center gap-2 pl-2 pr-3 py-1.5 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
                        <div className="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-violet-500 flex items-center justify-center text-white font-bold text-xs">
                          {userInfo?.name.charAt(0).toUpperCase() || "U"}
                        </div>
                        <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border ${tierColor}`}>
                          {tierLabel}
                        </span>
                        <ChevronDown className="w-3 h-3 text-slate-400" />
                      </button>
                      
                      <div className="absolute top-full right-0 mt-2 w-56 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all flex flex-col p-2 z-50">
                        <div className="px-3 py-2 mb-2 border-b border-slate-100 dark:border-slate-800">
                          <p className="text-sm font-bold text-slate-900 dark:text-white truncate">{userInfo?.name || "User"}</p>
                          <p className="text-xs text-slate-500 dark:text-slate-400">{tierLabel} Plan</p>
                        </div>
                        <Link href="/account" className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors">
                          <Settings className="w-4 h-4" /> Account Management
                        </Link>
                        <Link href="/account?tab=billing" className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors">
                          <CreditCard className="w-4 h-4" /> Transactions & Billing
                        </Link>
                        <Link href="/contact" className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors">
                          <LifeBuoy className="w-4 h-4" /> Help Centre & Legal
                        </Link>
                        <button onClick={() => alert('Keyboard shortcuts:\nCtrl+K: Search\nCtrl+/: Shortcuts')} className="w-full flex items-center gap-2 px-3 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white rounded-xl transition-colors text-left">
                          <Keyboard className="w-4 h-4" /> Keyboard Shortcuts
                        </button>
                        <div className="h-px bg-slate-100 dark:bg-slate-800 my-1"></div>
                        <button onClick={handleLogout} className="w-full flex items-center gap-2 px-3 py-2 text-sm font-medium text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-xl transition-colors text-left">
                          <LogOut className="w-4 h-4" /> Sign Out
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <button onClick={() => setShowLoginModal(true)} className="text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 px-5 py-2.5 rounded-full transition-all shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40">
                  Sign In
                </button>
              )
            )}

            <button className="lg:hidden p-2 text-slate-600 dark:text-slate-300" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
              {mobileMenuOpen ? <X /> : <Menu />}
            </button>
          </div>
        </div>

        {mobileMenuOpen && (
          <div className="lg:hidden border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 p-4 space-y-2 shadow-xl">
            {isLanding ? (
              <div className="flex flex-col gap-4 p-2">
                <Link href="#problem" onClick={() => setMobileMenuOpen(false)} className="font-medium text-slate-700 dark:text-slate-200">Problem</Link>
                <Link href="#solution" onClick={() => setMobileMenuOpen(false)} className="font-medium text-slate-700 dark:text-slate-200">Platform</Link>
                <Link href="#pricing" onClick={() => setMobileMenuOpen(false)} className="font-medium text-slate-700 dark:text-slate-200">Pricing</Link>
                <Link href="#blog" onClick={() => setMobileMenuOpen(false)} className="font-medium text-slate-700 dark:text-slate-200">Blog</Link>
              </div>
            ) : (
              appNavItems.map(item => {
                if (item.subItems) {
                  return (
                    <div key={item.name} className="flex flex-col gap-1">
                      <div className="flex items-center gap-3 p-3 font-medium text-slate-400 dark:text-slate-500 uppercase text-[10px] tracking-wider mt-2">
                        <item.icon className="w-4 h-4" />
                        {item.name}
                      </div>
                      {item.subItems.map(sub => (
                        <Link 
                          key={sub.name} 
                          href={sub.href}
                          onClick={() => setMobileMenuOpen(false)}
                          className="flex items-center gap-3 p-3 pl-10 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 font-medium text-slate-700 dark:text-slate-200"
                        >
                          {sub.name}
                        </Link>
                      ))}
                    </div>
                  );
                }
                return (
                  <Link 
                    key={item.name} 
                    href={item.href!}
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex items-center gap-3 p-3 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 font-medium text-slate-700 dark:text-slate-200"
                  >
                    <item.icon className="w-5 h-5 text-blue-500" />
                    {item.name}
                  </Link>
                );
              })
            )}
          </div>
        )}
      </nav>

      <LoginModal isOpen={showLoginModal} onClose={() => setShowLoginModal(false)} />
    </>
  );
}
