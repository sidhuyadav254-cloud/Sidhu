from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze_video():
    data = request.get_json()
    url = data.get("url", "")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Dummy analysis
    if "shorts" in url.lower():
        harmful_percentage = random.randint(60, 95)
        age_limit = "18+"
    else:
        harmful_percentage = random.randint(10, 50)
        age_limit = "13+"

    # Extract YouTube embed URL
    embed_url = url.replace("https://youtube.com/shorts/", "https://www.youtube.com/embed/")
    embed_url = embed_url.split("?")[0]  # remove extra params

    return jsonify({
        "harmful_percentage": harmful_percentage,
        "age_limit": age_limit,
        "embed_url": embed_url
    })

if __name__ == "__main__":
    app.run(debug=True)
