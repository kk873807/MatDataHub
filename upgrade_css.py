with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# We want to upgrade the CSS block.
old_css_start = "# --- THEME-AWARE CSS ---"
old_css_end = '""", unsafe_allow_html=True)'

start_idx = content.find(old_css_start)
end_idx = content.find(old_css_end, start_idx) + len(old_css_end)

new_css = '''# --- THEME-AWARE CSS ---
st.markdown("""
<style>
/* Futuristic Glassmorphism Theme */
:root {
    --glass-bg: rgba(255, 255, 255, 0.05);
    --glass-border: rgba(255, 255, 255, 0.1);
    --neon-green: #00F0FF; /* Cyberpunk cyan/green */
    --neon-purple: #8A2BE2;
}

[data-testid="stAppViewContainer"] {
    background-color: transparent;
}

.hero-section {
    background: linear-gradient(135deg, rgba(0, 240, 255, 0.05) 0%, rgba(138, 43, 226, 0.05) 100%);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 3rem 2rem; 
    border-radius: 16px; 
    border: 1px solid var(--glass-border);
    margin-bottom: 2.5rem; 
    text-align: center; 
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    animation: glow 4s infinite alternate;
}

@keyframes glow {
    from { box-shadow: 0 0 10px rgba(0, 240, 255, 0.05); }
    to { box-shadow: 0 0 20px rgba(138, 43, 226, 0.1); }
}

.hero-title {
    color: var(--text-color); 
    font-size: 3.5rem; 
    margin-bottom: 0.5rem; 
    font-weight: 900; 
    letter-spacing: -1.5px;
    background: -webkit-linear-gradient(45deg, #00F0FF, #8A2BE2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: var(--text-color); 
    opacity: 0.85;
    font-size: 1.25rem; 
    max-width: 750px; 
    margin: 0 auto; 
    line-height: 1.6;
    font-weight: 300;
}

.cyber-stat {
    background: var(--glass-bg);
    backdrop-filter: blur(8px);
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 1.5rem 1rem;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.cyber-stat:hover {
    border-color: var(--neon-green);
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 10px 25px rgba(0, 240, 255, 0.15);
}

.cyber-num {
    font-size: 2.5rem;
    font-weight: 900;
    color: var(--text-color);
    margin-bottom: 0.2rem;
    background: -webkit-linear-gradient(45deg, #00F0FF, #8A2BE2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.cyber-label {
    font-size: 0.85rem;
    color: var(--text-color);
    opacity: 0.7;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 700;
}

.domain-card {
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid var(--glass-border);
    height: 100%;
    transition: all 0.3s ease;
}

.domain-card:hover {
    border-color: var(--neon-purple);
    box-shadow: 0 8px 20px rgba(138, 43, 226, 0.15);
    transform: translateY(-3px);
}

.domain-card p {
    color: var(--text-color);
    opacity: 0.8;
    font-size: 0.95rem;
    margin-bottom: 0;
    line-height: 1.5;
}

.domain-card h4 {
    margin-top: 0;
    color: var(--text-color);
    font-weight: 800;
    letter-spacing: -0.5px;
}

/* Customizing Streamlit Tabs to look modern */
div[data-testid="stTabs"] button {
    font-weight: 600;
    font-size: 1rem;
}

</style>
""", unsafe_allow_html=True)'''

content = content[:start_idx] + new_css + content[end_idx:]

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Ultra-modern glassmorphic CSS injected!")
