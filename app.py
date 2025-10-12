from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pytube import YouTube
import random
import os

app = Flask(__name__)
CORS(app)

VIDEO_PATH = "youtube_video.mp4"

@app.route("/analyze", methods=["POST"])
def analyze_youtube_video():
    data = request.get_json()
    url = data.get("url", "")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # Download YouTube video
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        stream.download(filename=VIDEO_PATH)
    except Exception as e:
        return jsonify({"error": f"Video download failed: {str(e)}"}), 500

    # Dummy harmful analysis logic
    title_lower = yt.title.lower()
    if "horror" in title_lower or "shorts" in url.lower():
        harmful_percentage = random.randint(60, 95)
        age_limit = "18+"
    else:
        harmful_percentage = random.randint(10, 50)
        age_limit = "13+"

    return jsonify({
        "harmful_percentage": harmful_percentage,
        "age_limit": age_limit,
        "video_url": f"http://127.0.0.1:5000/video"
    })

# Route to serve downloaded video
@app.route("/video")
def serve_video():
    if not os.path.exists(VIDEO_PATH):
        return "Video not found", 404
    return send_file(VIDEO_PATH, mimetype="video/mp4")

if __name__ == "__main__":
    app.run(debug=True)
