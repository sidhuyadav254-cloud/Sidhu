from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_video():
    data = request.get_json()
    video_url = data.get("video_url")

    # Simulated harmful content detection (you can replace this with AI model)
    harmful_percent = random.randint(10, 95)

    # Define age limit based on harmful percent
    if harmful_percent < 30:
        age_limit = "All Ages"
        message = "Safe content"
    elif harmful_percent < 60:
        age_limit = "13+"
        message = "May contain mild disturbing scenes"
    elif harmful_percent < 85:
        age_limit = "16+"
        message = "Contains moderate violence or fear"
    else:
        age_limit = "18+"
        message = "Contains strong horror or violent content"

    return jsonify({
        "harmful_percent": harmful_percent,
        "age_limit": age_limit,
        "message": message
    })

if __name__ == '__main__':
    app.run(debug=True)
