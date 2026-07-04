"""
visual_questions.py
===================
Visual intelligence MCQ bank: shape identification, cube counting,
spatial rotation, mirror images, and 3D reasoning — 12 questions.
"""

VISUAL_QUESTIONS = [
    # ── Shape Identification ───────────────────────────────────────────────
    {
        "id": 1,
        "category": "🔷 Shape Identification",
        "question": "Which polygon has exactly 5 sides?",
        "options": ["Hexagon", "Pentagon", "Quadrilateral", "Octagon"],
        "answer": "Pentagon",
        "explanation": "Pentagon = 5 sides (penta = five in Greek).",
    },
    {
        "id": 2,
        "category": "🔷 Shape Identification",
        "question": "Which shape has ALL points equidistant from its center?",
        "options": ["Rectangle", "Circle", "Rhombus", "Hexagon"],
        "answer": "Circle",
        "explanation": "By definition, all points on a circle are at radius distance from the centre.",
    },
    {
        "id": 3,
        "category": "🔷 Shape Identification",
        "question": (
            "A shape has 4 equal sides but no right angles. What is it?"
        ),
        "options": ["Square", "Rectangle", "Rhombus", "Trapezoid"],
        "answer": "Rhombus",
        "explanation": "A rhombus has 4 equal sides with angles that are not necessarily 90°.",
    },
    # ── 3D Objects & Faces ─────────────────────────────────────────────────
    {
        "id": 4,
        "category": "🧊 3D Objects",
        "question": "How many faces does a cube have?",
        "options": ["4", "5", "6", "8"],
        "answer": "6",
        "explanation": "Cube: 6 square faces (top, bottom, front, back, left, right).",
    },
    {
        "id": 5,
        "category": "🧊 3D Objects",
        "question": "Which 3D shape has ONE curved surface and TWO circular faces?",
        "options": ["Cone", "Cylinder", "Sphere", "Cube"],
        "answer": "Cylinder",
        "explanation": "Cylinder: two circular ends + one lateral curved surface.",
    },
    {
        "id": 6,
        "category": "🧊 3D Objects",
        "question": "How many edges does a triangular prism have?",
        "options": ["6", "9", "12", "8"],
        "answer": "9",
        "explanation": "Triangular prism: 3 edges per triangular face × 2 + 3 lateral edges = 9.",
    },
    # ── Cube Counting ──────────────────────────────────────────────────────
    {
        "id": 7,
        "category": "📦 Cube Counting",
        "question": "A 2×2×2 structure is built from unit cubes. How many unit cubes are used?",
        "options": ["6", "8", "10", "12"],
        "answer": "8",
        "explanation": "2 × 2 × 2 = 8 unit cubes.",
    },
    {
        "id": 8,
        "category": "📦 Cube Counting",
        "question": "One corner cube is removed from a 3×3×3 cube. How many remain?",
        "options": ["24", "25", "26", "27"],
        "answer": "26",
        "explanation": "3 × 3 × 3 = 27; remove 1 corner = 26.",
    },
    {
        "id": 9,
        "category": "📦 Cube Counting",
        "question": (
            "In a 3×3×3 cube, how many unit cubes have exactly ONE face painted "
            "(if the entire outer surface is painted)?"
        ),
        "options": ["6", "8", "12", "24"],
        "answer": "6",
        "explanation": "Face-centre cubes (not on any edge): 6 faces × 1 centre cube each = 6.",
    },
    # ── Spatial Rotation & Mirror ──────────────────────────────────────────
    {
        "id": 10,
        "category": "🔄 Spatial Rotation",
        "question": "After rotating a square 90°, its shape appears as?",
        "options": ["Rectangle", "Triangle", "Square", "Circle"],
        "answer": "Square",
        "explanation": "Rotation preserves shape and dimensions.",
    },
    {
        "id": 11,
        "category": "🪞 Mirror Images",
        "question": "The vertical mirror image of the letter 'b' looks like?",
        "options": ["b", "d", "p", "q"],
        "answer": "d",
        "explanation": "A vertical mirror flips left-right: 'b' becomes 'd'.",
    },
    # ── Pattern Shapes ─────────────────────────────────────────────────────
    {
        "id": 12,
        "category": "🔵 Pattern Shapes",
        "question": "Shape sequence: triangle → square → pentagon → __?",
        "options": ["Hexagon", "Circle", "Octagon", "Rectangle"],
        "answer": "Hexagon",
        "explanation": "Sides increase by 1 each step: 3 → 4 → 5 → 6 (hexagon).",
    },
]
