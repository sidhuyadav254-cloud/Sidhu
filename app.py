from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Allow frontend to connect

@app.route("/analyze", methods=["POST"])
def analyze_video():
    data = request.get_json()
    video_url = data.get("url", "")

    # Simple logic — later replace with AI or moderation API
    if "horror" in video_url.lower():
        harmful_percentage = random.randint(70, 95)
        age_limit = "18+ (Horror/Violence)"
    elif "funny" in video_url.lower() or "cartoon" in video_url.lower():
        harmful_percentage = random.randint(5, 20)
        age_limit = "All Ages"
    else:
        harmful_percentage = random.randint(25, 60)
        age_limit = "13+ (Moderate)"

    return jsonify({
        "harmful_percentage": harmful_percentage,
        "age_limit": age_limit
    })

if __name__ == "__main__":
    app.run(debug=True)
