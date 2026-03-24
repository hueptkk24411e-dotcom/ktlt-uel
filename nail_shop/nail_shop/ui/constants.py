"""
File DUY NHẤT chứa tất cả biến dùng chung.
"""

# ══════════════════════════════════════════════════════════════════
# 1. BUTTON STYLES
# ══════════════════════════════════════════════════════════════════

STYLE_ACTION_BTN = """
    QPushButton {
        background-color: rgb(67, 139, 196);
        color: rgb(224, 253, 255);
        border: 2px solid rgb(170, 210, 250);
        border-radius: 10px;
        font-size: 12px;
        font-weight: bold;
        padding: 6px 10px;
    }
    QPushButton:hover    { background-color: #4E86B5; }
    QPushButton:pressed  { background-color: #3a6f99; }
    QPushButton:disabled { background-color: #aaa; color: #ddd; border-color: #bbb; }
"""

STYLE_PRODUCT_BTN = """
    QPushButton {
        background-color: rgb(167, 212, 238);
        color: rgb(0, 0, 127);
        border: 2px solid rgb(67, 139, 196);
        border-radius: 12px;
        font-size: 13px;
        font-weight: bold;
        font-family: "Georgia";
        padding: 6px 8px;
    }
    QPushButton:hover   { background-color: #A6C8FF; border: 2px solid #7FAFFF; color: white; }
    QPushButton:pressed { background-color: #7FAFFF; border: 2px solid #4A90E2; }
"""

# ══════════════════════════════════════════════════════════════════
# 2. STAR RATING — tên object name của 5 nút sao trong FeedbackWindow
# ══════════════════════════════════════════════════════════════════

STAR_BTN_NAMES = ["star_1", "star_2", "star_3", "star_4", "star_5"]

STAR_ON  = "QPushButton { background: transparent; color: gold; font-size: 35px; border: none; }"
STAR_OFF = "QPushButton { background: transparent; color: #333; font-size: 35px; border: none; }"

RATING_LABELS = {
    1: "😞  Poor",
    2: "😐  Fair",
    3: "🙂  Good",
    4: "😊  Very Good",
    5: "🤩  Excellent!",
}

# ══════════════════════════════════════════════════════════════════
# 3. COLOR PALETTE
# ══════════════════════════════════════════════════════════════════

COLOR_PALETTE = [
    ("color_1",  "#FF0000", "Red"),
    ("color_2",  "#FF1493", "Deep Pink"),
    ("color_3",  "#FFC0CB", "Pink"),
    ("color_4",  "#DB7093", "Pale Violet Red"),
    ("color_5",  "#800000", "Maroon"),
    ("color_6",  "#FFA500", "Orange"),
    ("color_7",  "#FFFF00", "Yellow"),
    ("color_8",  "#FFD700", "Gold"),
    ("color_9",  "#F4A460", "Sandy Brown"),
    ("color_10", "#E9967A", "Dark Salmon"),
    ("color_11", "#008000", "Green"),
    ("color_12", "#90EE90", "Light Green"),
    ("color_13", "#0000FF", "Blue"),
    ("color_14", "#ADD8E6", "Light Blue"),
    ("color_15", "#000080", "Navy"),
    ("color_16", "#800080", "Purple"),
    ("color_17", "#E6E6FA", "Lavender"),
    ("color_18", "#A52A2A", "Brown"),
    ("color_19", "#D2B48C", "Tan"),
    ("color_20", "#F5F5DC", "Beige"),
    ("color_21", "#000000", "Black"),
    ("color_22", "#FFFFFF", "White"),
    ("color_23", "#808080", "Gray"),
    ("color_24", "#C0C0C0", "Silver"),
    ("color_25", "#708090", "Slate Gray"),
]

