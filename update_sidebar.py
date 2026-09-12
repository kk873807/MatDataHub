import os
path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\components\Sidebar.tsx'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove "Website Home" from navItems array
text = text.replace('  { name: "Website Home", href: "/", icon: Globe },\n', '')

# 2. Add Globe button to the sidebar header
header_search = """        <button 
          onClick={() => setCollapsed(!collapsed)} 
          className={`p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors ${collapsed ? 'mx-auto' : ''}`}
          title="Toggle Sidebar"
        >
          {collapsed ? <PanelRightClose className="w-5 h-5" /> : <PanelLeftClose className="w-5 h-5" />}
        </button>"""

header_replace = """        <div className={`flex items-center gap-1 ${collapsed ? 'mx-auto flex-col' : ''}`}>
          <Link 
            href="/" 
            className="p-2 rounded-lg text-slate-400 hover:text-indigo-400 hover:bg-slate-800 transition-colors"
            title="Go to Website Home"
          >
            <Globe className="w-5 h-5" />
          </Link>
          <button 
            onClick={() => setCollapsed(!collapsed)} 
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            title="Toggle Sidebar"
          >
            {collapsed ? <PanelRightClose className="w-5 h-5" /> : <PanelLeftClose className="w-5 h-5" />}
          </button>
        </div>"""

text = text.replace(header_search, header_replace)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
    print("Sidebar updated")
