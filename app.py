"""
app.py — CogniSight™ Student Performance Intelligence Platform
=================================================================
Production-grade system: ML prediction · Cognitive assessment ·
AI-generated insights · Presentation mode · Night/Day theme
"""

import random
import time
import streamlit as st

from insights import (
    DEMO_PROFILE, cognitive_narrative, confidence_disclaimer,
    detect_weak_areas,
)
from logic_questions import LOGIC_QUESTIONS
from programming_questions import PROGRAMMING_QUESTIONS
from utils import (
    COLORS, MODEL_FEATURES,
    analytics_dashboard_charts, calc_critical_thinking, gauge_chart,
    generate_text_report, inspect_model, load_model, predict_performance,
    probability_bar, radar_chart, run_dummy_prediction, score_band,
    score_breakdown_bar, validate_feature_schema,
)
from visual_questions import VISUAL_QUESTIONS

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="CogniSight™ — Student Intelligence Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
_defaults = {
    "model":          None,
    "model_error":    "",
    "feature_order":  MODEL_FEATURES,
    "pred_label":     "",
    "pred_conf":      0.0,
    "pred_probs":     {},
    "input_data":     {},
    "student_name":   "Student",
    "logic_set":      [],
    "visual_set":     [],
    "prog_set":       [],
    "logic_score":    0.0,
    "visual_score":   0.0,
    "prog_score":     0.0,
    "night_mode":     False,
    "demo_mode":      False,
    "page":           "🏠  Dashboard",
    "analysis_done":  False,
}
for k, v in _defaults.items():
    st.session_state.setdefault(k, v)

# ══════════════════════════════════════════════════════════════════════════════
# MODEL BOOTSTRAP
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner=False)
def _load_cached_model():
    for path in ["final_random_forest_model.pkl",
                 "../final_random_forest_model.pkl",
                 "student-performance-app/final_random_forest_model.pkl"]:
        m, e = load_model(path)
        if m is not None:
            return m, None
    return None, "Model file not found. Ensure final_random_forest_model.pkl is present."

if st.session_state["model"] is None:
    mdl, err = _load_cached_model()
    st.session_state["model"]       = mdl
    st.session_state["model_error"] = err or ""
    if mdl is not None:
        ok, _, feats = validate_feature_schema(mdl)
        if ok:
            st.session_state["feature_order"] = feats

# ══════════════════════════════════════════════════════════════════════════════
# THEME PALETTE
# ══════════════════════════════════════════════════════════════════════════════
NM = st.session_state["night_mode"]
DM = st.session_state["demo_mode"]

if NM:
    P = dict(
        BG_PAGE="#0D0905",      BG_CARD="#1A1008",      BG_CARD2="#231508",
        BG_CARD3="#2C1A0A",     TEXT_MAIN="#F0E6D8",    TEXT_MUTED="#9C7B6B",
        TEXT_LABEL="#D4B896",   BORDER="#3D2415",        BORDER2="#2C1A0A",
        SB_BG="linear-gradient(180deg,#080503 0%,#130A04 55%,#1A1008 100%)",
        NAV_BG="#231508",       NAV_HOVER="#3D2415",    NAV_ACTIVE="#6B3A2A",
        NAV_TXT="#F5EBE0",      HDR_BG="linear-gradient(135deg,#0A0603 0%,#2C150A 65%,#3D1F14 100%)",
        INFO_BG="#0C1820",      INFO_BD="#2C6E8A",
        OK_BG="#0A1A11",        OK_BD="#2D7A4F",
        WARN_BG="#1A1203",      WARN_BD="#C4892A",
        ERR_BG="#160808",       ERR_BD="#B94040",
        QCARD="#1A1008",        TAB_BG="#1A1008",
        H="#F0E6D8",            H2_BD="#3D2415",
        EXP="#231508",          MET_BG="#1A1008",
        MET_VAL="#C4892A",      MET_LBL="#9C7B6B",
        ACNT="#231508",         DEMO_BG="#0D1B2A",
    )
else:
    P = dict(
        BG_PAGE="#FDFAF7",      BG_CARD="#FFFFFF",      BG_CARD2="#F9F4EF",
        BG_CARD3="#F5EDE0",     TEXT_MAIN="#2C1A0E",    TEXT_MUTED="#9C7B6B",
        TEXT_LABEL="#3D1F14",   BORDER="#E8D5C4",        BORDER2="#F0E0CC",
        SB_BG="linear-gradient(180deg,#3D1F14 0%,#5A2D18 45%,#6B3A2A 100%)",
        NAV_BG="rgba(255,255,255,0.08)", NAV_HOVER="rgba(255,255,255,0.16)",
        NAV_ACTIVE="#C4892A",   NAV_TXT="#FFFFFF",
        HDR_BG="linear-gradient(135deg,#3D1F14 0%,#6B3A2A 65%,#8B5E3C 100%)",
        INFO_BG="#EEF5FC",      INFO_BD="#2C6E8A",
        OK_BG="#E8F5EF",        OK_BD="#2D7A4F",
        WARN_BG="#FEF7E8",      WARN_BD="#C4892A",
        ERR_BG="#FDEAEA",       ERR_BD="#B94040",
        QCARD="#F9F4EF",        TAB_BG="#F5EDE0",
        H="#3D1F14",            H2_BD="#E8D5C4",
        EXP="#F5EDE0",          MET_BG="#FFFFFF",
        MET_VAL="#6B3A2A",      MET_LBL="#9C7B6B",
        ACNT="linear-gradient(135deg,#FDFAF7 0%,#F5EDE0 100%)",
        DEMO_BG="#EEF5FC",
    )

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Reset & Base ── */
.stApp {{
    background: {P["BG_PAGE"]} !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: {P["TEXT_MAIN"]} !important;
}}
*, p, span, div, li, td, th {{ color: {P["TEXT_MAIN"]}; box-sizing: border-box; }}
a {{ color: #C4892A !important; text-decoration: none; }}
h1,h2,h3,h4 {{ color: {P["H"]} !important; font-family: 'Inter', sans-serif !important; }}
h2 {{ border-bottom: 2px solid {P["H2_BD"]}; padding-bottom: 10px; margin-bottom: 16px; }}
.stMarkdown p, .stMarkdown li {{ color: {P["TEXT_MAIN"]} !important; line-height: 1.7; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {P["SB_BG"]} !important;
    border-right: 1px solid rgba(196,137,42,0.20);
}}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small {{
    color: #F5EBE0 !important;
}}
[data-testid="stSidebar"] [data-testid="stRadio"] {{ display: none !important; }}

/* ── Nav Boxes ── */
[data-testid="stSidebar"] .stButton > button {{
    background: {P["NAV_BG"]} !important;
    color: #E8D5C4 !important;
    border: 1px solid rgba(255,255,255,0.11) !important;
    border-radius: 9px !important;
    padding: 9px 13px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    margin-bottom: 4px !important;
    transition: all 0.18s ease !important;
    box-shadow: none !important;
    width: 100% !important;
    font-family: 'Inter', sans-serif !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: {P["NAV_HOVER"]} !important;
    border-color: rgba(196,137,42,0.40) !important;
    transform: translateX(3px) !important;
    color: #FFFFFF !important;
}}

/* ── Main Buttons ── */
.stButton > button {{
    background: linear-gradient(135deg,#6B3A2A,#8B5E3C) !important;
    color: #FDFAF7 !important; border: none !important;
    border-radius: 9px !important; font-weight: 600 !important;
    padding: 10px 22px !important;
    box-shadow: 0 3px 12px rgba(107,58,42,0.22) !important;
    transition: all 0.2s ease !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.01em !important;
}}
.stButton > button:hover {{ opacity: 0.88 !important; transform: translateY(-1px) !important; }}
.stFormSubmitButton > button {{
    background: linear-gradient(135deg,#6B3A2A,#C4892A) !important;
    color: #FFFFFF !important; border: none !important;
    border-radius: 9px !important; font-weight: 700 !important;
    font-size: 0.97rem !important; padding: 12px 28px !important;
    width: 100%; box-shadow: 0 4px 18px rgba(107,58,42,0.28) !important;
    letter-spacing: 0.02em !important;
}}

/* ── Input Labels ── */
.stSelectbox label, .stSlider label,
.stNumberInput label, .stTextInput label,
.stRadio label {{ color: {P["TEXT_LABEL"]} !important; font-weight: 500; font-size: 0.90rem; }}
.stSelectbox > div > div {{
    background: {P["BG_CARD"]} !important;
    border-color: {P["BORDER"]} !important;
    color: {P["TEXT_MAIN"]} !important;
}}
input, textarea {{ background: {P["BG_CARD"]} !important; color: {P["TEXT_MAIN"]} !important; }}
.stRadio > div > label > div > p {{ color: {P["TEXT_MAIN"]} !important; }}
.stRadio label {{ color: {P["TEXT_MAIN"]} !important; }}

/* ── Progress Bar ── */
.stProgress > div > div > div > div {{
    background: linear-gradient(90deg,#6B3A2A,#C4892A) !important;
    border-radius: 6px !important;
}}
.stProgress > div > div {{ background: {P["BORDER2"]} !important; border-radius: 6px !important; }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 5px; background: {P["TAB_BG"]}; padding: 6px 8px; border-radius: 10px;
    border: 1px solid {P["BORDER"]};
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent; border-radius: 7px;
    color: {P["TEXT_MAIN"]} !important; font-weight: 500; padding: 7px 16px;
    font-size: 0.88rem;
}}
.stTabs [aria-selected="true"] {{
    background: #6B3A2A !important; color: #FDFAF7 !important;
}}

/* ── Expander ── */
.streamlit-expanderHeader {{
    background: {P["EXP"]} !important; border: 1px solid {P["BORDER"]} !important;
    border-radius: 9px !important; color: {P["TEXT_MAIN"]} !important;
    font-weight: 600 !important;
}}
.streamlit-expanderContent {{
    background: {P["BG_CARD"]} !important;
    border: 1px solid {P["BORDER"]} !important;
    color: {P["TEXT_MAIN"]} !important;
}}
.streamlit-expanderContent * {{ color: {P["TEXT_MAIN"]} !important; }}

/* ── Caption ── */
.stCaption, .stCaption * {{ color: {P["TEXT_MUTED"]} !important; }}

/* ── Custom Component Classes ── */

/* Cards */
.card {{
    background: {P["BG_CARD"]}; border: 1px solid {P["BORDER"]};
    border-radius: 14px; padding: 20px 24px; margin-bottom: 14px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    transition: box-shadow 0.2s ease;
    color: {P["TEXT_MAIN"]} !important;
}}
.card * {{ color: {P["TEXT_MAIN"]} !important; }}
.card:hover {{ box-shadow: 0 5px 24px rgba(107,58,42,0.12); }}

.card-flat {{
    background: {P["BG_CARD2"]}; border: 1px solid {P["BORDER"]};
    border-radius: 12px; padding: 16px 20px; margin-bottom: 10px;
    color: {P["TEXT_MAIN"]} !important;
}}
.card-flat * {{ color: {P["TEXT_MAIN"]} !important; }}

.card-accent {{
    background: {P["ACNT"]}; border-left: 4px solid #6B3A2A;
    border-radius: 0 12px 12px 0; padding: 14px 18px; margin-bottom: 10px;
    color: {P["TEXT_MAIN"]} !important;
}}
.card-accent * {{ color: {P["TEXT_MAIN"]} !important; }}

/* Metric Cards */
.metric-card {{
    background: {P["MET_BG"]}; border: 1px solid {P["BORDER"]};
    border-radius: 12px; padding: 18px 14px; text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.metric-card:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(107,58,42,0.12); }}
.metric-card .mv {{ font-size: 2rem; font-weight: 700; color: {P["MET_VAL"]} !important; line-height: 1.1; }}
.metric-card .ml {{ font-size: 0.76rem; color: {P["MET_LBL"]} !important; margin-top: 5px;
                    text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; }}

/* KPI Banner Metric */
.kpi-card {{
    background: {P["BG_CARD"]}; border: 1px solid {P["BORDER"]};
    border-radius: 12px; padding: 16px 18px; position: relative;
    overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}}
.kpi-card::before {{
    content: ''; position: absolute; top: 0; left: 0;
    width: 4px; height: 100%; border-radius: 4px 0 0 4px;
}}
.kpi-card .kv {{ font-size: 1.8rem; font-weight: 700; color: {P["MET_VAL"]} !important; }}
.kpi-card .kl {{ font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em;
                 color: {P["TEXT_MUTED"]} !important; margin-top: 2px; font-weight: 600; }}
.kpi-card .ks {{ font-size: 0.82rem; color: {P["TEXT_MUTED"]} !important; margin-top: 6px; line-height: 1.4; }}

/* Insight Boxes */
.insight-box {{
    background: {P["BG_CARD"]}; border: 1px solid {P["BORDER"]};
    border-radius: 12px; padding: 20px 22px; margin-bottom: 14px;
    position: relative; overflow: hidden;
    color: {P["TEXT_MAIN"]} !important;
}}
.insight-box * {{ color: {P["TEXT_MAIN"]} !important; }}
.insight-box .ib-label {{
    font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.08em; color: {P["TEXT_MUTED"]} !important;
    margin-bottom: 8px;
}}
.insight-box .ib-text {{ font-size: 0.94rem; line-height: 1.72; color: {P["TEXT_MAIN"]} !important; }}

/* Recommendation Card */
.rec-card {{
    background: {P["BG_CARD2"]}; border: 1px solid {P["BORDER"]};
    border-radius: 12px; padding: 16px 18px; margin-bottom: 10px;
    display: flex; gap: 14px; align-items: flex-start;
    color: {P["TEXT_MAIN"]} !important;
}}
.rec-card * {{ color: {P["TEXT_MAIN"]} !important; }}
.rec-icon {{ font-size: 1.5rem; flex-shrink: 0; margin-top: 2px; }}
.rec-title {{ font-weight: 700; font-size: 0.94rem; margin-bottom: 4px; color: {P["H"]} !important; }}
.rec-body  {{ font-size: 0.87rem; line-height: 1.65; color: {P["TEXT_MAIN"]} !important; }}

/* Verdict Banner */
.verdict-banner {{
    border-radius: 16px; padding: 28px 32px; margin: 20px 0;
    border: 2px solid; position: relative; overflow: hidden;
    color: {P["TEXT_MAIN"]} !important;
}}
.verdict-banner * {{ color: {P["TEXT_MAIN"]} !important; }}
.verdict-title {{ font-size: 1.35rem; font-weight: 800; letter-spacing: 0.04em; margin-bottom: 10px; }}
.verdict-text  {{ font-size: 0.94rem; line-height: 1.75; }}
.verdict-tags  {{ margin-top: 16px; display: flex; gap: 8px; flex-wrap: wrap; }}
.v-tag {{
    padding: 4px 14px; border-radius: 20px; font-size: 0.78rem;
    font-weight: 600; border: 1px solid;
}}

/* Weak Area Item */
.weak-item {{
    background: {P["BG_CARD"]}; border: 1px solid {P["BORDER"]};
    border-radius: 11px; padding: 14px 18px; margin-bottom: 9px;
    border-left: 4px solid;
    color: {P["TEXT_MAIN"]} !important;
}}
.weak-item * {{ color: {P["TEXT_MAIN"]} !important; }}

/* Behaviour Item */
.beh-item {{
    background: {P["BG_CARD2"]}; border-radius: 10px;
    padding: 13px 17px; margin-bottom: 8px;
    border: 1px solid {P["BORDER"]};
    font-size: 0.91rem; line-height: 1.68;
    color: {P["TEXT_MAIN"]} !important;
}}

/* Section Header */
.section-hdr {{
    display: flex; align-items: center; gap: 10px;
    padding: 6px 0 12px 0; margin-bottom: 4px;
    border-bottom: 2px solid {P["H2_BD"]};
}}
.section-hdr .sh-icon {{ font-size: 1.3rem; }}
.section-hdr .sh-text {{
    font-size: 1.10rem; font-weight: 700; color: {P["H"]} !important;
    text-transform: uppercase; letter-spacing: 0.05em;
}}
.section-hdr .sh-sub {{
    font-size: 0.78rem; color: {P["TEXT_MUTED"]} !important;
    margin-left: 4px; font-weight: 400; text-transform: none; letter-spacing: 0;
}}

/* Divider */
.div-line {{
    height: 1px; background: linear-gradient(90deg,#6B3A2A,rgba(196,137,42,0.4),transparent);
    border: none; margin: 20px 0;
}}

/* Demo Banner */
.demo-banner {{
    background: {P["DEMO_BG"]}; border: 2px solid #2C6E8A;
    border-radius: 12px; padding: 14px 20px; margin-bottom: 20px;
    display: flex; align-items: center; gap: 14px;
    color: {P["TEXT_MAIN"]} !important;
}}
.demo-banner * {{ color: {P["TEXT_MAIN"]} !important; }}

/* Page Banner */
.page-banner {{
    background: {P["HDR_BG"]}; border-radius: 16px;
    padding: 24px 30px 20px; margin-bottom: 24px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.20);
    border: 1px solid rgba(196,137,42,0.25);
}}
.page-banner h1 {{ color: #F5EBE0 !important; margin: 0; font-size: 1.75rem; font-weight: 700; }}
.page-banner p  {{ color: #C4A882 !important; margin: 6px 0 0; font-size: 0.92rem; }}

/* Question Card */
.q-card {{
    background: {P["QCARD"]}; border: 1px solid {P["BORDER"]};
    border-radius: 11px; padding: 14px 18px; margin-bottom: 8px;
    border-left: 3px solid #6B3A2A; color: {P["TEXT_MAIN"]} !important;
}}
.q-card * {{ color: {P["TEXT_MAIN"]} !important; }}
.q-cat {{ font-size: 0.74rem; color: {P["TEXT_MUTED"]} !important;
          text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 5px; font-weight: 600; }}

/* Score Row */
.score-row {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 8px 13px; border-radius: 9px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.11); margin-bottom: 5px;
}}
.score-row .sr-lbl {{ color: #D4C4B4 !important; font-size: 0.86rem; }}
.score-row .sr-val {{ font-weight: 700; font-size: 0.92rem; }}

/* Nav section label */
.nav-sec {{ font-size: 0.68rem; color: rgba(232,213,196,0.50) !important;
            text-transform: uppercase; letter-spacing: 0.10em;
            padding: 10px 4px 4px; font-weight: 600; }}

/* Info / success / warn boxes */
.ib {{ padding: 12px 16px; border-radius: 0 10px 10px 0; margin: 10px 0;
       border-left: 4px solid; color: {P["TEXT_MAIN"]} !important; }}
.ib * {{ color: {P["TEXT_MAIN"]} !important; }}
.ib-info {{ background:{P["INFO_BG"]}; border-color:{P["INFO_BD"]}; }}
.ib-ok   {{ background:{P["OK_BG"]};   border-color:{P["OK_BD"]}; }}
.ib-warn {{ background:{P["WARN_BG"]}; border-color:{P["WARN_BD"]}; }}
.ib-err  {{ background:{P["ERR_BG"]};  border-color:{P["ERR_BD"]}; }}

/* Confidence pill */
.conf-pill {{
    display: inline-block; padding: 4px 14px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 700; border: 1px solid;
    margin-left: 8px;
}}

/* Stat number */
.big-stat {{
    font-size: 3rem; font-weight: 800; line-height: 1;
    color: {P["MET_VAL"]} !important;
    font-family: 'Inter', sans-serif;
}}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
NAV_PAGES = [
    ("🏠", "Dashboard"),
    ("👤", "Student Assessment"),
    ("🧠", "Cognitive Tests"),
    ("🔍", "AI Analysis Report"),
    ("🎯", "Critical Thinking"),
    ("📈", "Analytics Dashboard"),
    ("✅", "Model Validation"),
    ("📄", "Export Report"),
]

with st.sidebar:
    # Brand
    st.markdown(
        f'<div style="padding:6px 2px 4px">'
        f'<div style="font-size:1.4rem;font-weight:800;color:#F5EBE0;letter-spacing:-0.01em">'
        f'CogniSight™</div>'
        f'<div style="font-size:0.72rem;color:rgba(232,213,196,0.55);'
        f'letter-spacing:0.08em;text-transform:uppercase">Student Intelligence Platform</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr style="border-color:rgba(196,137,42,0.22);margin:10px 0">', unsafe_allow_html=True)

    # Night mode + Demo mode toggles
    c1, c2 = st.columns(2)
    with c1:
        nm_label = "☀️ Day" if NM else "🌙 Night"
        if st.button(nm_label, key="btn_night", use_container_width=True):
            st.session_state["night_mode"] = not NM
            st.rerun()
    with c2:
        dm_label = "🎬 Exit Demo" if DM else "🎬 Demo"
        if st.button(dm_label, key="btn_demo", use_container_width=True):
            if not DM:
                _load_demo_data()
            else:
                st.session_state["demo_mode"] = False
            st.rerun()

    st.markdown('<hr style="border-color:rgba(196,137,42,0.22);margin:10px 0">', unsafe_allow_html=True)
    st.markdown('<div class="nav-sec">Navigation</div>', unsafe_allow_html=True)

    for icon, label in NAV_PAGES:
        is_active = st.session_state["page"] == label
        btn_style = "" if not is_active else "active"
        key = f"nav_{label}"
        if st.button(f"{icon}  {label}", key=key, use_container_width=True):
            st.session_state["page"] = label
            st.rerun()
        # Inject active style after rendering (post-render CSS trick)
        if is_active:
            st.markdown(
                f'<style>[data-testid="stSidebar"] div[data-testid="element-container"]:has(button[kind="secondary"]:last-of-type)'
                f' button {{ background: {P["NAV_ACTIVE"]} !important; color: {P["NAV_TXT"]} !important;'
                f' border-color: rgba(255,255,255,0.30) !important; font-weight: 700 !important; }}</style>',
                unsafe_allow_html=True,
            )

    st.markdown('<hr style="border-color:rgba(196,137,42,0.22);margin:12px 0">', unsafe_allow_html=True)

    # Live scores
    st.markdown('<div class="nav-sec">Test Scores</div>', unsafe_allow_html=True)
    for lbl, sc in [("🧠 Logic", st.session_state["logic_score"]),
                    ("👁️ Visual", st.session_state["visual_score"]),
                    ("💻 Prog", st.session_state["prog_score"])]:
        sc_color = "#2D7A4F" if sc >= 65 else "#C4892A" if sc >= 45 else "#9C7B6B"
        st.markdown(
            f'<div class="score-row">'
            f'<span class="sr-lbl">{lbl}</span>'
            f'<span class="sr-val" style="color:{sc_color}">{sc:.0f}%</span>'
            f'</div>', unsafe_allow_html=True,
        )

    if st.session_state["pred_label"]:
        st.markdown('<hr style="border-color:rgba(196,137,42,0.22);margin:10px 0">', unsafe_allow_html=True)
        st.markdown('<div class="nav-sec">ML Prediction</div>', unsafe_allow_html=True)
        lbl = st.session_state["pred_label"]
        pc  = {"High":"#2D7A4F","Medium":"#C4892A","Low":"#B94040"}.get(lbl,"#C4892A")
        st.markdown(
            f'<div style="padding:10px 13px;border-radius:9px;background:rgba(255,255,255,0.07);'
            f'border:1px solid rgba(255,255,255,0.13);">'
            f'<div style="font-size:1.05rem;font-weight:700;color:{pc}">{lbl} Performer</div>'
            f'<div style="font-size:0.78rem;color:rgba(232,213,196,0.60);margin-top:3px">'
            f'Confidence: {st.session_state["pred_conf"]*100:.1f}%</div>'
            f'</div>', unsafe_allow_html=True,
        )

    st.markdown('<hr style="border-color:rgba(196,137,42,0.22);margin:10px 0">', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-size:0.70rem;color:rgba(232,213,196,0.40);text-align:center;line-height:1.7">'
        f'CogniSight™ v2.0<br>Powered by Random Forest ML<br>Sukkur IBA University</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# DEMO MODE LOADER (must be defined before sidebar call)
# ══════════════════════════════════════════════════════════════════════════════
def _load_demo_data():
    """Instantly load the DEMO_PROFILE into session state and run prediction."""
    dp = DEMO_PROFILE
    st.session_state["student_name"] = dp["name"]
    st.session_state["logic_score"]  = dp["logic_score"]
    st.session_state["visual_score"] = dp["visual_score"]
    st.session_state["prog_score"]   = dp["prog_score"]
    st.session_state["demo_mode"]    = True

    payload = {k: dp[k] for k in MODEL_FEATURES}
    payload["Gender"]            = dp.get("Gender","Female")
    payload["Diet_Type"]         = dp.get("Diet_Type","Vegetarian")
    payload["Exercise_Frequency"]= dp.get("Exercise_Frequency","Medium")

    model = st.session_state.get("model")
    if model:
        label, conf, probs, _ = predict_performance(model, payload)
        st.session_state.update({
            "pred_label":    label,
            "pred_conf":     conf,
            "pred_probs":    probs,
            "input_data":    payload,
            "analysis_done": True,
        })
    st.session_state["page"] = "AI Analysis Report"


# ══════════════════════════════════════════════════════════════════════════════
# UTILITY COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════
def section_header(icon, title, subtitle=""):
    sub_html = f'<span class="sh-sub">— {subtitle}</span>' if subtitle else ""
    st.markdown(
        f'<div class="section-hdr">'
        f'<span class="sh-icon">{icon}</span>'
        f'<span class="sh-text">{title}</span>{sub_html}'
        f'</div>', unsafe_allow_html=True,
    )

def metric_card(col, value, label, sub=None):
    sub_html = f'<div style="font-size:0.76rem;color:{P["TEXT_MUTED"]};margin-top:5px">{sub}</div>' if sub else ""
    col.markdown(
        f'<div class="metric-card">'
        f'<div class="mv">{value}</div>'
        f'<div class="ml">{label}</div>{sub_html}</div>',
        unsafe_allow_html=True,
    )

def kpi_row(items):
    """items: list of (value, label, sub, accent_color)"""
    cols = st.columns(len(items))
    for col, (val, lbl, sub, color) in zip(cols, items):
        col.markdown(
            f'<div class="kpi-card" style="border-left:4px solid {color}">'
            f'<div class="kv" style="color:{color}!important">{val}</div>'
            f'<div class="kl">{lbl}</div>'
            f'<div class="ks">{sub}</div>'
            f'</div>', unsafe_allow_html=True,
        )

def ib(kind, content):
    st.markdown(f'<div class="ib ib-{kind}">{content}</div>', unsafe_allow_html=True)

def divider():
    st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)

def demo_banner():
    if DM:
        st.markdown(
            f'<div class="demo-banner">'
            f'<span style="font-size:1.6rem">🎬</span>'
            f'<div><b>Presentation Mode Active</b> — Showing preloaded high-quality profile: '
            f'<b>{DEMO_PROFILE["name"]}</b>. All outputs are computed live from the ML model.</div>'
            f'</div>', unsafe_allow_html=True,
        )

def quiz_block(title, question_pool, key_prefix, gauge_color, total=10):
    if not st.session_state[f"{key_prefix}_set"]:
        st.session_state[f"{key_prefix}_set"] = random.sample(
            question_pool, min(total, len(question_pool))
        )
    questions = st.session_state[f"{key_prefix}_set"]

    with st.form(f"{key_prefix}_form"):
        answers = {}
        for i, q in enumerate(questions, 1):
            st.markdown(
                f'<div class="q-card">'
                f'<div class="q-cat">{q["category"]}</div>'
                f'<span style="font-weight:600;font-size:0.93rem">Q{i}. {q["question"]}</span>'
                f'</div>', unsafe_allow_html=True,
            )
            answers[q["id"]] = st.radio(
                f"A{q['id']}", q["options"],
                key=f"{key_prefix}_{q['id']}",
                label_visibility="collapsed",
                horizontal=True,
            )
            st.write("")
        submitted = st.form_submit_button(f"📝  Submit {title}", use_container_width=True)

    if submitted:
        correct = sum(1 for q in questions if answers.get(q["id"]) == q["answer"])
        score   = round(100 * correct / len(questions), 1)
        st.session_state[f"{key_prefix}_score"] = score
        band    = score_band(score)

        c1, c2, c3 = st.columns(3)
        metric_card(c1, f"{score}%",        "Your Score")
        metric_card(c2, f"{correct}/{len(questions)}", "Correct")
        metric_card(c3, band,               "Band")

        st.plotly_chart(gauge_chart(score / 100, f"{title} Score", gauge_color),
                        use_container_width=True)

        with st.expander("📖  Detailed Answer Review", expanded=False):
            for q in questions:
                given = answers.get(q["id"])
                ok    = given == q["answer"]
                bg    = P["OK_BG"] if ok else P["ERR_BG"]
                bd    = P["OK_BD"] if ok else P["ERR_BD"]
                st.markdown(
                    f'<div style="background:{bg};border-left:3px solid {bd};'
                    f'padding:11px 15px;border-radius:0 9px 9px 0;margin-bottom:8px;">'
                    f'<span style="font-weight:700">{"✅" if ok else "❌"} Q{q["id"]}.</span> '
                    f'<span>{q["question"]}</span><br>'
                    f'<span style="color:{P["TEXT_MUTED"]};font-size:0.84rem">'
                    f'Your answer: <b style="color:{P["TEXT_MAIN"]}">{given}</b> &nbsp;|&nbsp; '
                    f'Correct: <b style="color:{P["OK_BD"]}">{q["answer"]}</b></span><br>'
                    f'<span style="font-size:0.87rem">💡 {q["explanation"]}</span>'
                    f'</div>', unsafe_allow_html=True,
                )

        if st.button(f"🔄  Retake {title}", key=f"retake_{key_prefix}"):
            st.session_state[f"{key_prefix}_set"] = []
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE ROUTER
# ══════════════════════════════════════════════════════════════════════════════
page = st.session_state["page"]

# ── DASHBOARD ────────────────────────────────────────────────────────────────
if page == "Dashboard":
    demo_banner()

    # Hero
    st.markdown(
        f'<div class="page-banner">'
        f'<h1>🎓 CogniSight™ Intelligence Platform</h1>'
        f'<p>AI-powered cognitive assessment · Behavioural analytics · Academic performance prediction</p>'
        f'</div>', unsafe_allow_html=True,
    )

    # Quick stats row
    has_pred   = bool(st.session_state.get("pred_label"))
    has_logic  = st.session_state["logic_score"] > 0
    has_visual = st.session_state["visual_score"] > 0
    has_prog   = st.session_state["prog_score"] > 0
    done_count = sum([has_pred, has_logic, has_visual, has_prog])

    kpi_row([
        (f"{done_count}/4",     "Sections Complete",  "Across assessment modules",  "#6B3A2A"),
        (f"{st.session_state['logic_score']:.0f}%",  "Logic Score",
         score_band(st.session_state["logic_score"]), "#2C6E8A"),
        (f"{st.session_state['prog_score']:.0f}%",   "Programming Score",
         score_band(st.session_state["prog_score"]),  "#2D7A4F"),
        (st.session_state["pred_label"] or "—",      "ML Prediction",
         f"Confidence: {st.session_state['pred_conf']*100:.0f}%", "#C4892A"),
    ])

    divider()

    # Module cards
    st.markdown(f'<h2 style="color:{P["H"]}">Assessment Modules</h2>', unsafe_allow_html=True)

    modules = [
        ("👤", "Student Assessment", "Enter student profile data and run ML performance prediction.",
         "Start here →", "#6B3A2A", has_pred),
        ("🧠", "Cognitive Tests",    "Three adaptive tests: logical reasoning, visual intelligence, programming logic.",
         "Begin tests →", "#2C6E8A", all([has_logic, has_visual, has_prog])),
        ("🔍", "AI Analysis Report", "The platform's centrepiece — 7-section AI-generated intelligence report.",
         "View report →", "#2D7A4F", has_pred or all([has_logic, has_visual, has_prog])),
        ("🎬", "Presentation Mode",  "One-click demo with preloaded high-quality profile. Ready to impress.",
         "Launch demo →", "#C4892A", DM),
    ]

    col1, col2 = st.columns(2)
    for i, (icon, name, desc, cta, color, done) in enumerate(modules):
        col = col1 if i % 2 == 0 else col2
        status = f'<span style="color:{P["OK_BD"]};font-size:0.78rem;font-weight:600">● Complete</span>' if done else \
                 f'<span style="color:{P["TEXT_MUTED"]};font-size:0.78rem">○ Pending</span>'
        col.markdown(
            f'<div class="card" style="border-left:4px solid {color}">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">'
            f'<span style="font-size:1.6rem">{icon}</span>{status}</div>'
            f'<div style="font-size:1.0rem;font-weight:700;color:{P["H"]};margin-bottom:6px">{name}</div>'
            f'<div style="font-size:0.87rem;color:{P["TEXT_MUTED"]};line-height:1.6;margin-bottom:12px">{desc}</div>'
            f'<div style="font-size:0.83rem;font-weight:700;color:{color}">{cta}</div>'
            f'</div>', unsafe_allow_html=True,
        )

    divider()

    # How it works
    section_header("⚙️", "How It Works", "Platform Overview")
    steps = [
        ("1", "Enter Profile", "Input student academic, lifestyle, and cognitive data"),
        ("2", "Run ML Model", "Random Forest classifier predicts performance class"),
        ("3", "Complete Tests", "Adaptive cognitive assessments across 3 domains"),
        ("4", "Read AI Report", "7-section intelligent analysis with personalised insights"),
    ]
    cols = st.columns(4)
    for col, (num, title, desc) in zip(cols, steps):
        col.markdown(
            f'<div style="text-align:center;padding:16px 10px">'
            f'<div style="width:40px;height:40px;border-radius:50%;'
            f'background:linear-gradient(135deg,#6B3A2A,#C4892A);'
            f'display:flex;align-items:center;justify-content:center;'
            f'margin:0 auto 10px;font-weight:800;color:#FFFFFF;font-size:1rem">{num}</div>'
            f'<div style="font-weight:700;color:{P["H"]};font-size:0.90rem;margin-bottom:5px">{title}</div>'
            f'<div style="font-size:0.82rem;color:{P["TEXT_MUTED"]};line-height:1.5">{desc}</div>'
            f'</div>', unsafe_allow_html=True,
        )


# ── STUDENT ASSESSMENT ────────────────────────────────────────────────────────
elif page == "Student Assessment":
    demo_banner()
    st.markdown(
        f'<div class="page-banner"><h1>👤 Student Assessment</h1>'
        f'<p>Complete student profile → ML-powered academic performance prediction with confidence scoring</p></div>',
        unsafe_allow_html=True,
    )
    if st.session_state["model"] is None:
        ib("err", f"❌ Model not loaded: {st.session_state['model_error']}")
        st.stop()

    with st.form("predict_form"):
        c1, c2 = st.columns([1, 2])
        with c1:
            student_name = st.text_input("Student Name", value=st.session_state.get("student_name",""))
        with c2:
            pass

        st.markdown(f'<h3 style="color:{P["H"]}">👤 Personal & Lifestyle</h3>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        age      = c1.number_input("Age", 15, 60, 21)
        gender   = c2.selectbox("Gender", ["Female", "Male", "Other"])
        diet     = c3.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
        exercise = c4.selectbox("Exercise", ["Medium", "High", "Low"])

        c5, c6, c7 = st.columns(3)
        sleep   = c5.slider("Sleep (hrs/night)", 3.0, 12.0, 7.0, 0.5)
        stress  = c6.slider("Stress Level (1–10)", 1, 10, 5)
        screen  = c7.slider("Screen Time (hrs/day)", 0.0, 16.0, 4.0, 0.5)

        divider()
        st.markdown(f'<h3 style="color:{P["H"]}">📚 Academic Profile</h3>', unsafe_allow_html=True)
        c8, c9, c10 = st.columns(3)
        study      = c8.slider("Study Hours/Day", 0.0, 14.0, 5.0, 0.25)
        attendance = c9.slider("Attendance Rate (0–1)", 0.0, 1.0, 0.88, 0.01)
        gpa        = c10.slider("Previous GPA (0–4)", 0.0, 4.0, 3.2, 0.1)

        divider()
        st.markdown(f'<h3 style="color:{P["H"]}">🧠 Cognitive Measurements</h3>', unsafe_allow_html=True)
        c11, c12, c13 = st.columns(3)
        reaction   = c11.number_input("Reaction Time (ms)", 150, 900, 300,
                                       help="Lower = faster. Average: 250–350ms")
        memory     = c12.slider("Memory Test Score (0–100)", 0, 100, 78)
        cognition  = c13.slider("Cognitive Score (0–100)", 0, 100, 80)

        c14, c15, c16 = st.columns(3)
        logic_ts  = c14.slider("Logic Test Score (0–100)", 0, 100, 72)
        logic_er  = c15.slider("Logic Error Rate (0–1)", 0.0, 1.0, 0.18, 0.01,
                                help="0 = no errors. 1 = all incorrect.")
        caffeine  = c16.number_input("Caffeine Intake (mg/day)", 0, 600, 90)

        submitted = st.form_submit_button("🚀  Run ML Prediction", use_container_width=True)

    if submitted:
        st.session_state["student_name"] = student_name or "Student"
        payload = {
            "Age": age, "Sleep_Duration": sleep, "Stress_Level": stress,
            "Daily_Screen_Time": screen, "Caffeine_Intake": caffeine,
            "Reaction_Time": reaction, "Memory_Test_Score": memory,
            "Cognitive_Score": cognition, "Study_Hours_Per_Day": study,
            "Attendance_Rate": attendance, "Previous_GPA": gpa,
            "Logic_Test_Score": logic_ts, "Logic_Error_Rate": logic_er,
            "Gender": gender, "Diet_Type": diet, "Exercise_Frequency": exercise,
        }

        with st.spinner("Running ML prediction pipeline…"):
            time.sleep(0.4)
            label, conf, probs, errors = predict_performance(st.session_state["model"], payload)

        if errors:
            for e in errors:
                ib("err", f"❌ {e}")
        else:
            st.session_state.update({
                "pred_label": label, "pred_conf": conf,
                "pred_probs": probs, "input_data": payload, "analysis_done": True,
            })

            divider()
            # Confidence fallback
            cd = confidence_disclaimer(conf)
            ib("warn" if cd["level"] == "Low" else "info" if cd["level"] == "Moderate" else "ok",
               f'<b>Model Confidence: <span style="color:{cd["color"]}">{cd["level"]}</span> '
               f'({conf*100:.1f}%)</b> — {cd["msg"]}')

            divider()
            st.markdown(f'<h2 style="color:{P["H"]}">🎯 Prediction Result</h2>', unsafe_allow_html=True)

            bc    = label.lower()
            badge_colors = {"high": P["OK_BD"], "medium": P["WARN_BD"], "low": P["ERR_BD"]}
            badge_bgs    = {"high": P["OK_BG"],  "medium": P["WARN_BG"], "low": P["ERR_BG"]}
            bc_col = badge_colors.get(bc, P["WARN_BD"])
            bc_bg  = badge_bgs.get(bc, P["WARN_BG"])

            interp = {
                "High":   "This student's profile aligns with characteristics of high academic achievers in the training dataset. Strong study habits, adequate sleep, and above-average cognitive scores drive this prediction.",
                "Medium": "The student profile presents a mixed signal — some indicators point toward strong performance while others suggest inconsistencies in study habits or cognitive readiness. Targeted support can shift this classification upward.",
                "Low":    "Several risk factors are present in this profile — insufficient study time, elevated stress, and below-average cognitive scores are the primary drivers. Structured intervention is strongly recommended.",
            }
            col1, col2 = st.columns([1.1, 1])
            with col1:
                st.markdown(
                    f'<div class="card" style="padding:28px;text-align:center;">'
                    f'<div style="font-size:0.78rem;text-transform:uppercase;letter-spacing:0.08em;'
                    f'color:{P["TEXT_MUTED"]};margin-bottom:12px">PREDICTED PERFORMANCE CLASS</div>'
                    f'<div style="display:inline-block;background:{bc_bg};border:2px solid {bc_col};'
                    f'color:{bc_col}!important;padding:8px 28px;border-radius:25px;'
                    f'font-size:1.35rem;font-weight:800;margin-bottom:16px">{label} Performer</div>'
                    f'<div class="big-stat" style="color:{bc_col}!important">{conf*100:.1f}%</div>'
                    f'<div style="font-size:0.80rem;color:{P["TEXT_MUTED"]};margin:6px 0 16px">Model Confidence Score</div>'
                    f'<div style="font-size:0.88rem;line-height:1.7;color:{P["TEXT_MAIN"]};text-align:left;'
                    f'background:{P["BG_CARD2"]};padding:14px;border-radius:10px">{interp.get(label,"")}</div>'
                    f'</div>', unsafe_allow_html=True,
                )
            with col2:
                st.plotly_chart(probability_bar(probs), use_container_width=True)

            ib("info",
               f'✅ Prediction complete. Navigate to <b>🔍 AI Analysis Report</b> '
               f'for the full 7-section cognitive intelligence report.')


# ── COGNITIVE TESTS ───────────────────────────────────────────────────────────
elif page == "Cognitive Tests":
    demo_banner()
    st.markdown(
        f'<div class="page-banner"><h1>🧠 Cognitive Assessment Suite</h1>'
        f'<p>Three adaptive tests measuring logical reasoning · visual intelligence · programming logic</p></div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs([
        "🧠  Logical Reasoning",
        "👁️  Visual Intelligence",
        "💻  Programming Logic",
    ])

    with tab1:
        st.markdown(
            f'<div class="ib ib-info">📌 <b>10 questions</b> across pattern recognition, '
            f'analytical reasoning, logical deduction, and quantitative reasoning.</div>',
            unsafe_allow_html=True,
        )
        if st.session_state["logic_score"] > 0:
            ib("ok", f'Last score: <b>{st.session_state["logic_score"]:.1f}%</b>'
                     f' — {score_band(st.session_state["logic_score"])}')
        quiz_block("Logical Reasoning", LOGIC_QUESTIONS, "logic", COLORS["Primary"], 10)

    with tab2:
        st.markdown(
            f'<div class="ib ib-info">📌 <b>10 questions</b> testing shape identification, '
            f'cube counting, spatial rotation, and mirror image recognition.</div>',
            unsafe_allow_html=True,
        )
        if st.session_state["visual_score"] > 0:
            ib("ok", f'Last score: <b>{st.session_state["visual_score"]:.1f}%</b>'
                     f' — {score_band(st.session_state["visual_score"])}')
        quiz_block("Visual Intelligence", VISUAL_QUESTIONS, "visual", COLORS["Info"], 10)

    with tab3:
        st.markdown(
            f'<div class="ib ib-info">📌 <b>10 questions</b> on Python code tracing — '
            f'loop output, conditional logic, arithmetic, data structures, and functions.</div>',
            unsafe_allow_html=True,
        )
        if st.session_state["prog_score"] > 0:
            ib("ok", f'Last score: <b>{st.session_state["prog_score"]:.1f}%</b>'
                     f' — {score_band(st.session_state["prog_score"])}')
        quiz_block("Programming Logic", PROGRAMMING_QUESTIONS, "prog", COLORS["Secondary"], 10)


# ── AI ANALYSIS REPORT ────────────────────────────────────────────────────────
elif page == "AI Analysis Report":
    demo_banner()
    st.markdown(
        f'<div class="page-banner"><h1>🔍 AI Analysis Report</h1>'
        f'<p>Multi-dimensional cognitive intelligence report — powered by ML prediction + behavioural analytics</p></div>',
        unsafe_allow_html=True,
    )

    # Guard
    has_pred  = bool(st.session_state.get("pred_label"))
    has_tests = (st.session_state["logic_score"] > 0 or
                 st.session_state["visual_score"] > 0 or
                 st.session_state["prog_score"] > 0)

    if not has_pred and not has_tests:
        ib("warn",
           "⚠️ No assessment data found. Please complete <b>Student Assessment</b> and "
           "<b>Cognitive Tests</b> first — or click <b>🎬 Demo</b> in the sidebar for an instant preview.")
        st.stop()

    pred_label   = st.session_state.get("pred_label", "Medium") or "Medium"
    pred_conf    = st.session_state.get("pred_conf", 0.0)
    pred_probs   = st.session_state.get("pred_probs", {})
    input_data   = st.session_state.get("input_data", {})
    logic_score  = st.session_state["logic_score"]
    visual_score = st.session_state["visual_score"]
    prog_score   = st.session_state["prog_score"]
    student_name = st.session_state.get("student_name", "Student")

    # Compute critical thinking + insights
    with st.spinner("Generating AI analysis…"):
        time.sleep(0.3)
        ct = calc_critical_thinking(pred_label, pred_conf, logic_score,
                                     visual_score, prog_score, input_data)
        ins = cognitive_narrative(pred_label, pred_conf, ct, logic_score,
                                   visual_score, prog_score, input_data)
        weak_areas = detect_weak_areas(input_data, logic_score, visual_score, prog_score)
        cd = confidence_disclaimer(pred_conf)

    # ── SECTION 1: Student Profile Summary ────────────────────────────────────
    divider()
    section_header("👤", "Student Profile Summary")

    c1, c2 = st.columns([1.6, 1])
    with c1:
        bc_col = {"High": P["OK_BD"], "Medium": P["WARN_BD"], "Low": P["ERR_BD"]}.get(pred_label, P["WARN_BD"])
        st.markdown(
            f'<div class="card" style="border-left:5px solid {bc_col}">'
            f'<div style="display:flex;align-items:center;gap:16px;margin-bottom:16px">'
            f'<div style="width:54px;height:54px;border-radius:50%;'
            f'background:linear-gradient(135deg,#6B3A2A,#C4892A);'
            f'display:flex;align-items:center;justify-content:center;'
            f'font-size:1.5rem;color:#FFFFFF;font-weight:800;flex-shrink:0">'
            f'{student_name[0].upper()}</div>'
            f'<div><div style="font-size:1.2rem;font-weight:700;color:{P["H"]}">{student_name}</div>'
            f'<div style="font-size:0.82rem;color:{P["TEXT_MUTED"]}">Student Assessment Profile</div></div>'
            f'</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">'
            + "".join([
                f'<div style="background:{P["BG_CARD2"]};border-radius:8px;padding:10px 13px;">'
                f'<div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.05em;'
                f'color:{P["TEXT_MUTED"]}">{k}</div>'
                f'<div style="font-weight:700;color:{P["H"]};font-size:0.92rem;margin-top:3px">{v}</div>'
                f'</div>'
                for k, v in [
                    ("Age", f'{input_data.get("Age","—")} years'),
                    ("GPA", f'{input_data.get("Previous_GPA","—")} / 4.0'),
                    ("Attendance", f'{float(input_data.get("Attendance_Rate",0.85))*100:.0f}%'),
                    ("Study / Day", f'{input_data.get("Study_Hours_Per_Day","—")} hrs'),
                    ("Sleep / Night", f'{input_data.get("Sleep_Duration","—")} hrs'),
                    ("Stress Level", f'{input_data.get("Stress_Level","—")} / 10'),
                ]
            ]) + '</div></div>', unsafe_allow_html=True,
        )

    with c2:
        perf_badge_colors = {"High": P["OK_BD"], "Medium": P["WARN_BD"], "Low": P["ERR_BD"]}
        perf_badge_bgs    = {"High": P["OK_BG"],  "Medium": P["WARN_BG"], "Low": P["ERR_BG"]}
        bc = pred_label.lower()
        st.markdown(
            f'<div class="card" style="text-align:center;padding:22px 18px">'
            f'<div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;'
            f'color:{P["TEXT_MUTED"]};margin-bottom:10px">ML Predicted Class</div>'
            f'<div style="background:{perf_badge_bgs.get(pred_label,P["WARN_BG"])};'
            f'border:2px solid {perf_badge_colors.get(pred_label,P["WARN_BD"])};'
            f'color:{perf_badge_colors.get(pred_label,P["WARN_BD"])}!important;'
            f'padding:7px 20px;border-radius:25px;font-size:1.15rem;font-weight:800;'
            f'display:inline-block;margin-bottom:16px">{pred_label} Performer</div>'
            f'<div class="big-stat" style="color:{perf_badge_colors.get(pred_label,P["WARN_BD"])}!important">'
            f'{pred_conf*100:.1f}%</div>'
            f'<div style="font-size:0.78rem;color:{P["TEXT_MUTED"]};margin:4px 0 14px">Confidence Score</div>'
            f'<div style="background:{perf_badge_bgs.get(cd["level"],"")};'
            f'border:1px solid {cd["color"]};border-radius:8px;padding:8px 12px;">'
            f'<span style="font-size:0.78rem;font-weight:700;color:{cd["color"]}!important">'
            f'Confidence: {cd["level"]}</span><br>'
            f'<span style="font-size:0.78rem;color:{P["TEXT_MAIN"]}">{cd["msg"][:90]}…</span>'
            f'</div></div>', unsafe_allow_html=True,
        )

    # ── SECTION 2: Cognitive & Logic Scores ───────────────────────────────────
    divider()
    section_header("📊", "Cognitive & Logic Scores", "Visual performance overview")

    kpi_row([
        (f"{ct['Overall']}%",                    "Critical Thinking",     score_band(ct["Overall"]),       "#6B3A2A"),
        (f"{logic_score:.0f}%",                  "Logical Reasoning",     score_band(logic_score),          "#2C6E8A"),
        (f"{visual_score:.0f}%",                 "Visual Intelligence",   score_band(visual_score),         "#8B5E3C"),
        (f"{prog_score:.0f}%",                   "Programming Logic",     score_band(prog_score),           "#2D7A4F"),
        (f"{ct.get('Programming_Capability',0)}%","Prog Capability",      "Composite Index",                "#C4892A"),
        (f"{ct.get('Innovation_Potential',0)}%", "Innovation Potential",  "Creative-Adaptive Index",        "#7B4BA0"),
    ])

    col1, col2 = st.columns(2)
    col1.plotly_chart(radar_chart(ct), use_container_width=True)
    col2.plotly_chart(score_breakdown_bar(ct), use_container_width=True)

    # ── SECTION 3: Cognitive Analysis ─────────────────────────────────────────
    divider()
    section_header("🧬", "Cognitive Analysis", "AI-generated profile interpretation")

    st.markdown(
        f'<div class="insight-box">'
        f'<div class="ib-label">Overall Cognitive Summary</div>'
        f'<div class="ib-text">{ins["cognitive_summary"]}</div>'
        f'</div>', unsafe_allow_html=True,
    )

    # Confidence gauge
    c1, c2, c3 = st.columns(3)
    c1.plotly_chart(gauge_chart(ct["Overall"]/100, "Critical Thinking", "#6B3A2A"), use_container_width=True)
    c2.plotly_chart(gauge_chart(ct.get("Programming_Capability",0)/100, "Prog Capability", "#C4892A"), use_container_width=True)
    c3.plotly_chart(gauge_chart(ct.get("Innovation_Potential",0)/100, "Innovation", "#2D7A4F"), use_container_width=True)

    # ── SECTION 4: Learning Behaviour Insights ────────────────────────────────
    divider()
    section_header("📖", "Learning Behaviour Insights", "Lifestyle & academic habit analysis")

    col1, col2 = st.columns(2)
    for i, beh in enumerate(ins["behaviours"]):
        col = col1 if i % 2 == 0 else col2
        col.markdown(
            f'<div class="beh-item">{beh}</div>', unsafe_allow_html=True,
        )

    # ── SECTION 5: Strengths & Weak Areas ────────────────────────────────────
    divider()
    section_header("⚡", "Strengths & Development Areas")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div style="font-weight:700;color:{P["OK_BD"]};font-size:0.88rem;'
                    f'text-transform:uppercase;letter-spacing:0.05em;margin-bottom:10px">'
                    f'✅ Identified Strengths</div>', unsafe_allow_html=True)
        for s in ins["strengths"]:
            st.markdown(
                f'<div style="background:{P["OK_BG"]};border-left:3px solid {P["OK_BD"]};'
                f'border-radius:0 9px 9px 0;padding:11px 15px;margin-bottom:8px;'
                f'font-size:0.88rem;line-height:1.65;color:{P["TEXT_MAIN"]}">{s}</div>',
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown(f'<div style="font-weight:700;color:{P["WARN_BD"]};font-size:0.88rem;'
                    f'text-transform:uppercase;letter-spacing:0.05em;margin-bottom:10px">'
                    f'🔧 Development Areas</div>', unsafe_allow_html=True)

        if not weak_areas:
            st.markdown(
                f'<div class="beh-item">✅ No critical weak areas detected. '
                f'Focus on deepening advanced topics.</div>', unsafe_allow_html=True,
            )
        else:
            for wa in weak_areas[:5]:
                sev_icon = "🔴" if wa["severity"] == "Critical" else "🟡"
                st.markdown(
                    f'<div class="weak-item" style="border-left-color:{wa["color"]}">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">'
                    f'<span style="font-weight:700;font-size:0.90rem">{sev_icon} {wa["area"]}</span>'
                    f'<span style="font-size:0.78rem;font-weight:700;color:{wa["color"]}!important">'
                    f'{wa["severity"]} &nbsp;{wa["score"]}%</span></div>'
                    f'<div style="margin-bottom:7px">'
                    f'<div style="height:5px;background:{P["BORDER2"]};border-radius:3px">'
                    f'<div style="width:{wa["score"]}%;height:5px;background:{wa["color"]};border-radius:3px"></div>'
                    f'</div></div>'
                    f'<div style="font-size:0.82rem;color:{P["TEXT_MUTED"]}">💡 {wa["action"]}</div>'
                    f'</div>', unsafe_allow_html=True,
                )

    # ── SECTION 6: Programming Readiness ────────────────────────────────────
    divider()
    section_header("💻", "Programming Readiness Level")

    level_icons = {"Advanced": "🚀", "Intermediate": "📈", "Developing": "🔧"}
    c1, c2 = st.columns([1, 2])
    with c1:
        lv = ins["prog_level"]
        lv_color = ins["prog_color"]
        st.markdown(
            f'<div class="card" style="text-align:center;padding:28px 18px;">'
            f'<div style="font-size:2.5rem;margin-bottom:10px">{level_icons.get(lv,"📊")}</div>'
            f'<div style="font-size:1.3rem;font-weight:800;color:{lv_color}!important;margin-bottom:6px">{lv}</div>'
            f'<div style="font-size:0.78rem;text-transform:uppercase;letter-spacing:0.06em;'
            f'color:{P["TEXT_MUTED"]}">Programming Readiness</div>'
            f'<div style="margin-top:16px;">'
            f'<div style="font-size:2rem;font-weight:800;color:{lv_color}!important">'
            f'{ct.get("Programming_Capability",0)}%</div>'
            f'<div style="font-size:0.78rem;color:{P["TEXT_MUTED"]}">Capability Index</div>'
            f'</div></div>', unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="insight-box" style="height:100%">'
            f'<div class="ib-label">Programming Readiness Analysis</div>'
            f'<div class="ib-text">{ins["prog_insight"]}</div>'
            f'</div>', unsafe_allow_html=True,
        )

    # ── SECTION 7: AI Recommendations ─────────────────────────────────────────
    divider()
    section_header("🤖", "AI Recommendation Summary", "Personalised action plan")

    col1, col2 = st.columns(2)
    for i, rec in enumerate(ins["recommendations"]):
        col = col1 if i % 2 == 0 else col2
        col.markdown(
            f'<div class="rec-card">'
            f'<div class="rec-icon">{rec["icon"]}</div>'
            f'<div><div class="rec-title">{rec["title"]}</div>'
            f'<div class="rec-body">{rec["body"]}</div></div>'
            f'</div>', unsafe_allow_html=True,
        )

    # ── SECTION 8: Final Verdict ───────────────────────────────────────────────
    divider()
    section_header("🏁", "Final Verdict", "Comprehensive assessment conclusion")

    verdict = ins["verdict"]
    v_color = verdict["color"]
    v_bg    = P["OK_BG"] if v_color == "#2D7A4F" else P["WARN_BG"] if v_color == "#C4892A" else P["ERR_BG"]
    tags_html = "".join([
        f'<span class="v-tag" style="background:{v_bg};border-color:{v_color};color:{v_color}!important">{t}</span>'
        for t in verdict["tags"]
    ])
    st.markdown(
        f'<div class="verdict-banner" style="background:{v_bg};border-color:{v_color};">'
        f'<div style="display:flex;align-items:center;gap:14px;margin-bottom:14px">'
        f'<span style="font-size:2.2rem">{verdict["icon"]}</span>'
        f'<div class="verdict-title" style="color:{v_color}!important">{verdict["verdict"]}</div>'
        f'</div>'
        f'<div class="verdict-text">{verdict["statement"]}</div>'
        f'<div class="verdict-tags">{tags_html}</div>'
        f'</div>', unsafe_allow_html=True,
    )

    ib("info",
       f'📄 Download the full structured report from the <b>Export Report</b> page in the sidebar.')


# ── CRITICAL THINKING ─────────────────────────────────────────────────────────
elif page == "Critical Thinking":
    demo_banner()
    st.markdown(
        f'<div class="page-banner"><h1>🎯 Critical Thinking Engine</h1>'
        f'<p>Multi-dimensional cognitive scoring · Weighted formula · Radar analysis</p></div>',
        unsafe_allow_html=True,
    )
    ct = calc_critical_thinking(
        st.session_state.get("pred_label","Medium") or "Medium",
        st.session_state.get("pred_conf",0.0),
        st.session_state.get("logic_score",0.0),
        st.session_state.get("visual_score",0.0),
        st.session_state.get("prog_score",0.0),
        st.session_state.get("input_data",{}),
    )

    kpi_row([
        (f"{ct['Overall']}%",                   "Critical Thinking",     ct["Category"].split(" ",1)[-1], "#6B3A2A"),
        (f"{ct.get('Programming_Capability',0)}%","Prog Capability",     "Composite Index",               "#C4892A"),
        (f"{ct.get('Innovation_Potential',0)}%", "Innovation Potential", "Creative Index",                "#2D7A4F"),
    ])

    divider()
    col1, col2 = st.columns(2)
    col1.plotly_chart(gauge_chart(ct["Overall"]/100, "Overall Critical Thinking", "#6B3A2A"), use_container_width=True)
    col2.plotly_chart(radar_chart(ct), use_container_width=True)
    st.plotly_chart(score_breakdown_bar(ct), use_container_width=True)

    divider()
    section_header("📈", "Dimension Progress")
    skip = {"Overall","Category","Programming_Capability","Innovation_Potential"}
    items = [(k,v) for k,v in ct.items() if k not in skip]
    c1, c2 = st.columns(2)
    for i, (dim, score) in enumerate(items):
        col = c1 if i%2==0 else c2
        sc_col = "#2D7A4F" if score>=65 else "#C4892A" if score>=45 else "#B94040"
        col.markdown(
            f'<div style="display:flex;justify-content:space-between;margin-bottom:4px;">'
            f'<span style="font-weight:600;color:{P["H"]}">{dim}</span>'
            f'<span style="font-weight:700;color:{sc_col}">{score}%</span></div>',
            unsafe_allow_html=True,
        )
        col.progress(min(score/100,1.0))
        col.write("")

    with st.expander("🔢  Scoring Formula Reference", expanded=False):
        st.markdown(
            f'<div class="card-flat"><code style="background:{P["BG_CARD3"]};display:block;'
            f'padding:12px;border-radius:8px;font-size:0.85rem;line-height:1.9;color:{P["TEXT_MAIN"]}">'
            f'Critical Thinking = Academic×0.22 + Logic×0.22 + Programming×0.20 + Visual×0.16 + Habits×0.15 + Confidence×0.05\n'
            f'Prog Capability   = Programming×0.60 + Logic×0.30 + Visual×0.10\n'
            f'Innovation        = Visual×0.30 + Logic×0.25 + Programming×0.20 + Academic×0.15 + Habits×0.10'
            f'</code></div>', unsafe_allow_html=True,
        )


# ── ANALYTICS DASHBOARD ───────────────────────────────────────────────────────
elif page == "Analytics Dashboard":
    demo_banner()
    st.markdown(
        f'<div class="page-banner"><h1>📈 Analytics Dashboard</h1>'
        f'<p>Population-level academic performance analytics · Evidence-based pattern visualisation</p></div>',
        unsafe_allow_html=True,
    )
    ib("info", "📊 Insights derived from a synthetic representative cohort (n=400) "
               "reflecting realistic student population distributions.")

    with st.spinner("Loading analytics…"):
        f1, f2, f3, f4 = analytics_dashboard_charts()

    tab1,tab2,tab3,tab4 = st.tabs([
        "😤 Stress vs Performance","😴 Sleep vs Performance",
        "🧠 Logic vs Programming","📚 Study vs GPA"
    ])
    insights_map = {
        0: ("Stress Level vs Performance",
            "Stress consistently emerges as one of the strongest negative predictors of academic performance. "
            "Students in the High performance category maintain stress levels predominantly between 3–5, "
            "while Low performers cluster at 7–10. This supports clinical literature on cortisol's negative "
            "effect on working memory. Stress reduction is a high-ROI academic intervention."),
        1: ("Sleep Duration vs Performance",
            "The data reveals a clear non-linear relationship between sleep and performance. Peak performance "
            "clusters around 7.5–8.5 hrs. Notably, both under-sleepers (<6 hrs) and over-sleepers (>9 hrs) "
            "show degraded outcomes. This aligns with sleep research showing that both deprivation and "
            "excessive sleep impair executive function and information processing speed."),
        2: ("Logic Score vs Programming Ability",
            "A strong positive correlation (r ≈ 0.70) exists between logical reasoning and programming "
            "ability. This validates the platform's approach of using logic assessments as a programming "
            "readiness proxy. Students scoring above 70 in logic demonstrate consistently stronger "
            "programming capability — suggesting that logic training should precede or accompany "
            "programming instruction."),
        3: ("Study Hours vs GPA",
            "Study time shows a progressive positive relationship with GPA, particularly prominent in the "
            "High performer cluster. The bubble size (proportional to overall score) reveals that the "
            "strongest students combine both high study hours AND high GPA — confirming that quality "
            "study effort compounds over time rather than substituting for foundational knowledge."),
    }

    for i, (tab, fig) in enumerate(zip([tab1,tab2,tab3,tab4],[f1,f2,f3,f4])):
        with tab:
            tab.plotly_chart(fig, use_container_width=True)
            title, insight = insights_map[i]
            tab.markdown(
                f'<div class="card-accent"><b>{title} — Key Insight:</b><br>'
                f'<span style="font-size:0.89rem;line-height:1.7">{insight}</span></div>',
                unsafe_allow_html=True,
            )


# ── MODEL VALIDATION ─────────────────────────────────────────────────────────
elif page == "Model Validation":
    st.markdown(
        f'<div class="page-banner"><h1>✅ Model Validation</h1>'
        f'<p>Integrity check · Feature schema · Live prediction test · Preprocessing notes</p></div>',
        unsafe_allow_html=True,
    )
    model = st.session_state["model"]
    if model is None:
        ib("err", f"❌ Model not loaded: {st.session_state['model_error']}")
        st.stop()

    info = inspect_model(model)
    c1,c2,c3 = st.columns(3)
    metric_card(c1, info["model_type"].replace("Classifier",""), "Algorithm")
    metric_card(c2, info["n_features"], "Input Features")
    metric_card(c3, len(info["classes"]), "Output Classes")

    divider()
    col_a, col_b = st.columns(2)
    with col_a:
        section_header("📋","Feature Schema")
        ok, msg, features = validate_feature_schema(model)
        ib("ok" if ok else "warn", f'{"✅" if ok else "⚠️"} {msg}')
        for i, f in enumerate(features, 1):
            st.markdown(
                f'<div style="background:{P["BG_CARD2"]};border:1px solid {P["BORDER"]};'
                f'border-radius:8px;padding:7px 14px;margin-bottom:4px;display:flex;'
                f'align-items:center;gap:10px">'
                f'<span style="font-size:0.72rem;color:{P["TEXT_MUTED"]};font-weight:600;'
                f'width:24px;text-align:right">#{i:02d}</span>'
                f'<span style="font-weight:600;color:{P["H"]};font-size:0.90rem">{f}</span>'
                f'</div>', unsafe_allow_html=True,
            )

    with col_b:
        section_header("🧪","Live Prediction Test")
        ib("info","Dry-run prediction with representative sample data to verify pipeline integrity.")
        try:
            pred, proba = run_dummy_prediction(model, features)
            ib("ok",
               f'✅ <b>predict()</b> → <b>{pred}</b><br>'
               f'✅ <b>predict_proba()</b> → Functional<br>'
               f'<span style="font-size:0.82rem;color:{P["TEXT_MUTED"]}">'
               + " | ".join([f"{c}: {p*100:.1f}%" for c,p in zip(model.classes_,proba)])
               + '</span>')
        except Exception as e:
            ib("err", f"❌ Dry-run failed: {e}")

        section_header("🏷️","Output Classes")
        for cls in info["classes"]:
            bc = {"High": P["OK_BD"], "Medium": P["WARN_BD"], "Low": P["ERR_BD"]}.get(cls, "#6B3A2A")
            bb = {"High": P["OK_BG"],  "Medium": P["WARN_BG"], "Low": P["ERR_BG"]}.get(cls, P["BG_CARD2"])
            st.markdown(
                f'<span style="display:inline-block;background:{bb};border:1px solid {bc};'
                f'color:{bc}!important;padding:5px 16px;border-radius:20px;'
                f'font-weight:700;font-size:0.88rem;margin:4px 4px 0 0">{cls} Performer</span>',
                unsafe_allow_html=True,
            )

    divider()
    section_header("📌","Preprocessing Notes")
    notes = [
        ("13 numeric features", "No categorical encoding required. All features are continuous numeric values."),
        ("Feature order locked", "Exact feature order enforced from model metadata to prevent prediction drift."),
        ("Input validation", "Strict numeric range validation enforced before every prediction call."),
        ("Categorical fields", "Gender, Diet Type, Exercise are optional — used for analytics only, not prediction."),
        ("Fallback handling", "Low-confidence predictions (<55%) trigger an explicit uncertainty disclaimer."),
        ("Cache-loaded model", "@st.cache_resource ensures single model load across all user sessions."),
    ]
    c1, c2 = st.columns(2)
    for i, (title, desc) in enumerate(notes):
        col = c1 if i%2==0 else c2
        col.markdown(
            f'<div class="card-flat" style="padding:12px 16px;margin-bottom:8px">'
            f'<div style="font-weight:700;color:{P["H"]};font-size:0.88rem;margin-bottom:4px">⚙️ {title}</div>'
            f'<div style="font-size:0.84rem;color:{P["TEXT_MUTED"]};line-height:1.55">{desc}</div>'
            f'</div>', unsafe_allow_html=True,
        )


# ── EXPORT REPORT ─────────────────────────────────────────────────────────────
elif page == "Export Report":
    demo_banner()
    st.markdown(
        f'<div class="page-banner"><h1>📄 Export Report</h1>'
        f'<p>Generate and download a comprehensive structured assessment report</p></div>',
        unsafe_allow_html=True,
    )

    has_pred = bool(st.session_state.get("pred_label"))
    checks = [
        ("📊","ML Prediction",       has_pred),
        ("🧠","Logic Test",           st.session_state["logic_score"]>0),
        ("👁️","Visual Test",          st.session_state["visual_score"]>0),
        ("💻","Programming Test",     st.session_state["prog_score"]>0),
    ]
    c1,c2,c3,c4 = st.columns(4)
    for col,(icon,lbl,done) in zip([c1,c2,c3,c4],checks):
        bg = P["OK_BG"] if done else P["BG_CARD"]
        bd = P["OK_BD"] if done else P["BORDER"]
        col.markdown(
            f'<div style="background:{bg};border:1px solid {bd};border-radius:12px;'
            f'padding:16px;text-align:center">'
            f'<div style="font-size:1.5rem">{"✅" if done else "⬜"}</div>'
            f'<div style="font-weight:600;color:{P["H"]};font-size:0.87rem;margin-top:8px">{lbl}</div>'
            f'</div>', unsafe_allow_html=True,
        )

    divider()
    name = st.text_input("Student Name for Report", value=st.session_state.get("student_name","Student"))
    ct   = calc_critical_thinking(
        st.session_state.get("pred_label","Medium") or "Medium",
        st.session_state.get("pred_conf",0.0),
        st.session_state.get("logic_score",0.0),
        st.session_state.get("visual_score",0.0),
        st.session_state.get("prog_score",0.0),
        st.session_state.get("input_data",{}),
    )
    ins = cognitive_narrative(
        st.session_state.get("pred_label","Medium") or "Medium",
        st.session_state.get("pred_conf",0.0),
        ct,
        st.session_state.get("logic_score",0.0),
        st.session_state.get("visual_score",0.0),
        st.session_state.get("prog_score",0.0),
        st.session_state.get("input_data",{}),
    )

    # Report preview table
    st.markdown(f'<h3 style="color:{P["H"]}">📋 Report Summary Preview</h3>', unsafe_allow_html=True)
    verdict = ins["verdict"]
    rows = [
        ("Student",              name),
        ("ML Prediction",        st.session_state.get("pred_label","—") or "—"),
        ("Confidence",           f'{st.session_state.get("pred_conf",0)*100:.1f}%'),
        ("Logic Score",          f'{st.session_state["logic_score"]:.1f}%'),
        ("Visual Score",         f'{st.session_state["visual_score"]:.1f}%'),
        ("Programming Score",    f'{st.session_state["prog_score"]:.1f}%'),
        ("Critical Thinking",    f'{ct["Overall"]}%'),
        ("Prog Capability",      f'{ct.get("Programming_Capability",0)}%'),
        ("Innovation Potential", f'{ct.get("Innovation_Potential",0)}%'),
        ("Verdict",              verdict["verdict"]),
    ]
    c1, c2 = st.columns(2)
    for i, (k,v) in enumerate(rows):
        col = c1 if i%2==0 else c2
        col.markdown(
            f'<div style="display:flex;justify-content:space-between;padding:8px 12px;'
            f'border-radius:8px;background:{P["BG_CARD2"]};border:1px solid {P["BORDER"]};'
            f'margin-bottom:5px">'
            f'<span style="color:{P["TEXT_MUTED"]};font-size:0.86rem">{k}</span>'
            f'<span style="font-weight:700;color:{P["H"]};font-size:0.88rem">{v}</span>'
            f'</div>', unsafe_allow_html=True,
        )

    report_bytes = generate_text_report(
        student_name = name,
        user_input   = st.session_state.get("input_data",{}),
        pred_label   = st.session_state.get("pred_label","N/A") or "N/A",
        pred_conf    = st.session_state.get("pred_conf",0.0),
        logic_score  = st.session_state.get("logic_score",0.0),
        visual_score = st.session_state.get("visual_score",0.0),
        prog_score   = st.session_state.get("prog_score",0.0),
        ct           = ct,
    )

    divider()
    st.download_button(
        label     = "⬇️  Download Full Assessment Report (.txt)",
        data      = report_bytes,
        file_name = f"CogniSight_{name.replace(' ','_')}_Report.txt",
        mime      = "text/plain",
        use_container_width=True,
    )
    ib("info",
       "📋 The exported report includes: ML prediction · confidence analysis · all cognitive scores · "
       "critical thinking breakdown · programming capability · innovation potential · "
       "AI-generated cognitive summary · full student profile data.")
