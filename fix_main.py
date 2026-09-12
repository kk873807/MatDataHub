import os

with open('app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add standard entrypoint for Render
entrypoint = '''
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
'''

if 'if __name__ == "__main__":' not in content:
    with open('app/main.py', 'a', encoding='utf-8') as f:
        f.write('\n' + entrypoint)
        
print("Updated app/main.py")
