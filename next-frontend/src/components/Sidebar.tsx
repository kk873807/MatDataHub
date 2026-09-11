"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Database, Calculator, Workflow, User, Bot, BarChart3, BookOpen, MessageSquare, PanelLeftClose, PanelRightClose, ShieldAlert, Crown, Shield } from "lucide-react";
import { API } from "@/lib/api";

const navItems = [
  { name: "Dashboard", href: "/", icon: Home },
  { name: "Browse Materials", href: "/materials", icon: Database },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
  { name: "Ask AI Adviser", href: "/ai", icon: Bot },
  { name: "Workspaces", href: "/projects", icon: Workflow },
  { name: "Resources", href: "/resources", icon: BookOpen },
  { name: "Community", href: "/feedback", icon: MessageSquare },
  { name: "Account", href: "/account", icon: User },
  { name: "Admin Portal", href: "/admin", icon: ShieldAlert },
];

export function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);
  const [userInfo, setUserInfo] = useState<{ name: string; tier: string; is_admin: boolean } | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;
    fetch(`${API}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(r => r.ok ? r.json() : null)
      .then(data => {
        if (data) setUserInfo({ name: data.name || data.email, tier: data.tier, is_admin: data.is_admin || false });
      })
      .catch(() => {});
  }, []);

  const tierColor = userInfo?.is_admin
    ? "bg-red-900/40 text-red-400 border-red-800/50"
    : userInfo?.tier === "advanced"
    ? "bg-emerald-900/40 text-emerald-400 border-emerald-800/50"
    : userInfo?.tier === "pro"
    ? "bg-blue-900/40 text-blue-400 border-blue-800/50"
    : "bg-slate-800 text-slate-400 border-slate-700";

  const tierLabel = userInfo?.is_admin ? "Admin" : (userInfo?.tier || "free").charAt(0).toUpperCase() + (userInfo?.tier || "free").slice(1);

  return (
    <aside className={`${collapsed ? 'w-20' : 'w-64'} bg-slate-950 border-r border-slate-800 h-screen sticky top-0 flex-col hidden md:flex transition-all duration-300 z-50`}>
      <div className="p-4 border-b border-slate-800 flex items-center justify-between h-[73px]">
        {!collapsed && (
          <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400 truncate">
            MatDataHub
          </h1>
        )}
        <button 
          onClick={() => setCollapsed(!collapsed)} 
          className={`p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors ${collapsed ? 'mx-auto' : ''}`}
          title="Toggle Sidebar"
        >
          {collapsed ? <PanelRightClose className="w-5 h-5" /> : <PanelLeftClose className="w-5 h-5" />}
        </button>
      </div>
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto overflow-x-hidden">
        {navItems.map((item) => {
          const isActive = pathname === item.href || (item.href !== "/" && pathname?.startsWith(item.href));
          return (
            <Link 
              key={item.name} 
              href={item.href} 
              title={collapsed ? item.name : undefined}
              className={`relative flex items-center ${collapsed ? 'justify-center' : 'gap-3'} px-4 py-3 rounded-xl transition-all duration-200 ${isActive 
                ? 'bg-gradient-to-r from-slate-800 to-slate-800/60 text-white shadow-lg shadow-slate-900/50' 
                : 'text-slate-400 hover:bg-slate-800/50 hover:text-white'}`}
            >
              {/* Active route left accent */}
              {isActive && (
                <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-emerald-500 rounded-r-full shadow-lg shadow-emerald-500/50"></div>
              )}
              <item.icon className={`w-5 h-5 flex-shrink-0 ${isActive ? 'text-emerald-400' : ''}`} />
              {!collapsed && <span className="font-medium whitespace-nowrap">{item.name}</span>}
            </Link>
          );
        })}
      </nav>

      {/* User Info Footer */}
      <div className={`border-t border-slate-800 ${collapsed ? 'p-2' : 'p-4'}`}>
        {userInfo ? (
          <div className={`flex items-center ${collapsed ? 'justify-center' : 'gap-3'}`}>
            <div className="w-9 h-9 rounded-full bg-gradient-to-br from-emerald-500 to-blue-500 flex items-center justify-center text-white font-bold text-sm flex-shrink-0 shadow-lg">
              {userInfo.name.charAt(0).toUpperCase()}
            </div>
            {!collapsed && (
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold text-white truncate">{userInfo.name.split("@")[0]}</p>
                <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border ${tierColor}`}>
                  {userInfo.is_admin ? <Shield className="w-3 h-3" /> : <Crown className="w-3 h-3" />}
                  {tierLabel}
                </span>
              </div>
            )}
          </div>
        ) : (
          !collapsed && (
            <div className="text-xs text-slate-600 text-center">
              MatDataHub © 2026
            </div>
          )
        )}
      </div>
    </aside>
  );
}
