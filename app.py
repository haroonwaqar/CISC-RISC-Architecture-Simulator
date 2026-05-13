import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from simulators import CISC, RISC
from data import PRESETS, PLOT_BASE, SPEC_DATA, CPI_DATA, TRANSISTOR_DATA, PIPE_DATA
from ui_utils import CUSTOM_CSS, bar_chart, pipeline_html
# Initialize the Streamlit application page configuration. 
# 'wide' layout provides more horizontal space, which is ideal for side-by-side architecture comparisons.
st.set_page_config(page_title="CISC vs RISC", page_icon="⚡", layout="wide")

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="hero-title">
    CISC <span style="color:#334155">vs</span> RISC
    <span class="tag tag-cisc">x86</span>
    <span class="tag tag-risc">ARM / MIPS</span>
  </div>
  <div class="hero-sub">// Computer Architecture Simulator — interactive instruction execution & pipeline analysis</div>
</div>
""", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["  01 · Concepts  ", "  02 · Simulator  ", "  03 · Pipeline  ", "  04 · Benchmarks  "])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: CONCEPTS - Explains the high-level philosophical differences between architectures
with t1:
    st.markdown('<div class="section-label">Architecture Philosophy</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown("""
<div class="panel panel-cisc">
  <div class="panel-title panel-title-cisc">CISC — Complex Instruction Set</div>
  <div class="fact-row"><span class="fact-label">Philosophy</span><span class="fact-val">do more per instruction</span></div>
  <div class="fact-row"><span class="fact-label">Instruction size</span><span class="fact-val">variable  (1–15 bytes)</span></div>
  <div class="fact-row"><span class="fact-label">Instruction count</span><span class="fact-val">1,500 + (x86)</span></div>
  <div class="fact-row"><span class="fact-label">Memory access</span><span class="fact-val">any instruction</span></div>
  <div class="fact-row"><span class="fact-label">Registers</span><span class="fact-val">8–16 general purpose</span></div>
  <div class="fact-row"><span class="fact-label">Control unit</span><span class="fact-val">microcode (slower)</span></div>
  <div class="fact-row"><span class="fact-label">Pipeline depth</span><span class="fact-val">14–19 stages (modern)</span></div>
  <div class="fact-row"><span class="fact-label">Examples</span><span class="fact-val">Intel x86, AMD64</span></div>
  <div class="fact-row"><span class="fact-label">Dominant in</span><span class="fact-val">Desktop · Server</span></div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class="panel panel-risc">
  <div class="panel-title panel-title-risc">RISC — Reduced Instruction Set</div>
  <div class="fact-row"><span class="fact-label">Philosophy</span><span class="fact-val">simple instructions, fast</span></div>
  <div class="fact-row"><span class="fact-label">Instruction size</span><span class="fact-val">fixed  (4 bytes)</span></div>
  <div class="fact-row"><span class="fact-label">Instruction count</span><span class="fact-val">~100</span></div>
  <div class="fact-row"><span class="fact-label">Memory access</span><span class="fact-val">LOAD / STORE only</span></div>
  <div class="fact-row"><span class="fact-label">Registers</span><span class="fact-val">16–32 general purpose</span></div>
  <div class="fact-row"><span class="fact-label">Control unit</span><span class="fact-val">hardwired (faster)</span></div>
  <div class="fact-row"><span class="fact-label">Pipeline depth</span><span class="fact-val">5 stages (classic)</span></div>
  <div class="fact-row"><span class="fact-label">Examples</span><span class="fact-val">ARM, MIPS, RISC-V</span></div>
  <div class="fact-row"><span class="fact-label">Dominant in</span><span class="fact-val">Mobile · Embedded · now Mac</span></div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="section-label">Key Difference — Memory Access Model</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown("""
<div class="code-block"><span class="c-cmt">; CISC x86 — ADD can reach into memory</span>
<span class="c-kw">MOV</span>  <span class="c-reg">EAX</span>, <span class="c-mem">[100]</span>      <span class="c-cmt">; load A</span>
<span class="c-kw">ADD</span>  <span class="c-reg">EAX</span>, <span class="c-mem">[104]</span>      <span class="c-cmt">; add B from memory ← CISC</span>
<span class="c-kw">MOV</span>  <span class="c-mem">[200]</span>, <span class="c-reg">EAX</span>      <span class="c-cmt">; store result</span>

<span class="c-ok">✓ 3 instructions  |  ~7 cycles</span></div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="code-block"><span class="c-cmt"># RISC MIPS — only LOAD/STORE touch memory</span>
<span class="c-kw">LOAD</span>  <span class="c-reg">R1</span>, <span class="c-num">100</span>         <span class="c-cmt"># R1 = MEM[100]</span>
<span class="c-kw">LOAD</span>  <span class="c-reg">R2</span>, <span class="c-num">104</span>         <span class="c-cmt"># R2 = MEM[104]</span>
<span class="c-kw">ADD</span>   <span class="c-reg">R3</span>, <span class="c-reg">R1</span>, <span class="c-reg">R2</span>     <span class="c-cmt"># R3 = R1 + R2   ← RISC</span>
<span class="c-kw">STORE</span> <span class="c-reg">R3</span>, <span class="c-num">200</span>         <span class="c-cmt"># MEM[200] = R3</span>

<span class="c-warn">4 instructions  |  ~6 cycles  |  1 cycle each</span></div>
""", unsafe_allow_html=True)

    st.markdown('<div class="section-label">The Modern Reality</div>', unsafe_allow_html=True)
    st.info("**Modern x86 CPUs secretly decode CISC instructions into micro-ops (µops) — tiny RISC-like operations — before execution.** Intel Skylake decodes up to 5 µops/cycle. The execution engine IS a RISC core. CISC is the public interface; RISC is the engine inside.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: SIMULATOR - Live execution of assembly code
with t2:
    st.markdown('<div class="section-label">Interactive Instruction Simulator</div>', unsafe_allow_html=True)

    preset = st.selectbox("Load preset program", list(PRESETS.keys()), label_visibility="collapsed")

    ed1, ed2 = st.columns(2, gap="medium")
    with ed1:
        st.markdown('<span style="font-family:IBM Plex Mono;font-size:0.72rem;color:#3b82f6;font-weight:700;letter-spacing:1px">CISC PROGRAM  (x86-style)</span>', unsafe_allow_html=True)
        cisc_src = st.text_area("c", value=PRESETS[preset]["cisc"], height=220, key="csrc", label_visibility="collapsed")
    with ed2:
        st.markdown('<span style="font-family:IBM Plex Mono;font-size:0.72rem;color:#f97316;font-weight:700;letter-spacing:1px">RISC PROGRAM  (MIPS-style)</span>', unsafe_allow_html=True)
        risc_src = st.text_area("r", value=PRESETS[preset]["risc"], height=220, key="rsrc", label_visibility="collapsed")

    run = st.button("▶  Execute Both", type="primary", use_container_width=True)

    if run:
        ci, cc, cr, cm, cl = CISC().run(cisc_src)
        ri, rc, rr, rm, rl = RISC().run(risc_src)

        m1,m2,m3,m4 = st.columns(4)
        m1.metric("CISC Instructions", ci)
        m2.metric("RISC Instructions", ri, delta=f"+{ri-ci}" if ri>ci else str(ri-ci))
        m3.metric("CISC Cycles", cc)
        m4.metric("RISC Cycles", rc, delta=f"+{rc-cc}" if rc>cc else str(rc-cc))

        fig = bar_chart(["Instructions", "Cycles"], [ci, cc], [ri, rc], "Instruction count vs Cycle count")
        st.plotly_chart(fig, use_container_width=True)

        l1, l2 = st.columns(2, gap="medium")
        with l1:
            log_text = '\n'.join(cl)
            st.markdown(f'<div class="result-box"><span style="color:#3b82f6;font-weight:700">CISC execution log</span>\n{log_text}</div>', unsafe_allow_html=True)
        with l2:
            log_text2 = '\n'.join(rl)
            st.markdown(f'<div class="result-box"><span style="color:#f97316;font-weight:700">RISC execution log</span>\n{log_text2}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-label">Register State After Execution</div>', unsafe_allow_html=True)
        r1, r2 = st.columns(2, gap="medium")
        with r1:
            used = {k:v for k,v in cr.items() if v!=0}
            if used:
                df = pd.DataFrame(list(used.items()), columns=["Register","Value"])
                st.dataframe(df, use_container_width=True, hide_index=True)
        with r2:
            used2 = {k:v for k,v in rr.items() if v!=0}
            if used2:
                df2 = pd.DataFrame(list(used2.items()), columns=["Register","Value"])
                st.dataframe(df2, use_container_width=True, hide_index=True)

        all_keys = sorted(set(list(cm.keys())+list(rm.keys())))
        if all_keys:
            st.markdown('<div class="section-label">Memory After Execution</div>', unsafe_allow_html=True)
            mem_df = pd.DataFrame({
                "Address": [f"MEM[{k}]" for k in all_keys],
                "CISC value": [cm.get(k,'—') for k in all_keys],
                "RISC value": [rm.get(k,'—') for k in all_keys],
            })
            st.dataframe(mem_df, use_container_width=True, hide_index=True)

        if ci < ri:
            st.success(f"CISC used **{ri-ci} fewer instructions** — complex ops pack more work per line. But RISC's {rc} cycles vs CISC's {cc} shows each RISC instruction is cheaper.")
        elif ri <= ci:
            st.success(f"RISC matched or beat CISC in instruction count here. With 1-cycle instructions, RISC often wins on throughput.")

    st.markdown('<div class="section-label">Instruction Reference</div>', unsafe_allow_html=True)
    ref1, ref2 = st.columns(2, gap="medium")
    with ref1:
        st.markdown("""
<div class="code-block"><span class="c-cmt">; CISC (x86) instruction set used here</span>
<span class="c-kw">DATA</span>  addr, val   <span class="c-cmt">; initialize memory (helper)</span>
<span class="c-kw">MOV</span>   dst, src    <span class="c-cmt">; move — src/dst can be [mem]   2 cyc</span>
<span class="c-kw">ADD</span>   dst, src    <span class="c-cmt">; add  — src can be [mem]       3 cyc</span>
<span class="c-kw">SUB</span>   dst, src    <span class="c-cmt">; sub  — src can be [mem]       3 cyc</span>
<span class="c-kw">IMUL</span>  dst, src    <span class="c-cmt">; signed multiply               4 cyc</span>
<span class="c-kw">INC</span>   reg         <span class="c-cmt">; increment by 1                1 cyc</span>
<span class="c-kw">DEC</span>   reg         <span class="c-cmt">; decrement by 1                1 cyc</span></div>
""", unsafe_allow_html=True)
    with ref2:
        st.markdown("""
<div class="code-block"><span class="c-cmt"># RISC (MIPS) instruction set used here</span>
<span class="c-kw">DATA</span>  addr, val   <span class="c-cmt"># initialize memory (helper)</span>
<span class="c-kw">MOV</span>   Rd, #imm    <span class="c-cmt"># load immediate into register   1 cyc</span>
<span class="c-kw">LOAD</span>  Rd, addr    <span class="c-cmt"># Rd ← MEM[addr]                2 cyc</span>
<span class="c-kw">STORE</span> Rs, addr    <span class="c-cmt"># MEM[addr] ← Rs               2 cyc</span>
<span class="c-kw">ADD</span>   Rd, Ra, Rb  <span class="c-cmt"># Rd = Ra + Rb  (reg only)      1 cyc</span>
<span class="c-kw">SUB</span>   Rd, Ra, Rb  <span class="c-cmt"># Rd = Ra - Rb                  1 cyc</span>
<span class="c-kw">MUL</span>   Rd, Ra, Rb  <span class="c-cmt"># Rd = Ra × Rb                  1 cyc</span></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: PIPELINE - Visualizes instruction pipelining and hazards
with t3:
    st.markdown('<div class="section-label">Pipeline Visualizer</div>', unsafe_allow_html=True)

    n = st.slider("Number of instructions", 3, 7, 4, key="pipe_n")

    p1, p2 = st.columns(2, gap="medium")

    risc_stages  = ["IF","ID","EX","MEM","WB"]
    risc_colors  = ["#6d28d9","#2563eb","#059669","#d97706","#dc2626"]

    cisc_stages  = ["IF","ID","µDEC","EX","EX2","MEM","WB"]
    cisc_colors  = ["#6d28d9","#2563eb","#0891b2","#059669","#65a30d","#d97706","#dc2626"]

    with p1:
        st.markdown('<span style="font-family:IBM Plex Mono;font-size:0.72rem;color:#f97316;font-weight:700;letter-spacing:1px">RISC — 5-stage pipeline (MIPS classic)</span>', unsafe_allow_html=True)
        legend = " ".join(
            f'<span style="background:{c}22;color:{c};border:1px solid {c}44;border-radius:4px;padding:2px 8px;font-family:IBM Plex Mono;font-size:0.68rem;font-weight:600;margin:2px">{s}</span>'
            for s,c in zip(risc_stages, risc_colors))
        st.markdown(legend, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(pipeline_html(n, risc_stages, [c+'44' for c in risc_colors]), unsafe_allow_html=True)
        total = n + len(risc_stages) - 1
        st.markdown(f'<div style="font-family:IBM Plex Mono;font-size:0.75rem;color:#64748b;margin-top:10px">{n} instructions → <span style="color:#f97316">{total} cycles</span>  ·  CPI after fill: <span style="color:#4ade80">1.0</span></div>', unsafe_allow_html=True)

    with p2:
        st.markdown('<span style="font-family:IBM Plex Mono;font-size:0.72rem;color:#3b82f6;font-weight:700;letter-spacing:1px">CISC — 7-stage pipeline (x86 simplified)</span>', unsafe_allow_html=True)
        legend2 = " ".join(
            f'<span style="background:{c}22;color:{c};border:1px solid {c}44;border-radius:4px;padding:2px 8px;font-family:IBM Plex Mono;font-size:0.68rem;font-weight:600;margin:2px">{s}</span>'
            for s,c in zip(cisc_stages, cisc_colors))
        st.markdown(legend2, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(pipeline_html(n, cisc_stages, [c+'44' for c in cisc_colors]), unsafe_allow_html=True)
        total2 = n + len(cisc_stages) - 1
        st.markdown(f'<div style="font-family:IBM Plex Mono;font-size:0.75rem;color:#64748b;margin-top:10px">{n} instructions → <span style="color:#3b82f6">{total2} cycles</span>  ·  +µDecode stage overhead</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Hazards & Stalls</div>', unsafe_allow_html=True)

    h1, h2, h3 = st.columns(3, gap="medium")
    with h1:
        st.markdown("""
<div class="panel panel-risc" style="border-top-color:#dc2626">
  <div class="panel-title" style="color:#f87171">DATA HAZARD (RAW)</div>
  <div style="font-size:0.8rem;color:#94a3b8;margin-bottom:0.6rem">Read-After-Write: next instruction needs a result not yet written back.</div>
</div>
""", unsafe_allow_html=True)
        st.markdown("""
<div class="code-block" style="font-size:0.72rem"><span class="c-kw">ADD</span>  <span class="c-reg">R3</span>, R1, R2   <span class="c-cmt"># writes R3</span>
<span class="c-kw">SUB</span>  <span class="c-reg">R4</span>, <span class="c-warn">R3</span>, R5   <span class="c-cmt"># needs R3 ← stall!</span>

<span class="c-ok">Fix: forwarding / bypassing</span>
<span class="c-cmt">routes EX output → EX input</span>
<span class="c-cmt">eliminates most stalls</span></div>
""", unsafe_allow_html=True)

    with h2:
        st.markdown("""
<div class="panel panel-cisc" style="border-top-color:#f59e0b">
  <div class="panel-title" style="color:#fbbf24">CONTROL HAZARD</div>
  <div style="font-size:0.8rem;color:#94a3b8;margin-bottom:0.6rem">Branch: CPU doesn't know next instruction until branch resolves.</div>
</div>
""", unsafe_allow_html=True)
        st.markdown("""
<div class="code-block" style="font-size:0.72rem"><span class="c-kw">BEQ</span>  R1, R2, <span class="c-lbl">label</span>
<span class="c-cmt">; pipeline already fetched</span>
<span class="c-cmt">; 2–3 wrong instructions!</span>

<span class="c-warn">RISC fix:</span> <span class="c-cmt">branch delay slot</span>
<span class="c-warn">x86 fix:</span>  <span class="c-cmt">branch predictor</span>
<span class="c-cmt">~99% accuracy, 19-cycle</span>
<span class="c-cmt">penalty on miss (Skylake)</span></div>
""", unsafe_allow_html=True)

    with h3:
        st.markdown("""
<div class="panel panel-cisc" style="border-top-color:#8b5cf6">
  <div class="panel-title" style="color:#a78bfa">STRUCTURAL HAZARD</div>
  <div style="font-size:0.8rem;color:#94a3b8;margin-bottom:0.6rem">Two instructions compete for the same hardware unit at the same time.</div>
</div>
""", unsafe_allow_html=True)
        st.markdown("""
<div class="code-block" style="font-size:0.72rem"><span class="c-cmt">; e.g. two instructions both</span>
<span class="c-cmt">; need the memory port</span>

<span class="c-warn">More severe in CISC</span>
<span class="c-cmt">complex instructions hold</span>
<span class="c-cmt">resources for many cycles</span>

<span class="c-ok">RISC fix:</span> <span class="c-cmt">Harvard cache</span>
<span class="c-cmt">separate I-cache & D-cache</span></div>
""", unsafe_allow_html=True)

    st.markdown('<div class="section-label">Real Pipeline Depths</div>', unsafe_allow_html=True)
    df_p = pd.DataFrame(PIPE_DATA)
    colors_p = ['#f97316' if a=='RISC' else '#3b82f6' for a in df_p['Arch']]
    fig_p = go.Figure(go.Bar(x=df_p["Processor"], y=df_p["Stages"],
                               marker_color=colors_p, text=df_p["Stages"], textposition='outside'))
    fig_p.update_layout(**PLOT_BASE, height=260,
                         xaxis=dict(color='#475569', tickangle=-20, tickfont=dict(size=9)),
                         yaxis=dict(color='#475569', title="Pipeline Stages", gridcolor='rgba(255,255,255,0.04)'))
    st.plotly_chart(fig_p, use_container_width=True)
    st.caption("Intel Pentium 4's 31-stage pipeline meant a 31-cycle branch penalty on misprediction — a famous design mistake.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4: BENCHMARKS - Real-world data visualization
with t4:
    st.markdown('<div class="section-label">Real-World Performance Data</div>', unsafe_allow_html=True)

    df_s = pd.DataFrame(SPEC_DATA)
    df_s["PPW"] = (df_s["Score"]/df_s["TDP"]).round(3)

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        colors_s = ['#3b82f6' if a=='CISC' else '#f97316' for a in df_s['Arch']]
        fig_s = go.Figure(go.Bar(x=df_s["Processor"], y=df_s["Score"],
                                   marker_color=colors_s, text=df_s["Score"], textposition='outside'))
        fig_s.update_layout(**PLOT_BASE, height=270,
                              title=dict(text="SPECint_rate2017 Score", font=dict(size=12,color='#cbd5e1')),
                              xaxis=dict(color='#475569', tickangle=-15, tickfont=dict(size=9)),
                              yaxis=dict(color='#475569', gridcolor='rgba(255,255,255,0.04)'))
        st.plotly_chart(fig_s, use_container_width=True)

    with c2:
        fig_ppw = go.Figure(go.Bar(x=df_s["Processor"], y=df_s["PPW"],
                                     marker_color=colors_s, text=df_s["PPW"], textposition='outside'))
        fig_ppw.update_layout(**PLOT_BASE, height=270,
                               title=dict(text="Performance per Watt (score / TDP)", font=dict(size=12,color='#cbd5e1')),
                               xaxis=dict(color='#475569', tickangle=-15, tickfont=dict(size=9)),
                               yaxis=dict(color='#475569', gridcolor='rgba(255,255,255,0.04)'))
        st.plotly_chart(fig_ppw, use_container_width=True)

    st.markdown('<div class="section-label">CPI by Workload Type</div>', unsafe_allow_html=True)

    fig_cpi = bar_chart(CPI_DATA["wl_names"], CPI_DATA["cisc_cpi"], CPI_DATA["risc_cpi"], "Average CPI — lower is better", "Cycles per Instruction")
    fig_cpi.add_shape(type='line', x0=-0.5, x1=4.5, y0=1.0, y1=1.0,
                       line=dict(color='#4ade80', width=1.5, dash='dot'))
    fig_cpi.add_annotation(x=4.6, y=1.0, text="ideal", showarrow=False,
                             font=dict(color='#4ade80', size=9, family='IBM Plex Mono'))
    fig_cpi.update_layout(height=300, yaxis_range=[0, 2.0])
    st.plotly_chart(fig_cpi, use_container_width=True)

    st.markdown('<div class="section-label">Transistor Count — Moore\'s Law</div>', unsafe_allow_html=True)

    df_tr = pd.DataFrame(TRANSISTOR_DATA)
    fig_tr = go.Figure()
    for arch, color in [("CISC","#3b82f6"),("RISC","#f97316")]:
        sub = df_tr[df_tr["arch"]==arch]
        fig_tr.add_trace(go.Scatter(x=sub["year"], y=sub["tr_m"], mode='lines+markers+text',
                                      name=arch, line=dict(color=color, width=2), marker=dict(size=7),
                                      text=sub["name"], textfont=dict(size=8), textposition='top right'))
    fig_tr.update_layout(**PLOT_BASE, height=320, yaxis_type='log',
                          title=dict(text="Transistor Count (millions) — log scale", font=dict(size=12,color='#cbd5e1')),
                          xaxis=dict(color='#475569', gridcolor='rgba(255,255,255,0.04)'),
                          yaxis=dict(color='#475569', gridcolor='rgba(255,255,255,0.04)'),
                          legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#94a3b8')))
    st.plotly_chart(fig_tr, use_container_width=True)

    st.markdown('<div class="section-label">Apple M3 Max vs Intel i9-13900K</div>', unsafe_allow_html=True)
    compare_df = pd.DataFrame({
        "Metric":["Transistors","TDP","Memory BW","SPECint Score","Score / Watt"],
        "Apple M3 Max  (RISC/ARM)":["92 B","92 W","400 GB/s","58.9","0.64"],
        "Intel i9-13900K  (CISC/x86)":["19.4 B","253 W","89 GB/s","57.6","0.23"],
    })
    st.dataframe(compare_df.set_index("Metric"), use_container_width=True)
    st.caption("Both chips score nearly identically in SPECint — but the M3 Max uses 63% less power and delivers 2.8× better efficiency. This is why ARM dominates mobile and is now challenging desktops.")