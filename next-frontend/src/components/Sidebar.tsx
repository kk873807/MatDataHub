"use client";
import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Database, Calculator, Workflow, User, Bot, BarChart3, BookOpen, MessageSquare, PanelLeftClose, PanelRightClose, ShieldAlert } from "lucide-react";

const navItems = [
  { name: "Dashboard", href: "/", icon: Home },
  { name: "Browse Materials", href: "/materials", icon: Database },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
  { name: "Ask AI Adviser", href: "/ai", icon: Bot },
  { name: "Workflows", href: "/projects", icon: Workflow },
  { name: "Resources", href: "/resources", icon: BookOpen },
  { name: "Community", href: "/feedback", icon: MessageSquare },
  { name: "Account", href: "/account", icon: User },
  { name: "Admin Portal", href: "/admin", icon: ShieldAlert },
];

export function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

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
      <nav className="flex-1 p-3 space-y-2 overflow-y-auto overflow-x-hidden">
        {navItems.map((item) => {
          const isActive = pathname === item.href || (item.href !== "/" && pathname?.startsWith(item.href));
          return (
            <Link 
              key={item.name} 
              href={item.href} 
              title={collapsed ? item.name : undefined}
              className={`flex items-center ${collapsed ? 'justify-center' : 'gap-3'} px-4 py-3 rounded-lg transition-colors ${isActive ? 'bg-slate-800 text-white' : 'text-slate-400 hover:bg-slate-800/50 hover:text-white'}`}
            >
              <item.icon className="w-5 h-5 flex-shrink-0" />
              {!collapsed && <span className="font-medium whitespace-nowrap">{item.name}</span>}
            </Link>
          );
        })}
      </nav>
      {!collapsed && (
        <div className="p-4 border-t border-slate-800 text-xs text-slate-600 text-center">
          MatDataHub © 2026
        </div>
      )}
    </aside>
  );
}
