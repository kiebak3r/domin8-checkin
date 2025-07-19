import sqlite3
from datetime import datetime, timedelta
from PIL import Image
from constants import *


# Initialise the database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create Users Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            subscription_type TEXT
        )
    """)

    # Create Subscriptions Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_type TEXT PRIMARY KEY,
            max_entries_per_week INTEGER
        )
    """)

    # Create Attendance Log Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS attendance_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            timestamp TEXT
        )
    """)

    # Commit and close Connection
    conn.commit()
    conn.close()


# Save Logo
def save_image(flip: bool, filename: str):
    img = Image.open(LOGO).convert("RGBA")
    if flip:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(filename)


# Get Start of Week
def get_week_start():
    today = datetime.now()
    start = today - timedelta(days=today.weekday())
    return start.replace(hour=0, minute=0, second=0, microsecond=0)


# Verify the Users Login Attempt
def verify_user(user_id):
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check Users Subscription
    c.execute("SELECT subscription_type, name FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    if not user:
        conn.close()
        return 2, (f"{WARN} User ID: {user_id}", "No Record of a User with this ID exists in the system.")
    subscription_type = user[0]
    name = user[1]

    # Check Users Max Entries per subscription
    c.execute("SELECT max_entries_per_week FROM subscriptions WHERE subscription_type = ?", (subscription_type,))
    max_entries = c.fetchone()[0]

    # Check Users Previous Attendance
    week_start = get_week_start().isoformat()
    c.execute("SELECT timestamp FROM attendance_log WHERE user_id = ? AND timestamp >= ?", (user_id, week_start))
    rows = c.fetchall()
    timestamps = [datetime.fromisoformat(row[0]) for row in rows]

    # Successful Entry
    if len(timestamps) < max_entries:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        c.execute("INSERT INTO attendance_log (user_id, timestamp) VALUES (?, ?)", (user_id, now))
        conn.commit()
        conn.close()
        return 0, (f"{VALID} Welcome Back {name}!", f"Attendance Logged at {now}")

    # Denied Entry
    else:
        conn.close()
        return 1, (
            f"{DENIED} Access denied for {name} (User ID: {user_id})",
            f"{subscription_type} Membership only allows access {max_entries} time(s) per week."
        )
