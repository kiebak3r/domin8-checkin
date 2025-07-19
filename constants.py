import os

# Emojis
INVALID = '❌'
VALID = '✅'
WARN = '⚠️'
DENIED = '🚫'

# Paths
base_dir = os.path.abspath(os.path.dirname(__file__))
LOGO = os.path.join(base_dir, "Assets", "imgs", "domin8-Logo.png")
BACKGROUND = os.path.join(base_dir, "Assets", "imgs", "domin8-bg.jpg")
normal_path = os.path.join(base_dir, "Assets", "imgs", "normal.png")
flipped_path = os.path.join(base_dir, "Assets", "imgs", "flipped.png")

# Variables
TITLE = "CHECK IN"
INPUT_LABEL = "Enter User ID"
INPUT_EMPTY_ERROR = f"{WARN} Please enter a valid User ID"
