with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# We append to the existing CSS block
old_css_end = '/* Customizing Streamlit Tabs to look modern */'
new_css_additions = '''
/* Ultra-modern Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.02);
}
::-webkit-scrollbar-thumb {
    background: rgba(0, 240, 255, 0.3);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(138, 43, 226, 0.6);
}

/* Glassmorphism Buttons */
div[data-testid="stButton"] > button {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(5px);
    transition: all 0.3s ease;
    border-radius: 8px;
}
div[data-testid="stButton"] > button:hover {
    border-color: #00F0FF;
    box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
    transform: translateY(-2px);
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0);
}

/* Primary Button Glow */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(90deg, rgba(0, 240, 255, 0.2), rgba(138, 43, 226, 0.2));
    border: 1px solid #00F0FF;
    font-weight: bold;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    box-shadow: 0 0 20px rgba(138, 43, 226, 0.4);
}

/* Inputs & Selectboxes Glass */
div[data-baseweb="select"] > div, 
div[data-baseweb="input"] > div {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 6px;
    backdrop-filter: blur(4px);
    transition: border-color 0.3s ease;
}
div[data-baseweb="select"]:hover > div, 
div[data-baseweb="input"]:hover > div {
    border-color: #00F0FF !important;
}

/* Customizing Streamlit Tabs to look modern */'''

content = content.replace(old_css_end, new_css_additions)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Futuristic components (buttons, scrollbar, inputs) added to CSS.")
