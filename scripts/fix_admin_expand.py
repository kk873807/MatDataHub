import re

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\admin\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add State
if 'const [expandedUsers, setExpandedUsers]' not in content:
    content = content.replace(
        'const [error, setError] = useState("");',
        'const [error, setError] = useState("");\n  const [expandedUsers, setExpandedUsers] = useState<Record<number, boolean>>({});\n  const toggleExpand = (userId: number) => setExpandedUsers(prev => ({ ...prev, [userId]: !prev[userId] }));'
    )

# 2. Update Render Block
old_map = '''                            <div className="flex flex-wrap gap-2">
                              {c.materials.slice(0, 5).map((m: any) => ('''
new_map = '''                            <div className="flex flex-wrap gap-2">
                              {(expandedUsers[c.user.id] ? c.materials : c.materials.slice(0, 5)).map((m: any) => ('''
content = content.replace(old_map, new_map)

old_more = '''                              {c.materials.length > 5 && (
                                <div className="bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs flex items-center justify-center font-bold text-slate-500">
                                  +{c.materials.length - 5} more
                                </div>
                              )}'''
new_more = '''                              {!expandedUsers[c.user.id] && c.materials.length > 5 && (
                                <button onClick={() => toggleExpand(c.user.id)} className="bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs flex items-center justify-center font-bold text-slate-500 transition-colors cursor-pointer">
                                  +{c.materials.length - 5} more (Click to Expand)
                                </button>
                              )}
                              {expandedUsers[c.user.id] && c.materials.length > 5 && (
                                <button onClick={() => toggleExpand(c.user.id)} className="bg-slate-200 hover:bg-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 border border-slate-300 dark:border-slate-600 rounded-lg p-2 text-xs flex items-center justify-center font-bold text-slate-600 dark:text-slate-300 transition-colors cursor-pointer w-full mt-2">
                                  Show Less
                                </button>
                              )}'''
content = content.replace(old_more, new_more)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added UI expansion logic to admin/page.tsx")
