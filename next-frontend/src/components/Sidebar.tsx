"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Database, Calculator, Workflow, User } from "lucide-react";

const navItems = [
  { name: "Dashboard", href: "/", icon: Home },
  { name: "Browse Materials", href: "/materials", icon: Database },
  { name: "Calculators", href: "/calculators", icon: Calculator },
  { name: "Workflows", href: "/projects", icon: Workflow },
  { name: "Account", href: "/account", icon: User },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-neutral-950 border-r border-neutral-800 h-screen sticky top-0 flex-col hidden md:flex">
      <div className="p-6 border-b border-neutral-800">
        <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
          MatDataHub
        </h1>
      </div>
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => {
          const isActive = pathname === item.href || (item.href !== "/" && pathname?.startsWith(item.href));
          return (
            <Link key={item.name} href={item.href} className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${isActive ? 'bg-neutral-800 text-white' : 'text-neutral-400 hover:bg-neutral-800/50 hover:text-white'}`}>
              <item.icon className="w-5 h-5" />
              <span className="font-medium">{item.name}</span>
            </Link>
          );
        })}
      </nav>
      <div className="p-4 border-t border-neutral-800 text-xs text-neutral-600 text-center">
        MatDataHub © 2026
      </div>
    </aside>
  );
}
