"""
programming_questions.py
========================
Programming logic MCQ bank — output prediction, control flow, data structures.
12 questions of increasing complexity.
"""

PROGRAMMING_QUESTIONS = [
    # ── Loop Output ────────────────────────────────────────────────────────
    {
        "id": 1,
        "category": "🔁 Loop Output",
        "question": "What is printed?\n\nfor i in range(3):\n    print(i)",
        "options": ["1 2 3", "0 1 2", "0 1 2 3", "Error"],
        "answer": "0 1 2",
        "explanation": "range(3) yields 0, 1, 2 — three values starting at zero.",
    },
    {
        "id": 2,
        "category": "🔁 Loop Output",
        "question": "What does this print?\n\ncount = 0\nfor i in range(2):\n    for j in range(3):\n        count += 1\nprint(count)",
        "options": ["2", "3", "5", "6"],
        "answer": "6",
        "explanation": "Nested loops: 2 outer × 3 inner = 6 iterations.",
    },
    {
        "id": 3,
        "category": "🔁 Loop Output",
        "question": "What does this print?\n\nx = 0\nwhile x < 4:\n    x += 2\nprint(x)",
        "options": ["2", "3", "4", "5"],
        "answer": "4",
        "explanation": "x starts at 0, increments by 2 each iteration. Stops at x=4 (not < 4).",
    },
    # ── Condition Logic ────────────────────────────────────────────────────
    {
        "id": 4,
        "category": "🔀 Condition Logic",
        "question": "What is printed?\n\nx = 10\nif x < 5:\n    print('L')\nelif x < 10:\n    print('M')\nelse:\n    print('H')",
        "options": ["L", "M", "H", "No output"],
        "answer": "H",
        "explanation": "x=10 fails both conditions, so the else block prints 'H'.",
    },
    {
        "id": 5,
        "category": "🔀 Condition Logic",
        "question": "Output of:\n\nprint(True and False or True)",
        "options": ["True", "False", "Error", "None"],
        "answer": "True",
        "explanation": "(True and False) = False; (False or True) = True.",
    },
    {
        "id": 6,
        "category": "🔀 Condition Logic",
        "question": "What prints?\n\na = 5\nb = 10\nif a > 3 and b < 20:\n    print('Yes')\nelse:\n    print('No')",
        "options": ["Yes", "No", "Error", "Nothing"],
        "answer": "Yes",
        "explanation": "a > 3 is True AND b < 20 is True → both True → 'Yes'.",
    },
    # ── Arithmetic & Expressions ───────────────────────────────────────────
    {
        "id": 7,
        "category": "🔢 Arithmetic",
        "question": "Result of:\n\na = 2\nb = 3\nprint(a ** b + b % 2)",
        "options": ["8", "9", "10", "11"],
        "answer": "9",
        "explanation": "2**3 = 8; 3 % 2 = 1; 8 + 1 = 9.",
    },
    {
        "id": 8,
        "category": "🔢 Arithmetic",
        "question": "What is the output?\n\nprint(10 // 3)",
        "options": ["3", "3.33", "4", "1"],
        "answer": "3",
        "explanation": "Floor division 10 // 3 = 3 (integer part only).",
    },
    # ── Data Structures ────────────────────────────────────────────────────
    {
        "id": 9,
        "category": "📋 Data Structures",
        "question": "What prints?\n\narr = [10, 20, 30, 40]\nprint(arr[-1])",
        "options": ["10", "30", "40", "Error"],
        "answer": "40",
        "explanation": "Negative indexing: arr[-1] accesses the last element.",
    },
    {
        "id": 10,
        "category": "📋 Data Structures",
        "question": "What is the output?\n\nd = {'a': 1, 'b': 2}\nprint(d.get('c', 0))",
        "options": ["1", "2", "0", "Error"],
        "answer": "0",
        "explanation": "dict.get(key, default) returns default when key is missing.",
    },
    # ── Functions ──────────────────────────────────────────────────────────
    {
        "id": 11,
        "category": "⚙️ Functions",
        "question": "What does this print?\n\ndef square(n):\n    return n * n\nprint(square(4) - square(2))",
        "options": ["8", "12", "14", "16"],
        "answer": "12",
        "explanation": "square(4) = 16, square(2) = 4; 16 − 4 = 12.",
    },
    {
        "id": 12,
        "category": "⚙️ Functions",
        "question": "What is printed?\n\ndef f(x, y=5):\n    return x + y\nprint(f(3))",
        "options": ["3", "5", "8", "Error"],
        "answer": "8",
        "explanation": "f(3) uses default y=5; 3 + 5 = 8.",
    },
]
