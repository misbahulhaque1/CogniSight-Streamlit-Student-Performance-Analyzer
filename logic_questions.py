"""
logic_questions.py
==================
Logical reasoning question bank — 15 MCQs across pattern recognition,
analytical reasoning, deductive logic, and mathematical reasoning.
"""

LOGIC_QUESTIONS = [
    # ── Pattern Recognition ────────────────────────────────────────────────
    {
        "id": 1,
        "category": "🔵 Pattern Recognition",
        "question": "Find the next number: 2, 6, 12, 20, 30, __?",
        "options": ["40", "42", "44", "36"],
        "answer": "42",
        "explanation": "Differences are 4, 6, 8, 10, 12. So 30 + 12 = 42.",
    },
    {
        "id": 2,
        "category": "🔵 Pattern Recognition",
        "question": "Which letter comes next?  A, C, F, J, O, __?",
        "options": ["T", "U", "V", "S"],
        "answer": "U",
        "explanation": "Gaps increase: +2, +3, +4, +5, +6. O is position 15, +6 = position 21 = U.",
    },
    {
        "id": 3,
        "category": "🔵 Pattern Recognition",
        "question": "Next term in: 1, 4, 9, 16, 25, __?",
        "options": ["30", "35", "36", "49"],
        "answer": "36",
        "explanation": "Perfect squares: 1², 2², 3², 4², 5², 6² = 36.",
    },
    {
        "id": 4,
        "category": "🔵 Pattern Recognition",
        "question": "Series: 3, 6, 11, 18, 27, __?",
        "options": ["36", "38", "40", "38"],
        "answer": "38",
        "explanation": "Differences: 3, 5, 7, 9, 11. So 27 + 11 = 38.",
    },
    # ── Analytical Reasoning ───────────────────────────────────────────────
    {
        "id": 5,
        "category": "🟢 Analytical Reasoning",
        "question": (
            "Five students scored: Ali=70, Sara=85, Ravi=90, Mia=78, Tom=65. "
            "Who scored third highest?"
        ),
        "options": ["Ali", "Sara", "Ravi", "Mia"],
        "answer": "Mia",
        "explanation": "Ranking: Ravi(90) > Sara(85) > Mia(78) > Ali(70) > Tom(65). Third = Mia(78).",
    },
    {
        "id": 6,
        "category": "🟢 Analytical Reasoning",
        "question": (
            "A class of 40: 60% passed Math, 50% passed Science, 20% passed both. "
            "How many passed at least one subject?"
        ),
        "options": ["35", "36", "32", "28"],
        "answer": "36",
        "explanation": "Union = 60% + 50% − 20% = 90% of 40 = 36.",
    },
    {
        "id": 7,
        "category": "🟢 Analytical Reasoning",
        "question": (
            "In a race, Ahmed finishes before Bilal. Bilal finishes before Carla. "
            "Which statement is definitely true?"
        ),
        "options": [
            "Carla finished first",
            "Ahmed finished first",
            "Bilal finished last",
            "Ahmed finished before Carla",
        ],
        "answer": "Ahmed finished before Carla",
        "explanation": "Ahmed > Bilal > Carla transitively means Ahmed is ahead of Carla.",
    },
    # ── Logical Deduction ──────────────────────────────────────────────────
    {
        "id": 8,
        "category": "🟡 Logical Deduction",
        "question": (
            "All students who study > 6 h/day pass the exam. "
            "Ahmed studies 7 h/day. Conclusion?"
        ),
        "options": [
            "Ahmed may or may not pass",
            "Ahmed will definitely pass",
            "Ahmed will fail",
            "No conclusion possible",
        ],
        "answer": "Ahmed will definitely pass",
        "explanation": "Modus ponens: condition satisfied → conclusion follows.",
    },
    {
        "id": 9,
        "category": "🟡 Logical Deduction",
        "question": (
            "No high-stress student sleeps more than 6 h. "
            "Sara sleeps 8 h. Which is valid?"
        ),
        "options": [
            "Sara is high-stress",
            "Sara is not high-stress",
            "Sara studies a lot",
            "Cannot determine",
        ],
        "answer": "Sara is not high-stress",
        "explanation": "Contrapositive: if high-stress → ≤6 h sleep, then 8 h sleep → not high-stress.",
    },
    {
        "id": 10,
        "category": "🟡 Logical Deduction",
        "question": (
            "If it rains, the match is cancelled. The match was NOT cancelled. "
            "What can we conclude?"
        ),
        "options": [
            "It rained",
            "It did not rain",
            "The match was rescheduled",
            "Nothing",
        ],
        "answer": "It did not rain",
        "explanation": "Contrapositive of 'rain → cancel' is 'not cancel → not rain'.",
    },
    # ── Quantitative Reasoning ─────────────────────────────────────────────
    {
        "id": 11,
        "category": "🔴 Quantitative Reasoning",
        "question": "A train travels 240 km in 3 h. How long for 400 km at the same speed?",
        "options": ["4 h", "5 h", "4.5 h", "6 h"],
        "answer": "5 h",
        "explanation": "Speed = 80 km/h. Time = 400 ÷ 80 = 5 h.",
    },
    {
        "id": 12,
        "category": "🔴 Quantitative Reasoning",
        "question": "If 5 workers complete a job in 12 days, how many days do 10 workers need?",
        "options": ["24", "6", "8", "10"],
        "answer": "6",
        "explanation": "Inverse proportion: 5 × 12 = 10 × d → d = 6.",
    },
    # ── Critical Thinking ──────────────────────────────────────────────────
    {
        "id": 13,
        "category": "🟣 Critical Thinking",
        "question": (
            "A study shows students who drink coffee score higher on tests. "
            "What is the BEST conclusion?"
        ),
        "options": [
            "Coffee causes better test scores",
            "Coffee and test scores are correlated, but causation is unproven",
            "All students should drink coffee",
            "Students who score well drink coffee",
        ],
        "answer": "Coffee and test scores are correlated, but causation is unproven",
        "explanation": "Correlation ≠ causation. A confounding factor (study habits) could explain both.",
    },
    {
        "id": 14,
        "category": "🟣 Critical Thinking",
        "question": (
            "Only seniors can enter Room A. Zara is in Room A. "
            "Which must be true?"
        ),
        "options": [
            "Zara is a junior",
            "Zara is a senior",
            "All seniors are in Room A",
            "Nothing can be concluded",
        ],
        "answer": "Zara is a senior",
        "explanation": "Only seniors → Room A; Zara is in Room A → Zara is a senior (modus ponens reverse).",
    },
    {
        "id": 15,
        "category": "🟣 Critical Thinking",
        "question": (
            "Team A won more matches than Team B. Team B won more than Team C. "
            "Team C won at least one match. Which is definitely true?"
        ),
        "options": [
            "Team A won at least 2 matches",
            "Team C won more than Team A",
            "Team B won zero matches",
            "Team A won the fewest matches",
        ],
        "answer": "Team A won at least 2 matches",
        "explanation": "C ≥ 1, B > C → B ≥ 2, A > B → A ≥ 3 ≥ 2. So A won at least 2 matches.",
    },
]
