import os

file_path = 'next-frontend/src/components/InteractiveFeatures.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Leaf import
if 'Leaf' not in content:
    content = content.replace('} from "lucide-react";', ', Leaf } from "lucide-react";')

# Fix tools: []
content = content.replace('icon: Leaf,\n    color: "bg-emerald-500",\n  },', 'icon: Leaf,\n    color: "bg-emerald-500",\n    tools: [],\n  },')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
