with open("frontend/app.py", "r", encoding="utf-8") as f:
    content = f.read()

old_chart = """                            import plotly.graph_objects as go
                            fig = go.Figure()
                            fig.add_trace(go.Scatterpolar(
                                  r=[5, 2.7, 310, 8.1],
                                  theta=['Cost','Density','Strength', 'Carbon'],
                                  fill='toself',
                                  name='Base Material'
                            ))
                            fig.add_trace(go.Scatterpolar(
                                  r=[res['cost'], res['density'], res['tensile'], res['carbon']],
                                  theta=['Cost','Density','Strength', 'Carbon'],
                                  fill='toself',
                                  name=res['name']
                            ))
                            fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
                            st.plotly_chart(fig, use_container_width=True)"""

new_chart = """                            import plotly.graph_objects as go
                            fig = go.Figure()
                            # Ultra-modern cyberpunk radar chart
                            fig.add_trace(go.Scatterpolar(
                                  r=[5, 2.7, 310, 8.1],
                                  theta=['Cost','Density','Strength', 'Carbon'],
                                  fill='toself',
                                  name='Base Material',
                                  line_color='#8A2BE2',
                                  fillcolor='rgba(138, 43, 226, 0.2)'
                            ))
                            fig.add_trace(go.Scatterpolar(
                                  r=[res['cost'], res['density'], res['tensile'], res['carbon']],
                                  theta=['Cost','Density','Strength', 'Carbon'],
                                  fill='toself',
                                  name=res['name'],
                                  line_color='#00F0FF',
                                  fillcolor='rgba(0, 240, 255, 0.4)'
                            ))
                            fig.update_layout(
                                polar=dict(
                                    radialaxis=dict(visible=True, color='rgba(255,255,255,0.3)', gridcolor='rgba(255,255,255,0.1)'),
                                    angularaxis=dict(color='var(--text-color)', gridcolor='rgba(255,255,255,0.1)')
                                ),
                                showlegend=True,
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(family="sans-serif", size=14, color="var(--text-color)"),
                                margin=dict(l=20, r=20, t=20, b=20)
                            )
                            st.plotly_chart(fig, use_container_width=True)"""

content = content.replace(old_chart, new_chart)

with open("frontend/app.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated chart to futuristic style.")
