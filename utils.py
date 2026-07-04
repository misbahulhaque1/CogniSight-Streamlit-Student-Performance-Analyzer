"""
utils.py
========
Shared helpers: model loading, validation, prediction, charting, scoring, reports.
Upgraded — Premium Brown + White Cognitive Analyzer.
"""

import warnings
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── Feature Schema (exact model order, verified against pkl) ─────────────────
MODEL_FEATURES = [
    "Age",
    "Sleep_Duration",
    "Stress_Level",
    "Daily_Screen_Time",
    "Caffeine_Intake",
    "Reaction_Time",
    "Memory_Test_Score",
    "Cognitive_Score",
    "Study_Hours_Per_Day",
    "Attendance_Rate",
    "Previous_GPA",
    "Logic_Test_Score",
    "Logic_Error_Rate",
]

OPTIONAL_FIELDS = ["Gender", "Diet_Type", "Exercise_Frequency"]

# ─── Premium Brown + White Palette ───────────────────────────────────────────
COLORS = {
    "High":        "#2D7A4F",
    "Medium":      "#C4892A",
    "Low":         "#B94040",
    "Primary":     "#6B3A2A",
    "Secondary":   "#C4892A",
    "Accent":      "#8B5E3C",
    "Info":        "#2C6E8A",
    "BgCard":      "#FFFFFF",
    "BgPage":      "#FDFAF7",
    "Text":        "#2C1A0E",
    "Muted":       "#9C7B6B",
    "Border":      "#E8D5C4",
}

# Plotly shared theme
_T = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,253,250,0.85)",
    font=dict(color=COLORS["Text"], family="Georgia, serif", size=12),
    margin=dict(l=20, r=20, t=50, b=20),
)


# ─── Model Lifecycle ──────────────────────────────────────────────────────────

def load_model(path="final_random_forest_model.pkl"):
    """Load model safely; returns (model, error_str)."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = joblib.load(path)
        return model, None
    except FileNotFoundError:
        return None, f"Model file not found: {path}"
    except Exception as exc:
        return None, f"Model load failed: {exc}"


def inspect_model(model):
    """Return key metadata dict for validation display."""
    if model is None:
        return {"model_type": "Not Loaded", "n_features": 0,
                "feature_names": [], "classes": []}
    return {
        "model_type":    type(model).__name__,
        "n_features":    int(getattr(model, "n_features_in_", 0)),
        "feature_names": list(getattr(model, "feature_names_in_", MODEL_FEATURES)),
        "classes":       list(getattr(model, "classes_", ["High", "Medium", "Low"])),
    }


def validate_feature_schema(model):
    """Check feature compatibility; returns (ok, message, feature_list)."""
    if model is None:
        return False, "Model not loaded.", MODEL_FEATURES
    info     = inspect_model(model)
    features = info["feature_names"] if info["feature_names"] else MODEL_FEATURES
    if info["n_features"] and info["n_features"] != len(features):
        return (False,
                f"Feature count mismatch: model={info['n_features']}, schema={len(features)}",
                features)
    return True, "Feature schema validated successfully.", features


def run_dummy_prediction(model, feature_order):
    """Dry-run with safe sample values to verify predict() and predict_proba()."""
    dummy = {
        "Age": 22, "Sleep_Duration": 7.0, "Stress_Level": 5,
        "Daily_Screen_Time": 4.0, "Caffeine_Intake": 120,
        "Reaction_Time": 340, "Memory_Test_Score": 72, "Cognitive_Score": 75,
        "Study_Hours_Per_Day": 4.5, "Attendance_Rate": 0.88,
        "Previous_GPA": 3.1, "Logic_Test_Score": 70, "Logic_Error_Rate": 0.22,
    }
    X     = build_feature_frame(dummy, feature_order)
    pred  = model.predict(X)[0]
    proba = model.predict_proba(X)[0] if hasattr(model, "predict_proba") else None
    return pred, proba


# ─── Input Validation & Frame Builder ────────────────────────────────────────

FIELD_RANGES = [
    ("Age",                 15,  60),
    ("Sleep_Duration",      3.0, 12.0),
    ("Stress_Level",        1,   10),
    ("Daily_Screen_Time",   0.0, 16.0),
    ("Caffeine_Intake",     0,   600),
    ("Reaction_Time",       150, 900),
    ("Memory_Test_Score",   0,   100),
    ("Cognitive_Score",     0,   100),
    ("Study_Hours_Per_Day", 0.0, 14.0),
    ("Attendance_Rate",     0.0, 1.0),
    ("Previous_GPA",        0.0, 4.0),
    ("Logic_Test_Score",    0,   100),
    ("Logic_Error_Rate",    0.0, 1.0),
]


def validate_student_input(user_input):
    errors = []
    for key, lo, hi in FIELD_RANGES:
        if key not in user_input:
            errors.append(f"Missing: {key}")
            continue
        try:
            val = float(user_input[key])
        except Exception:
            errors.append(f"Invalid numeric value for {key}.")
            continue
        if not (lo <= val <= hi):
            errors.append(f"{key} = {val} is out of range [{lo}, {hi}].")
    return len(errors) == 0, errors


def build_feature_frame(user_input, feature_order):
    """Create an ordered DataFrame that matches the trained model schema exactly."""
    row = {}
    for feat in feature_order:
        if feat not in user_input:
            raise ValueError(f"Missing required feature: {feat}")
        row[feat] = float(user_input[feat])
    return pd.DataFrame([row], columns=feature_order)


# ─── Prediction Engine ────────────────────────────────────────────────────────

def predict_performance(model, user_input):
    """
    Full prediction pipeline: validate schema → validate input → predict.
    Returns (label, confidence, proba_dict, errors).
    """
    _fb = ("Medium", 0.0, {"High": 0.33, "Low": 0.33, "Medium": 0.34})

    ok, msg, feature_order = validate_feature_schema(model)
    if not ok:
        return _fb[0], _fb[1], _fb[2], [msg]

    valid, errs = validate_student_input(user_input)
    if not valid:
        return _fb[0], _fb[1], _fb[2], errs

    try:
        X     = build_feature_frame(user_input, feature_order)
        label = str(model.predict(X)[0])
        if hasattr(model, "predict_proba"):
            raw    = model.predict_proba(X)[0]
            proba  = {c: float(p) for c, p in zip(model.classes_, raw)}
            conf   = max(proba.values())
        else:
            proba, conf = {"High": 0.0, "Low": 0.0, "Medium": 0.0}, 0.0
        return label, conf, proba, []
    except Exception as exc:
        return _fb[0], _fb[1], _fb[2], [f"Prediction error: {exc}"]


# ─── Scoring ──────────────────────────────────────────────────────────────────

def score_band(score: float) -> str:
    if score >= 80: return "🏆 Exceptional"
    if score >= 65: return "✅ Strong"
    if score >= 50: return "📈 Average"
    if score >= 35: return "⚠️ Developing"
    return "🔴 Needs Work"


def score_color(score: float) -> str:
    if score >= 65: return COLORS["High"]
    if score >= 45: return COLORS["Medium"]
    return COLORS["Low"]


# ─── Critical Thinking Calculator ────────────────────────────────────────────

def calc_critical_thinking(pred_label, pred_conf, logic_score, visual_score,
                            prog_score, user_input):
    """
    Formula-based multi-dimensional cognitive score.

    Weights:  Academic(ML) 22% | Logic 22% | Programming 20% |
              Visual 16%       | Habits 15% | Confidence 5%
    """
    perf_map  = {"High": 90, "Medium": 62, "Low": 35}
    study_h   = float(user_input.get("Study_Hours_Per_Day", 4))
    sleep_h   = float(user_input.get("Sleep_Duration", 7))
    stress    = float(user_input.get("Stress_Level", 5))
    attend    = float(user_input.get("Attendance_Rate", 0.85))
    gpa       = float(user_input.get("Previous_GPA", 3.0))

    habit_score = (
        min(study_h / 10, 1.0) * 30
        + min(sleep_h / 9,  1.0) * 20
        + (1 - min(stress / 10, 1.0)) * 20
        + min(attend, 1.0) * 15
        + min(gpa / 4.0, 1.0) * 15
    )

    dims = {
        "Academic (ML)":  round(perf_map.get(pred_label, 62)),
        "Logic":           round(logic_score),
        "Visual":          round(visual_score),
        "Programming":     round(prog_score),
        "Habits":          round(habit_score),
        "Confidence":      round(pred_conf * 100),
    }

    overall = round(
        dims["Academic (ML)"]  * 0.22
        + dims["Logic"]        * 0.22
        + dims["Visual"]       * 0.16
        + dims["Programming"]  * 0.20
        + dims["Habits"]       * 0.15
        + dims["Confidence"]   * 0.05
    )

    prog_cap   = round(prog_score * 0.60 + logic_score * 0.30 + visual_score * 0.10)
    innovation = round(
        visual_score * 0.30 + logic_score * 0.25 + prog_score * 0.20
        + dims["Academic (ML)"] * 0.15 + habit_score * 0.10
    )

    category = (
        "🏆 Advanced Cognitive Thinker" if overall >= 78
        else "📈 Developing Thinker" if overall >= 55
        else "⚠️ Foundational Stage"
    )

    dims["Overall"]               = overall
    dims["Category"]              = category
    dims["Programming_Capability"] = prog_cap
    dims["Innovation_Potential"]  = innovation
    return dims


# ─── Charts ──────────────────────────────────────────────────────────────────

def gauge_chart(value: float, title: str, color: str = "#6B3A2A"):
    """Rich gauge chart — value 0‒1, displayed as percentage."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=round(value * 100, 1),
            number={"suffix": "%", "font": {"size": 38, "color": COLORS["Primary"]}},
            gauge={
                "axis": {"range": [0, 100],
                         "tickcolor": COLORS["Muted"],
                         "tickfont": {"size": 9, "color": COLORS["Muted"]}},
                "bar": {"color": color, "thickness": 0.3},
                "bgcolor": "rgba(232,213,196,0.3)",
                "borderwidth": 1,
                "bordercolor": COLORS["Border"],
                "steps": [
                    {"range": [0,  40], "color": "rgba(185,64,64,0.10)"},
                    {"range": [40, 65], "color": "rgba(196,137,42,0.10)"},
                    {"range": [65,100], "color": "rgba(45,122,79,0.10)"},
                ],
                "threshold": {
                    "line": {"color": COLORS["Primary"], "width": 2},
                    "thickness": 0.75, "value": 65,
                },
            },
            title={"text": title, "font": {"size": 14, "color": COLORS["Primary"]}},
        )
    )
    fig.update_layout(**_T, height=290)
    return fig


def radar_chart(dimensions: dict):
    """Spider/radar chart for multi-dimensional cognitive profile."""
    skip   = {"Overall", "Category", "Programming_Capability", "Innovation_Potential"}
    dims   = {k: v for k, v in dimensions.items() if k not in skip}
    labels = list(dims.keys())
    values = list(dims.values())
    fig    = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill="toself",
        fillcolor="rgba(107,58,42,0.15)",
        line=dict(color=COLORS["Primary"], width=2.5),
        marker=dict(color=COLORS["Secondary"], size=7),
        name="Profile",
    ))
    fig.update_layout(
        **_T,
        polar=dict(
            radialaxis=dict(
                visible=True, range=[0, 100],
                tickfont=dict(size=9, color=COLORS["Muted"]),
                gridcolor=COLORS["Border"],
            ),
            angularaxis=dict(tickfont=dict(size=10, color=COLORS["Text"])),
            bgcolor="rgba(253,250,247,0.7)",
        ),
        showlegend=False, height=400,
        title=dict(text="Cognitive Dimension Radar",
                   font=dict(size=14, color=COLORS["Primary"])),
    )
    return fig


def probability_bar(proba: dict):
    """Vertical bar chart for class probability."""
    labels = list(proba.keys())
    values = [v * 100 for v in proba.values()]
    colors = [COLORS.get(lbl, COLORS["Accent"]) for lbl in labels]
    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=colors,
        marker_line_color=COLORS["Border"], marker_line_width=1,
        text=[f"{v:.1f}%" for v in values], textposition="outside",
        textfont=dict(size=14, color=COLORS["Text"]),
    ))
    fig.update_layout(
        **_T,
        yaxis=dict(range=[0, 120], title="Probability (%)", gridcolor=COLORS["Border"]),
        xaxis=dict(title="Performance Class"),
        height=300,
        title=dict(text="Class Probability Distribution",
                   font=dict(size=14, color=COLORS["Primary"])),
    )
    return fig


def score_breakdown_bar(dimensions: dict):
    """Horizontal bar for cognitive dimension scores."""
    skip   = {"Overall", "Category", "Programming_Capability", "Innovation_Potential"}
    dims   = {k: v for k, v in dimensions.items() if k not in skip}
    labels = list(dims.keys())
    values = list(dims.values())
    colors = [score_color(v) for v in values]
    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker_color=colors,
        marker_line_color=COLORS["Border"], marker_line_width=1,
        text=[f"{v}%" for v in values], textposition="outside",
        textfont=dict(color=COLORS["Text"]),
    ))
    fig.update_layout(
        **_T,
        xaxis=dict(range=[0, 120], title="Score (%)", gridcolor=COLORS["Border"]),
        height=320,
        title=dict(text="Dimension Score Breakdown",
                   font=dict(size=14, color=COLORS["Primary"])),
    )
    return fig


def analytics_dashboard_charts():
    """Synthetic representative analytics — four Plotly figures."""
    rng = np.random.default_rng(42)
    n   = 400
    stress = rng.integers(1, 11, n).astype(float)
    sleep  = rng.uniform(4, 10, n)
    logic  = rng.uniform(20, 100, n)
    prog   = np.clip(logic * 0.7 + rng.normal(0, 18, n), 0, 100)
    study  = rng.uniform(1, 12, n)
    gpa    = rng.uniform(1.5, 4.0, n)
    attend = rng.uniform(0.5, 1.0, n)
    raw    = (55 + logic * 0.22 + prog * 0.18 + (10 - stress) * 2.2
              + sleep * 2.0 + study * 2.5 + gpa * 3.5 + attend * 10
              + rng.normal(0, 7, n))
    perf   = np.where(raw >= 82, "High", np.where(raw >= 63, "Medium", "Low"))
    df     = pd.DataFrame({"Stress": stress, "Sleep": sleep, "Logic": logic,
                           "Programming": prog, "Study Hours": study,
                           "GPA": gpa, "Performance": perf, "Score": raw})
    cmap   = {"High": COLORS["High"], "Medium": COLORS["Medium"], "Low": COLORS["Low"]}
    order  = {"Performance": ["High", "Medium", "Low"]}

    fig1 = px.box(df, x="Performance", y="Stress", color="Performance",
                  color_discrete_map=cmap, category_orders=order,
                  title="Stress Level vs Academic Performance")
    fig2 = px.violin(df, x="Performance", y="Sleep", color="Performance",
                     color_discrete_map=cmap, box=True, category_orders=order,
                     title="Sleep Duration vs Academic Performance")
    fig3 = px.scatter(df, x="Logic", y="Programming", color="Performance",
                      color_discrete_map=cmap, opacity=0.65,
                      title="Logic Score vs Programming Ability",
                      trendline="ols",
                      trendline_color_override=COLORS["Primary"])
    fig4 = px.scatter(df, x="Study Hours", y="GPA", color="Performance",
                      color_discrete_map=cmap, opacity=0.65, size="Score",
                      size_max=12, title="Study Hours vs GPA")
    for fig in [fig1, fig2, fig3, fig4]:
        fig.update_layout(**_T)
    return fig1, fig2, fig3, fig4


# ─── Report ───────────────────────────────────────────────────────────────────

def generate_text_report(student_name, user_input, pred_label, pred_conf,
                          logic_score, visual_score, prog_score, ct):
    """Build a polished plain-text report; returns UTF-8 bytes."""
    S  = "=" * 62
    S2 = "-" * 62
    lines = [
        S, "  INTELLIGENT STUDENT COGNITIVE & PERFORMANCE ANALYZER",
        "  Machine Learning + Cognitive Engine Report", S,
        f"  Student   : {student_name}",
        f"  Generated : {datetime.now().strftime('%Y-%m-%d  %H:%M')}",
        S, "",
        "[ ML MODEL PREDICTION ]", S2,
        f"  Performance Class : {pred_label}",
        f"  Confidence        : {pred_conf * 100:.1f}%", "",
        "[ COGNITIVE TEST SCORES ]", S2,
        f"  Logical Reasoning   : {logic_score:.1f}%  — {score_band(logic_score)}",
        f"  Visual Intelligence : {visual_score:.1f}%  — {score_band(visual_score)}",
        f"  Programming Logic   : {prog_score:.1f}%  — {score_band(prog_score)}", "",
        "[ CRITICAL THINKING ANALYSIS ]", S2,
        f"  Overall Critical Thinking : {ct['Overall']}%",
        f"  Category                  : {ct['Category']}",
        f"  Programming Capability    : {ct.get('Programming_Capability', 'N/A')}%",
        f"  Innovation Potential      : {ct.get('Innovation_Potential', 'N/A')}%", "",
        "  Dimension Scores:",
    ]
    skip = {"Overall", "Category", "Programming_Capability", "Innovation_Potential"}
    for k, v in ct.items():
        if k not in skip:
            lines.append(f"    {k:<22}: {v}%")
    lines += ["", "[ INPUT DATA ]", S2]
    labels = {
        "Age": "Age", "Sleep_Duration": "Sleep (hrs)",
        "Stress_Level": "Stress (1-10)", "Daily_Screen_Time": "Screen Time (hrs)",
        "Caffeine_Intake": "Caffeine (mg)", "Reaction_Time": "Reaction Time (ms)",
        "Memory_Test_Score": "Memory Score", "Cognitive_Score": "Cognitive Score",
        "Study_Hours_Per_Day": "Study Hours/Day", "Attendance_Rate": "Attendance Rate",
        "Previous_GPA": "Previous GPA", "Logic_Test_Score": "Logic Test Score",
        "Logic_Error_Rate": "Logic Error Rate",
    }
    for k, v in user_input.items():
        lines.append(f"  {labels.get(k, k):<28}: {v}")
    lines += ["", S,
              "  Results are indicative guidance only.",
              "  Generated by the Cognitive Analyzer System.", S]
    return "\n".join(lines).encode("utf-8")
