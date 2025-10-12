from flask import Flask, request, jsonify
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
        # Download video from YouTube
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        stream.download(filename=VIDEO_PATH)
    except Exception as e:
        return jsonify({"error": f"Video download failed: {str(e)}"}), 500

    # Dummy analysis logic (replace with AI/video moderation later)
    if "shorts" in url.lower() or "horror" in yt.title.lower():
        harmful_percentage = random.randint(60, 95)
        age_limit = "18+"
    else:
        harmful_percentage = random.randint(10, 50)
        age_limit = "13+"

    return jsonify({
        "harmful_percentage": harmful_percentage,
        "age_limit": age_limit,
        "video_file": VIDEO_PATH
    })


if __name__ == "__main__":
    app.run(debug=True)
