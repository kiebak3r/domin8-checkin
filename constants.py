import os

# Emojis
INVALID = '❌'
VALID = '✅'
WARN = '⚠️'
DENIED = '🚫'

# Paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOGO = os.path.join(BASE_DIR, "Assets", "imgs", "domin8-Logo.png")
BACKGROUND = os.path.join(BASE_DIR, "Assets", "imgs", "domin8-bg.jpg")
normal_path = os.path.join(BASE_DIR, "Assets", "imgs", "normal.png")
flipped_path = os.path.join(BASE_DIR, "Assets", "imgs", "flipped.png")

# Variables
DB_PATH = "Assets/domin8.db"
TITLE = "CHECK IN"
INPUT_LABEL = "Enter User ID"
INPUT_EMPTY_ERROR = f"{WARN} Please enter a valid User ID"
