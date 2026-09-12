import re

with open('src/components/TopNav.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update lucide-react imports
import_match = re.search(r'import \{([\s\S]*?)\} from "lucide-react";', content)
if import_match:
    imports = import_match.group(1)
    if 'FileText' not in imports:
        new_imports = imports.strip() + ", FileText, HelpCircle, MessageSquare, ChevronDown"
        content = content.replace(import_match.group(0), f'import {{ {new_imports} }} from "lucide-react";')

# 2. Update appNavItems array
old_nav_items = '''const appNavItems = [
  { name: "Dashboard", href: "/dashboard", icon: Home },
  { name: "Materials", href: "/materials", icon: Database },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
  { name: "Workspaces", href: "/projects", icon: Workflow },
];'''

new_nav_items = '''type NavItem = {
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
];'''

content = content.replace(old_nav_items, new_nav_items)

# 3. Update desktop rendering
old_desktop_map = '''{appNavItems.map((item) => {
                  const isActive = pathname === item.href || (item.href !== "/" && pathname?.startsWith(item.href));
                  return (
                    <Link
                      key={item.name}
                      href={item.href}
                      className={lex items-center gap-2 px-3 py-2 rounded-full text-sm font-medium transition-all }
                    >
                      <item.icon className="w-4 h-4" />
                      {item.name}
                    </Link>
                  );
                })}'''

new_desktop_map = '''{appNavItems.map((item) => {
                  if (item.subItems) {
                    return (
                      <div key={item.name} className="relative group">
                        <button className="flex items-center gap-1.5 px-3 py-2 rounded-full text-sm font-medium transition-all text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:text-slate-900 dark:hover:text-white">
                          <item.icon className="w-4 h-4" />
                          {item.name}
                          <ChevronDown className="w-3 h-3 ml-0.5" />
                        </button>
                        <div className="absolute top-full left-0 mt-1 w-48 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all flex flex-col p-1.5 z-50">
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
                      className={lex items-center gap-2 px-3 py-2 rounded-full text-sm font-medium transition-all }
                    >
                      <item.icon className="w-4 h-4" />
                      {item.name}
                    </Link>
                  );
                })}'''

content = content.replace(old_desktop_map, new_desktop_map)

# 4. Update mobile rendering
old_mobile_map = '''appNavItems.map(item => (
                <Link 
                  key={item.name} 
                  href={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center gap-3 p-3 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 font-medium text-slate-700 dark:text-slate-200"
                >
                  <item.icon className="w-5 h-5 text-blue-500" />
                  {item.name}
                </Link>
              ))'''

new_mobile_map = '''appNavItems.map(item => {
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
              })'''

content = content.replace(old_mobile_map, new_mobile_map)

with open('src/components/TopNav.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Modification complete")
