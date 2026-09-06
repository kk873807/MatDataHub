import sys
with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix 1: Primary Button CSS
old_primary = """div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(90deg, rgba(0, 240, 255, 0.2), rgba(138, 43, 226, 0.2));
    border: 1px solid #00F0FF;
    font-weight: bold;
}"""
new_primary = """div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(90deg, rgba(0, 240, 255, 0.2), rgba(138, 43, 226, 0.2));
    border: 1px solid #00F0FF;
    font-weight: bold;
    color: var(--text-color) !important;
}"""
content = content.replace(old_primary, new_primary)

# Fix 2: Radar Chart formatting
old_radar_base_color = "line_color='rgba(255, 255, 255, 0.4)',"
new_radar_base_color = "line_color='rgba(128, 128, 128, 0.6)',"
content = content.replace(old_radar_base_color, new_radar_base_color)

old_radar_base_fill = "fillcolor='rgba(255, 255, 255, 0.05)'"
new_radar_base_fill = "fillcolor='rgba(128, 128, 128, 0.1)'"
content = content.replace(old_radar_base_fill, new_radar_base_fill)

old_radar_layout = """                            fig.update_layout(
                                polar=dict(
                                    radialaxis=dict(visible=True, color='rgba(255,255,255,0.2)', gridcolor='rgba(255,255,255,0.1)'),
                                    angularaxis=dict(color='var(--text-color)', gridcolor='rgba(255,255,255,0.1)')
                                ),
                                showlegend=True,
                                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(family="sans-serif", size=12, color="var(--text-color)"),
                                margin=dict(l=20, r=20, t=20, b=20),
                                height=300
                            )"""

new_radar_layout = """                            fig.update_layout(
                                polar=dict(
                                    radialaxis=dict(visible=True, color='rgba(128,128,128,0.4)', gridcolor='rgba(128,128,128,0.2)', tickfont=dict(size=9)),
                                    angularaxis=dict(color='var(--text-color)', gridcolor='rgba(128,128,128,0.2)', tickfont=dict(size=10))
                                ),
                                showlegend=True,
                                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(family="sans-serif", size=10, color="var(--text-color)"),
                                margin=dict(l=20, r=20, t=20, b=20),
                                height=300
                            )"""
content = content.replace(old_radar_layout, new_radar_layout)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Applied fixes to buttons and radar chart!")
