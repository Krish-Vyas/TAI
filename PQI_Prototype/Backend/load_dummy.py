import sqlite3

conn = sqlite3.connect("C:/Users/hp/Desktop/TCS AI Hackathon/database.db")
cursor = conn.cursor()

dummy_data = [
    ("Team Alpha", "Alice", 8, "Completed sprint tasks", "Good progress", "No blockers"),
    ("Team Alpha", "Bob", 5, "Needs support on API", "Delay noticed", "Pending API fixes"),
    ("Team Beta", "Charlie", 13, "Delivered ahead of time", "Excellent work", "Consider for leadership role"),
    ("Team Beta", "David", 3, "Struggled with testing", "Customer concerned", "Needs mentoring"),
    ("Team Gamma", "Eve", 8, "Stable sprint performance", "Neutral feedback", "Documentation improvements"),
    ("Team Gamma", "Frank", 10, "Handled integration issues well", "Good progress", "Requires more resources"),
    ("Team Delta", "Grace", 6, "Partial completion", "Mixed feedback", "Time management issue"),
    ("Team Delta", "Heidi", 9, "Resolved critical bug", "Customer happy", "Strong debugging skills"),
    ("Team Epsilon", "Ivan", 11, "Took extra ownership", "Very positive", "Can mentor juniors"),
    ("Team Epsilon", "Judy", 7, "Consistent performance", "Good progress", "Keep same momentum"),
]

cursor.executemany("""
INSERT INTO submissions (team_name, member_name, story_points, comments, customer_feedback, additional_info)
VALUES (?, ?, ?, ?, ?, ?)
""", dummy_data)

conn.commit()

cursor.execute("SELECT * FROM submissions;")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
print("✅ Dummy data inserted successfully!")