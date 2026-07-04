"""
insights.py
===========
Intelligence Engine — generates human-quality, personalised academic insights
from ML predictions, cognitive scores, and student lifestyle data.

All outputs are in a confident, academic, non-robotic voice suitable for
university-level evaluation and recruiter presentations.
"""

# ─── Presentation Mode Sample Profile ─────────────────────────────────────────
DEMO_PROFILE = {
    # Identity
    "name":               "Aisha Malik",
    "age_group":          "Junior",
    # Model features (exact schema)
    "Age":                21,
    "Sleep_Duration":     7.5,
    "Stress_Level":       5,
    "Daily_Screen_Time":  4.0,
    "Caffeine_Intake":    100,
    "Reaction_Time":      290,
    "Memory_Test_Score":  81,
    "Cognitive_Score":    84,
    "Study_Hours_Per_Day":5.5,
    "Attendance_Rate":    0.91,
    "Previous_GPA":       3.4,
    "Logic_Test_Score":   78,
    "Logic_Error_Rate":   0.14,
    # Optional
    "Gender":             "Female",
    "Diet_Type":          "Vegetarian",
    "Exercise_Frequency": "Medium",
    # Pre-set test scores (demo)
    "logic_score":        80.0,
    "visual_score":       75.0,
    "prog_score":         70.0,
}


# ─── Low-Confidence Fallback Messaging ────────────────────────────────────────
def confidence_disclaimer(conf: float) -> dict:
    """
    Returns a dict with level label and message when confidence is low.
    conf is 0–1.
    """
    if conf >= 0.75:
        return {"level": "High", "color": "#2D7A4F",
                "msg": "The model prediction carries high confidence based on the provided profile data."}
    if conf >= 0.55:
        return {"level": "Moderate", "color": "#C4892A",
                "msg": "The prediction is moderately confident. A few lifestyle or academic indicators show mixed signals, which may require a follow-up assessment."}
    return {"level": "Low", "color": "#B94040",
            "msg": "Confidence is below threshold. The student's profile contains conflicting indicators. Treat this prediction as directional — not definitive. Recommend a manual review."}


# ─── Cognitive Narrative Generator ────────────────────────────────────────────
def cognitive_narrative(pred_label: str, conf: float, ct: dict,
                         logic: float, visual: float, prog: float,
                         data: dict) -> dict:
    """
    Returns a rich dict of human-quality insight strings across 7 analysis areas.
    """
    overall    = ct.get("Overall", 0)
    prog_cap   = ct.get("Programming_Capability", 0)
    innovation = ct.get("Innovation_Potential", 0)
    habits     = ct.get("Habits", 50)
    sleep      = float(data.get("Sleep_Duration", 7))
    stress     = float(data.get("Stress_Level", 5))
    study      = float(data.get("Study_Hours_Per_Day", 4))
    attend     = float(data.get("Attendance_Rate", 0.85))
    gpa        = float(data.get("Previous_GPA", 3.0))
    react      = float(data.get("Reaction_Time", 350))
    memory     = float(data.get("Memory_Test_Score", 70))
    screen     = float(data.get("Daily_Screen_Time", 4))
    caffeine   = float(data.get("Caffeine_Intake", 100))

    # ── 1. Cognitive Summary ──────────────────────────────────────────────────
    if overall >= 78:
        cog_summary = (
            f"This student exhibits a well-developed cognitive profile with an overall critical "
            f"thinking score of {overall}%. Their performance across logical reasoning, visual "
            f"intelligence, and programming logic is consistently strong, suggesting a high "
            f"capacity for complex problem-solving and analytical work. This level of cognitive "
            f"breadth is characteristic of students who thrive in research, engineering, and "
            f"technology-focused academic environments."
        )
    elif overall >= 58:
        cog_summary = (
            f"The student demonstrates a solid cognitive foundation with an overall score of "
            f"{overall}%. While core reasoning abilities are present, there is measurable "
            f"variance across domains — particularly between visual-spatial processing and "
            f"abstract logic. With targeted practice in their weaker areas, this student has "
            f"clear potential to advance into the high-performance tier within one academic semester."
        )
    else:
        cog_summary = (
            f"The student's cognitive profile registers at {overall}%, indicating that foundational "
            f"reasoning and problem-solving skills are still in development. This is not uncommon "
            f"among early-stage learners transitioning into technical disciplines. A structured "
            f"intervention focusing on logical sequencing, pattern recognition, and consistent "
            f"study habits can significantly accelerate cognitive development over the next 8–12 weeks."
        )

    # ── 2. Learning Behaviour Insights ───────────────────────────────────────
    behaviours = []

    # Sleep
    if sleep >= 7.5:
        behaviours.append(
            f"Sleep hygiene is excellent at {sleep} hrs/night — a strong predictor of memory "
            f"consolidation, attention, and next-day cognitive performance.")
    elif sleep >= 6:
        behaviours.append(
            f"Sleep duration of {sleep} hrs is adequate but not optimal. Research consistently "
            f"shows that 7.5–8.5 hrs produces measurably better learning retention and reaction speed.")
    else:
        behaviours.append(
            f"Sleep deprivation at {sleep} hrs/night is a significant academic risk factor. "
            f"Chronic under-sleeping impairs working memory, attention span, and decision quality — "
            f"all critical for performance in technical courses.")

    # Stress
    if stress <= 4:
        behaviours.append(
            f"Low stress level ({stress}/10) suggests good emotional regulation, which creates "
            f"an optimal cognitive state for deep learning and knowledge retention.")
    elif stress <= 6:
        behaviours.append(
            f"Moderate stress ({stress}/10) is within normal academic range. However, when "
            f"combined with high screen time or poor sleep, it can erode sustained focus. "
            f"Mindfulness or structured breaks are recommended.")
    else:
        behaviours.append(
            f"Elevated stress at {stress}/10 is a notable concern. High chronic stress activates "
            f"the cortisol response, which is directly antagonistic to long-term memory formation "
            f"and logical reasoning under exam conditions. Immediate stress-management intervention is advised.")

    # Study hours
    if study >= 5:
        behaviours.append(
            f"Daily study investment of {study} hrs reflects strong academic discipline and "
            f"correlates positively with GPA outcomes in the dataset population.")
    elif study >= 3:
        behaviours.append(
            f"Study time of {study} hrs/day is moderate. Increasing this to at least 5 hrs with "
            f"active recall techniques (not passive re-reading) can produce disproportionate improvement.")
    else:
        behaviours.append(
            f"Study time of {study} hrs/day is critically low for a technical degree. "
            f"Students in STEM fields typically require 5–7 hrs of focused daily engagement to "
            f"keep pace with curriculum complexity. Immediate restructuring of the daily schedule is needed.")

    # Attendance
    if attend >= 0.9:
        behaviours.append(
            f"Attendance rate of {attend*100:.0f}% is commendable. Consistent presence directly "
            f"correlates with higher comprehension and peer-learning benefits that self-study cannot replicate.")
    elif attend >= 0.75:
        behaviours.append(
            f"Attendance of {attend*100:.0f}% is acceptable but shows some absence patterns. "
            f"Missing more than 10% of classes typically results in knowledge gaps that compound "
            f"in fast-paced technical courses.")
    else:
        behaviours.append(
            f"Attendance below {attend*100:.0f}% is a significant academic risk indicator. "
            f"This level of absenteeism strongly correlates with poor exam performance and course failure. "
            f"Immediate re-engagement with faculty is strongly recommended.")

    # Screen time
    if screen > 8:
        behaviours.append(
            f"Screen time of {screen} hrs/day is excessive. High non-academic screen use fragments "
            f"attention, disrupts sleep cycles, and competes directly with study time.")
    elif screen > 5:
        behaviours.append(
            f"Screen time of {screen} hrs/day is above optimal. Consider auditing how much is "
            f"academic vs entertainment — the distinction matters significantly for cognitive load.")

    # ── 3. Strengths ─────────────────────────────────────────────────────────
    strengths = []
    score_pairs = [
        ("Logical Reasoning",    logic),
        ("Visual Intelligence",  visual),
        ("Programming Logic",    prog),
        ("Memory Performance",   memory),
    ]
    top_scores = sorted(score_pairs, key=lambda x: x[1], reverse=True)

    for name, score in top_scores[:3]:
        if score >= 70:
            strengths.append(_strength_phrase(name, score))

    if gpa >= 3.5:
        strengths.append(f"Consistently strong academic record (GPA {gpa:.1f}) demonstrates sustained engagement and knowledge mastery.")
    if attend >= 0.9:
        strengths.append("Exceptional class attendance reflects strong academic commitment and proactive learning mindset.")
    if react <= 280:
        strengths.append(f"Reaction time of {react:.0f}ms is in the top tier, suggesting strong neural processing speed and situational awareness.")
    if memory >= 75:
        strengths.append(f"Memory test score of {memory:.0f}% indicates well-developed information encoding and retrieval mechanisms.")

    if not strengths:
        strengths.append("The student demonstrates resilience and a willingness to engage with challenging cognitive tasks — a valuable foundational trait.")

    # ── 4. Development Areas ─────────────────────────────────────────────────
    weaknesses = []
    bottom_scores = sorted(score_pairs, key=lambda x: x[1])

    for name, score in bottom_scores[:2]:
        if score < 65:
            weaknesses.append(_weakness_phrase(name, score))

    if stress >= 7:
        weaknesses.append(f"Stress management ({stress}/10) needs urgent attention — it is actively suppressing cognitive performance.")
    if sleep < 6.5:
        weaknesses.append(f"Insufficient sleep ({sleep} hrs) is undermining memory consolidation and attention span.")
    if attend < 0.80:
        weaknesses.append(f"Low attendance ({attend*100:.0f}%) is creating compounding knowledge gaps.")
    if study < 3:
        weaknesses.append(f"Inadequate study time ({study} hrs/day) is insufficient for technical curriculum demands.")

    if not weaknesses:
        weaknesses.append("No critical developmental gaps detected. Focus should shift to deepening advanced topics and research exposure.")

    # ── 5. Programming Readiness ──────────────────────────────────────────────
    if prog_cap >= 78:
        prog_level = "Advanced"
        prog_color = "#2D7A4F"
        prog_insight = (
            f"With a programming capability index of {prog_cap}%, this student is ready for "
            f"advanced software development coursework, competitive programming, and industry internships. "
            f"Their logical reasoning strongly complements their programming score, which is the exact "
            f"combination employers seek in technical roles. Exposure to system design and algorithm "
            f"complexity is the recommended next step."
        )
    elif prog_cap >= 58:
        prog_level = "Intermediate"
        prog_color = "#C4892A"
        prog_insight = (
            f"Programming capability at {prog_cap}% places this student in the intermediate tier. "
            f"Core programming constructs are understood, but abstract problem decomposition and "
            f"algorithm optimisation remain areas for growth. Consistent practice with LeetCode-style "
            f"problems (medium difficulty) and building 2–3 complete projects will accelerate readiness "
            f"for technical interviews and industry placements within one semester."
        )
    else:
        prog_level = "Developing"
        prog_color = "#B94040"
        prog_insight = (
            f"Programming capability index of {prog_cap}% indicates that fundamental programming "
            f"concepts require reinforcement. The gap between logical reasoning and code-execution "
            f"accuracy suggests that theory is understood but translating it into working code is "
            f"still challenging. Daily coding practice of at least 45 minutes on structured exercises "
            f"(e.g., Python basics, control flow, data structures) for 6–8 weeks will produce "
            f"measurable improvement."
        )

    # ── 6. AI Recommendations ────────────────────────────────────────────────
    recommendations = _build_recommendations(
        pred_label, logic, visual, prog, sleep, stress, study, attend, gpa,
        prog_cap, overall, memory, react, screen, caffeine
    )

    # ── 7. Final Verdict ──────────────────────────────────────────────────────
    verdict = _build_final_verdict(pred_label, conf, overall, prog_cap, innovation, gpa)

    return {
        "cognitive_summary":   cog_summary,
        "behaviours":          behaviours,
        "strengths":           strengths,
        "weaknesses":          weaknesses,
        "prog_level":          prog_level,
        "prog_color":          prog_color,
        "prog_insight":        prog_insight,
        "recommendations":     recommendations,
        "verdict":             verdict,
    }


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _strength_phrase(name: str, score: float) -> str:
    phrases = {
        "Logical Reasoning": [
            f"Logical reasoning ability ({score:.0f}%) is a standout strength — this student can identify patterns, deconstruct arguments, and construct valid inferences with high reliability.",
            f"Above-average logical reasoning ({score:.0f}%) positions this student well for algorithm design, data analysis, and research-oriented roles.",
        ],
        "Visual Intelligence": [
            f"Visual intelligence at {score:.0f}% indicates strong spatial reasoning — critical for UI/UX design, data visualisation, computer architecture, and geometry-heavy domains.",
            f"High visual-spatial ability ({score:.0f}%) enables efficient mental model construction — valuable in engineering, 3D modelling, and systems thinking.",
        ],
        "Programming Logic": [
            f"Programming logic score of {score:.0f}% demonstrates the ability to trace code execution, predict output, and reason about control flow — core competencies in software development.",
            f"Strong programming logic ({score:.0f}%) reflects well-developed computational thinking — the student can work through bugs and optimise logic mentally before coding.",
        ],
        "Memory Performance": [
            f"Memory performance at {score:.0f}% shows strong retention capacity — this student can hold and manipulate multiple concepts in working memory, essential for complex problem-solving.",
        ],
    }
    options = phrases.get(name, [f"{name} at {score:.0f}% is a notable strength."])
    return options[int(score * 100) % len(options)]


def _weakness_phrase(name: str, score: float) -> str:
    phrases = {
        "Logical Reasoning": (
            f"Logical reasoning ({score:.0f}%) shows inconsistencies in deductive thinking. "
            f"Recommend: daily 15-minute pattern recognition puzzles and formal logic exercises."
        ),
        "Visual Intelligence": (
            f"Visual-spatial intelligence ({score:.0f}%) is below the performance threshold. "
            f"Spatial reasoning can be improved through puzzles, 3D visualisation tools, and diagram-based learning."
        ),
        "Programming Logic": (
            f"Programming logic ({score:.0f}%) indicates difficulty tracing execution flow. "
            f"Recommend: code-tracing exercises with pen-and-paper before running code, and structured pseudocode practice."
        ),
        "Memory Performance": (
            f"Memory test performance ({score:.0f}%) suggests limited working memory capacity. "
            f"Spaced repetition (Anki), mind mapping, and interleaved practice are evidence-based remediation techniques."
        ),
    }
    return phrases.get(name, f"{name} at {score:.0f}% requires targeted improvement.")


def _build_recommendations(pred_label, logic, visual, prog, sleep, stress,
                             study, attend, gpa, prog_cap, overall, memory,
                             react, screen, caffeine):
    recs = []

    # Academic performance level
    if pred_label == "High":
        recs.append({
            "icon": "🎯",
            "title": "Pursue Advanced Challenges",
            "body": "Academic performance is in the top tier. Enrol in honours courses, participate in research projects, or compete in national-level programming contests. Maintaining this trajectory will open pathways to graduate school and competitive industry placements."
        })
    elif pred_label == "Medium":
        recs.append({
            "icon": "📈",
            "title": "Consolidate and Accelerate",
            "body": "Performance is solid but not yet at peak potential. Identify which 2–3 subjects are dragging the average and allocate focused weekly sessions to each. Forming a study group with high performers can create a measurable upward shift within 4–6 weeks."
        })
    else:
        recs.append({
            "icon": "🔧",
            "title": "Structured Academic Recovery Plan",
            "body": "Current academic indicators suggest an elevated risk of underperformance. A structured 8-week recovery plan with weekly check-ins, mandatory tutoring sessions, and portfolio building is strongly recommended. Early intervention produces the best outcomes."
        })

    # Cognitive specific
    if logic < 60:
        recs.append({
            "icon": "🧠",
            "title": "Logic Training Protocol",
            "body": "Logical reasoning score falls below the competency threshold. Begin with 20 minutes of structured logic puzzles daily (Sudoku, sequence problems, syllogisms). Progress to formal argument analysis by week 3. Re-test in 6 weeks to track improvement."
        })
    if prog_cap < 60:
        recs.append({
            "icon": "💻",
            "title": "Programming Competency Bridge",
            "body": "Programming capability requires structured reinforcement. Complete a 30-day Python problem-solving challenge (one problem per day, medium difficulty). Focus on loops, recursion, and data structure manipulation. Track error rate weekly as a metric."
        })
    if visual < 55:
        recs.append({
            "icon": "👁️",
            "title": "Spatial Reasoning Development",
            "body": "Visual-spatial intelligence is below optimal. Integrate diagram-first learning: always sketch data flows, system architectures, and algorithms before writing code. Use tools like draw.io for technical diagrams. 3D puzzle games can also improve spatial manipulation."
        })

    # Lifestyle
    if sleep < 6.5:
        recs.append({
            "icon": "😴",
            "title": "Sleep Optimisation — High Priority",
            "body": f"Current sleep of {sleep} hrs is critically insufficient. Set a non-negotiable sleep window of 7.5–8 hrs. Avoid screens 45 minutes before sleep. Even 2 additional hours per night produces measurable improvement in exam scores within 10 days."
        })
    if stress >= 7:
        recs.append({
            "icon": "🧘",
            "title": "Stress Regulation Protocol",
            "body": f"Stress at {stress}/10 is actively impeding cognitive performance. Implement a 10-minute daily mindfulness routine (apps: Headspace, Calm). Break study blocks into 50-minute Pomodoro intervals with 10-minute movement breaks. Review workload distribution with an academic advisor."
        })
    if study < 3.5:
        recs.append({
            "icon": "📚",
            "title": "Study Time Architecture",
            "body": f"At {study} hrs/day, study time is insufficient for technical degree demands. Redesign the daily schedule: allocate 2 hrs in the morning for new material, 2 hrs in the afternoon for problem sets, and 1 hr in the evening for review. Use time-blocking, not open-ended study sessions."
        })
    if screen > 7:
        recs.append({
            "icon": "📵",
            "title": "Digital Hygiene Audit",
            "body": f"Screen time of {screen} hrs/day is fragmenting attention and competing with study time. Use Screen Time (iOS) or Digital Wellbeing (Android) to audit entertainment vs. academic use. Set hard limits: no social media after 9 PM, and no phone during study blocks."
        })

    # Always include a growth mindset rec
    recs.append({
        "icon": "🚀",
        "title": "Long-Term Development Roadmap",
        "body": "Regardless of current standing, consistent marginal improvement compounds dramatically over a semester. Building one strong project portfolio, one research experience, and one professional certification (e.g., AWS Cloud, Google Data Analytics, or GitHub certifications) will differentiate this student in the job market within 12 months."
    })

    return recs[:6]  # Cap at 6 for clean display


def _build_final_verdict(pred_label, conf, overall, prog_cap, innovation, gpa):
    conf_pct = round(conf * 100, 1)

    if pred_label == "High" and overall >= 72:
        return {
            "verdict":    "STRONG ACADEMIC CANDIDATE",
            "color":      "#2D7A4F",
            "icon":       "🏆",
            "statement":  (
                f"This student presents a compelling academic and cognitive profile. With an ML-predicted "
                f"performance class of High (confidence: {conf_pct}%), a critical thinking index of {overall}%, "
                f"and a programming capability of {prog_cap}%, this individual demonstrates the exact combination "
                f"of analytical depth and technical aptitude sought by top universities and technology employers. "
                f"With continued momentum, this student is on a clear trajectory toward high-impact academic and "
                f"professional achievement."
            ),
            "tags": ["High Performer", "Research Ready", "Technically Capable", "Low Intervention Needed"],
        }
    elif pred_label == "Medium" or (pred_label == "High" and overall < 72):
        return {
            "verdict":    "DEVELOPING HIGH-POTENTIAL CANDIDATE",
            "color":      "#C4892A",
            "icon":       "📈",
            "statement":  (
                f"This student occupies the developing-potential tier — a position of real opportunity. "
                f"The ML model places them in the {pred_label} performance class (confidence: {conf_pct}%), "
                f"with a critical thinking score of {overall}% and a programming capability of {prog_cap}%. "
                f"The profile shows a student who is engaged but inconsistent. With a focused 6-week intervention "
                f"targeting the identified weak areas, a transition into the High performance class is realistic "
                f"and achievable. This student is worth investing in."
            ),
            "tags": ["Growth Potential", "Needs Structured Support", "Moderate Performer", "Engagement Required"],
        }
    else:
        return {
            "verdict":    "REQUIRES ACADEMIC INTERVENTION",
            "color":      "#B94040",
            "icon":       "⚠️",
            "statement":  (
                f"The current profile indicates a student at academic risk. ML prediction class: {pred_label} "
                f"(confidence: {conf_pct}%), critical thinking: {overall}%. The combination of lifestyle, "
                f"cognitive, and academic indicators suggests that without structured intervention, academic "
                f"performance is likely to decline further. An immediate review with academic counselling, "
                f"a customised study plan, and a 4-week intensive cognitive training programme is recommended. "
                f"Early action is the highest-ROI decision at this stage."
            ),
            "tags": ["Needs Intervention", "At-Risk Profile", "Structured Support Required", "Early Action Advised"],
        }


# ─── Weak Area Detector ───────────────────────────────────────────────────────
def detect_weak_areas(data: dict, logic: float, visual: float, prog: float) -> list:
    """
    Returns a list of dicts: {area, score, severity, action}
    sorted by severity descending.
    """
    areas = []

    def _add(area, score, threshold_red, threshold_yellow, action):
        if score < threshold_red:
            sev = "Critical"
            sc  = "#B94040"
        elif score < threshold_yellow:
            sev = "Moderate"
            sc  = "#C4892A"
        else:
            return  # Not a weak area
        areas.append({"area": area, "score": score, "severity": sev,
                      "color": sc, "action": action})

    _add("Logical Reasoning",   logic,
         40, 62,
         "Begin daily 15-min logic puzzle practice. Re-test in 3 weeks.")
    _add("Visual Intelligence", visual,
         40, 58,
         "Use diagram-based learning and spatial reasoning exercises.")
    _add("Programming Logic",   prog,
         40, 62,
         "Complete structured code-tracing exercises. 30-min daily practice.")

    sleep   = float(data.get("Sleep_Duration", 7))
    stress  = float(data.get("Stress_Level", 5))
    study   = float(data.get("Study_Hours_Per_Day", 4))
    attend  = float(data.get("Attendance_Rate", 0.85))
    memory  = float(data.get("Memory_Test_Score", 70))
    react   = float(data.get("Reaction_Time", 350))
    screen  = float(data.get("Daily_Screen_Time", 4))

    if sleep < 6.0:
        areas.append({"area": "Sleep Quality", "score": round(sleep/9*100),
                      "severity": "Critical", "color": "#B94040",
                      "action": "Achieve 7.5+ hrs immediately. Critical for memory consolidation."})
    elif sleep < 7.0:
        areas.append({"area": "Sleep Quality", "score": round(sleep/9*100),
                      "severity": "Moderate", "color": "#C4892A",
                      "action": "Aim for 7.5 hrs. Even 30 extra minutes improves cognition measurably."})

    if stress >= 7:
        areas.append({"area": "Stress Management", "score": round((10-stress)/10*100),
                      "severity": "Critical", "color": "#B94040",
                      "action": "Immediate stress-management intervention. Mindfulness + workload review."})
    elif stress >= 6:
        areas.append({"area": "Stress Management", "score": round((10-stress)/10*100),
                      "severity": "Moderate", "color": "#C4892A",
                      "action": "Introduce structured breaks. 10-min mindfulness daily."})

    if study < 3:
        areas.append({"area": "Study Consistency", "score": round(study/10*100),
                      "severity": "Critical", "color": "#B94040",
                      "action": "Redesign daily schedule. Target minimum 5 hrs structured study."})
    elif study < 4.5:
        areas.append({"area": "Study Consistency", "score": round(study/10*100),
                      "severity": "Moderate", "color": "#C4892A",
                      "action": "Increase study time by 1–1.5 hrs using time-blocking method."})

    if attend < 0.75:
        areas.append({"area": "Class Attendance", "score": round(attend*100),
                      "severity": "Critical", "color": "#B94040",
                      "action": "Attend every scheduled class. Knowledge gaps compound quickly."})
    elif attend < 0.85:
        areas.append({"area": "Class Attendance", "score": round(attend*100),
                      "severity": "Moderate", "color": "#C4892A",
                      "action": "Identify and address barriers to attendance. Target 90%+."})

    if memory < 55:
        areas.append({"area": "Memory & Retention", "score": round(memory),
                      "severity": "Critical" if memory < 40 else "Moderate",
                      "color": "#B94040" if memory < 40 else "#C4892A",
                      "action": "Adopt spaced repetition (Anki) for all course material. Review daily."})

    if screen > 8:
        areas.append({"area": "Digital Habits", "score": max(0, round((16-screen)/16*100)),
                      "severity": "Moderate", "color": "#C4892A",
                      "action": f"Reduce screen time from {screen} hrs. Set 2-hr daily entertainment limit."})

    # Sort: Critical first, then Moderate
    sev_order = {"Critical": 0, "Moderate": 1}
    areas.sort(key=lambda x: sev_order.get(x["severity"], 2))
    return areas
