import sqlite3

# Always create DB in project root (../database.db from backend/)
conn = sqlite3.connect("../database.db")
cursor = conn.cursor()

# Create submissions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT,
    member_name TEXT,
    story_points INTEGER,
    comments TEXT,
    customer_feedback TEXT,
    additional_info TEXT
);
""")

conn.commit()
conn.close()
print("Database initialized with submissions table!")
