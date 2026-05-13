

import plotly.graph_objects as go
from data import PLOT_BASE
# Custom CSS block to enforce specific branding, typography, and component styling.
# By setting `unsafe_allow_html=True` in Streamlit, this raw CSS targets the generated DOM elements.

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

*, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
code, pre, .mono { font-family: 'IBM Plex Mono', monospace !important; }

.hero { background: #0a0a0f; border: 1px solid #1e1e2e; border-radius: 16px; padding: 2.5rem 2rem 2rem; margin-bottom: 1.5rem; position: relative; overflow: hidden; }
.hero::before { content: ''; position: absolute; top: -60px; left: -60px; width: 220px; height: 220px; background: radial-gradient(circle, rgba(59,130,246,0.18) 0%, transparent 70%); border-radius: 50%; }
.hero::after { content: ''; position: absolute; bottom: -40px; right: -40px; width: 180px; height: 180px; background: radial-gradient(circle, rgba(249,115,22,0.15) 0%, transparent 70%); border-radius: 50%; }
.hero-title { font-family: 'IBM Plex Mono', monospace; font-size: 2rem; font-weight: 700; color: #f1f5f9; margin: 0 0 0.4rem; letter-spacing: -0.5px; }
.hero-sub { font-size: 0.9rem; color: #64748b; font-family: 'IBM Plex Mono', monospace; }
.tag { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 0.72rem; font-family: 'IBM Plex Mono', monospace; font-weight: 600; margin-left: 0.5rem; vertical-align: middle; }
.tag-cisc { background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
.tag-risc { background: rgba(249,115,22,0.15); color: #fb923c; border: 1px solid rgba(249,115,22,0.3); }

.panel { background: #0f0f1a; border-radius: 12px; padding: 1.2rem 1.4rem; border: 1px solid #1e1e2e; height: 100%; }
.panel-cisc { border-top: 3px solid #3b82f6; }
.panel-risc { border-top: 3px solid #f97316; }

.panel-title { font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 0.8rem; }
.panel-title-cisc { color: #3b82f6; }
.panel-title-risc { color: #f97316; }

.fact-row { display: flex; justify-content: space-between; align-items: center; padding: 0.35rem 0; border-bottom: 1px solid #1e1e2e; font-size: 0.82rem; }
.fact-row:last-child { border-bottom: none; }
.fact-label { color: #64748b; }
.fact-val { font-family: 'IBM Plex Mono', monospace; font-weight: 600; color: #e2e8f0; font-size: 0.8rem; }

.code-block { background: #070710; border-radius: 8px; padding: 1rem 1.2rem; font-family: 'IBM Plex Mono', monospace; font-size: 0.78rem; line-height: 1.9; border: 1px solid #1e1e2e; white-space: pre; overflow-x: auto; }
.c-kw  { color: #7dd3fc; } 
.c-reg { color: #86efac; } 
.c-mem { color: #fbbf24; } 
.c-num { color: #f9a8d4; } 
.c-cmt { color: #475569; font-style: italic; } 
.c-lbl { color: #c084fc; } 
.c-ok  { color: #4ade80; } 
.c-warn{ color: #fb923c; } 

.result-box { background: #070710; border-radius: 8px; padding: 0.8rem 1rem; border: 1px solid #1e1e2e; font-family: 'IBM Plex Mono', monospace; font-size: 0.76rem; line-height: 1.8; }
.exec-line { color: #94a3b8; }
.exec-highlight { color: #fbbf24; }

.pill { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 6px; font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; font-weight: 600; margin: 3px; }
.pill-if  { background: rgba(124,58,237,0.25); color: #a78bfa; }
.pill-id  { background: rgba(59,130,246,0.25); color: #60a5fa; }
.pill-ex  { background: rgba(16,185,129,0.25); color: #34d399; }
.pill-mem { background: rgba(245,158,11,0.25); color: #fbbf24; }
.pill-wb  { background: rgba(239,68,68,0.25);  color: #f87171; }
.pill-ud  { background: rgba(156,163,175,0.15);color: #6b7280; } 
.pill-stl { background: rgba(75,85,99,0.2);    color: #374151; border: 1px dashed #374151; }

.section-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #334155; margin: 1.8rem 0 0.8rem; }

div[data-testid="metric-container"] { background: #0f0f1a; border: 1px solid #1e1e2e; border-radius: 10px; padding: 0.7rem 1rem; }
div[data-testid="metric-container"] label { color: #64748b !important; font-size: 0.75rem !important; }
div[data-testid="metric-container"] [data-testid="metric-value"] { font-family: 'IBM Plex Mono', monospace !important; font-size: 1.6rem !important; color: #f1f5f9 !important; }

.stTabs [data-baseweb="tab"] { font-family: 'IBM Plex Mono', monospace; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.5px; }
.stSelectbox label, .stTextArea label { color: #64748b !important; font-size: 0.78rem !important; }
.stButton > button { font-family: 'IBM Plex Mono', monospace !important; font-weight: 600 !important; font-size: 0.82rem !important; letter-spacing: 0.5px; }
</style>
"""

def bar_chart(labels, vals_cisc, vals_risc, title, ylab=""):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=vals_cisc, name='CISC', marker_color='#3b82f6',
                          text=[str(v) for v in vals_cisc], textposition='outside', textfont=dict(size=10)))
    fig.add_trace(go.Bar(x=labels, y=vals_risc, name='RISC', marker_color='#f97316',
                          text=[str(v) for v in vals_risc], textposition='outside', textfont=dict(size=10)))
    fig.update_layout(**PLOT_BASE, title=dict(text=title, font=dict(size=13, color='#cbd5e1')),
                       barmode='group', height=280,
                       xaxis=dict(color='#475569', gridcolor='rgba(255,255,255,0.04)'),
                       yaxis=dict(color='#475569', title=ylab, gridcolor='rgba(255,255,255,0.04)'),
                       legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94a3b8')))
    return fig

def pipeline_html(n_instr: int, stages: list, colors: list, stall_cells: set = set()):
    cells = ""
    for i in range(n_instr):
        cells += f'<div style="color:#475569;font-size:0.7rem;display:flex;align-items:center;padding:2px 6px;font-family:IBM Plex Mono">I{i+1}</div>'
        for j, (stage, color) in enumerate(zip(stages, colors)):
            cycle = i + j
            is_stall = (i, j) in stall_cells
            bg = 'rgba(30,30,46,0.8)' if is_stall else color
            label = '—' if is_stall else stage
            opacity = '0.25' if is_stall else '0.9'
            cells += f'''<div style="
                background:{bg}; opacity:{opacity};
                border-radius:5px; padding:3px 0; margin:2px;
                font-family:IBM Plex Mono; font-size:0.65rem; font-weight:600;
                color:#fff; text-align:center; min-width:38px;
                grid-column:{cycle+2};">{label}</div>'''
    n_cols = n_instr + len(stages)
    header = '<div></div>' + ''.join(
        f'<div style="color:#334155;font-size:0.62rem;font-family:IBM Plex Mono;text-align:center;padding-bottom:4px">C{c+1}</div>'
        for c in range(n_cols))
    # Wrap headers and rows into the parent CSS Grid container
    return f'''<div style="
        display:grid;
        grid-template-columns: 28px repeat({n_cols}, minmax(38px,1fr));
        gap:3px; background:#070710; border-radius:10px;
        border:1px solid #1e1e2e; padding:12px 10px;">
        {header}{cells}</div>'''