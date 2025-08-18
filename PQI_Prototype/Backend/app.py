# from flask import Flask, jsonify, request
# import sqlite3
# from flask_cors import CORS
# from transformers import pipeline

# app = Flask(__name__)
# CORS(app)
# DB_PATH = "C:/Users/hp/Desktop/TCS AI Hackathon/database.db"

# sentiment_analyzer = pipeline("sentiment-analysis")
# keyphrase_extractor = pipeline("feature-extraction")

# def extract_key_phrases(text):
#     # Simple demo: take first 5 words
#     return text.split()[:5]

# def get_db_connection():
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row  # So we get dict-like rows
#     return conn

# # Root route
# @app.route("/")
# def home():
#     return {"message": "Hackathon API is running 🚀"}

# # Fetch all submissions
# @app.route("/submissions", methods=["GET"])
# def get_submissions():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM submissions")
#     rows = cursor.fetchall()
#     conn.close()

#     # Convert sqlite3.Row objects → dict
#     submissions = [dict(row) for row in rows]
#     return jsonify(submissions)

# # Add new submission
# @app.route("/submissions", methods=["POST"])
# def add_submission():
#     data = request.get_json()
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         INSERT INTO submissions (team_name, member_name, story_points, comments, customer_feedback, additional_info)
#         VALUES (?, ?, ?, ?, ?, ?)
#     """, (
#         data.get("team_name"),
#         data.get("member_name"),
#         data.get("story_points"),
#         data.get("comments"),
#         data.get("customer_feedback"),
#         data.get("additional_info")
#     ))

#     conn.commit()
#     conn.close()
#     return {"status": "success", "message": "Submission added successfully!"}, 201

# # AI Analysis endpoint
# @app.route("/ai/analyze", methods=["POST"])
# def analyze_submission():
#     data = request.get_json()
#     comments = data.get("comments", "")
#     customer_feedback = data.get("customer_feedback", "")

#     # Sentiment analysis
#     comments_sentiment = sentiment_analyzer(comments)[0]
#     customer_sentiment = sentiment_analyzer(customer_feedback)[0]

#     # Key phrases
#     key_phrases = extract_key_phrases(comments)

#     return jsonify({
#         "comments_sentiment": comments_sentiment,
#         "customer_sentiment": customer_sentiment,
#         "key_phrases": key_phrases
#     })

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from transformers import pipeline
from keybert import KeyBERT
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = Flask(__name__)
CORS(app)

DB_PATH = "C:/Users/hp/Desktop/TCS AI Hackathon/database.db"

# Initialize AI models
sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
kw_model = KeyBERT()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Root route
@app.route("/")
def home():
    return {"message": "Hackathon API running 🚀"}

# Get all submissions
@app.route("/submissions", methods=["GET"])
def get_submissions():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM submissions").fetchall()
    conn.close()
    submissions = [dict(row) for row in rows]
    return jsonify(submissions)

# Add new submission
@app.route("/submissions", methods=["POST"])
def add_submission():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO submissions (team_name, member_name, story_points, comments, customer_feedback, additional_info)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.get("team_name"),
        data.get("member_name"),
        data.get("story_points"),
        data.get("comments"),
        data.get("customer_feedback"),
        data.get("additional_info")
    ))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Submission added successfully!"}, 201

# AI analysis endpoint
@app.route("/ai/analyze", methods=["POST"])
def analyze_text():
    data = request.get_json()
    comments = data.get("comments", "")
    feedback = data.get("customer_feedback", "")

    # Sentiment analysis
    # comments_sent = sentiment_model(comments)[0]
    # feedback_sent = sentiment_model(feedback)[0]
    # Get star rating (1-5)
    comments_star = sentiment_model(comments)[0]["label"]  # e.g., "4 stars"
    feedback_star = sentiment_model(feedback)[0]["label"]

    # Extract numeric value
    comments_score = int(comments_star.split()[0])
    feedback_score = int(feedback_star.split()[0])

    # Key phrases
    key_phrases = kw_model.extract_keywords(comments, top_n=5)
    key_phrases = [k[0] for k in key_phrases]

    return jsonify({
        "comments_star": comments_score,
        "customer_star": feedback_score,
        "key_phrases": key_phrases
    })

# AI recommendations endpoint
@app.route("/ai/recommendations", methods=["GET"])
def recommendations():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM submissions").fetchall()
    conn.close()

    recs = []

    for row in rows:
        # Use story points and AI stars
        comments = row["comments"]
        feedback = row["customer_feedback"]
        story_points = row["story_points"]

        ai_result = analyze_submission_text(comments, feedback)

        # Simple rules for demo
        if ai_result["comments_star"] <= 2 or story_points < 5:
            recs.append(f"⚠️ {row['member_name']} ({row['team_name']}) may need mentoring or support.")
        elif ai_result["comments_star"] >= 4 and story_points >= 8:
            recs.append(f"✅ {row['member_name']} ({row['team_name']}) exceeded expectations. Consider leadership opportunities.")

    return jsonify({"recommendations": recs})

# Helper to call existing AI analyze_text function
def analyze_submission_text(comments, feedback):
    result = sentiment_model(comments)[0]
    comments_star = int(result["label"].split()[0])
    feedback_star = int(sentiment_model(feedback)[0]["label"].split()[0])

    key_phrases = kw_model.extract_keywords(comments, top_n=5)
    key_phrases = [k[0] for k in key_phrases]

    return {"comments_star": comments_star, "customer_star": feedback_star, "key_phrases": key_phrases}

@app.route("/ai/team-insights", methods=["GET"])
def team_insights():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM submissions").fetchall()
    conn.close()

    teams = {}
    
    for row in rows:
        team = row["team_name"]
        if team not in teams:
            teams[team] = {"story_points": [], "comments_star": [], "customer_star": [], "members": []}
        
        ai_result = analyze_submission_text(row["comments"], row["customer_feedback"])
        
        teams[team]["story_points"].append(row["story_points"])
        teams[team]["comments_star"].append(ai_result["comments_star"])
        teams[team]["customer_star"].append(ai_result["customer_star"])
        teams[team]["members"].append(row["member_name"])
    
    # Calculate averages
    team_summary = {}
    for team, vals in teams.items():
        avg_story = round(sum(vals["story_points"])/len(vals["story_points"]), 2)
        avg_comments_star = round(sum(vals["comments_star"])/len(vals["comments_star"]), 2)
        avg_customer_star = round(sum(vals["customer_star"])/len(vals["customer_star"]), 2)
        team_summary[team] = {
            "avg_story_points": avg_story,
            "avg_comments_star": avg_comments_star,
            "avg_customer_star": avg_customer_star,
            "members": vals["members"]
        }
    
    return jsonify(team_summary)



if __name__ == "__main__":
    app.run(debug=True)
