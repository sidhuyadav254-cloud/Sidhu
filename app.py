from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import random
import os
import yt_dlp

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
        # Download YouTube Shorts as MP4 using yt-dlp
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': VIDEO_PATH,
            'noplaylist': True,
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return jsonify({"error": f"Video download failed: {str(e)}"}), 500

    # Dummy harmful % logic
    harmful_percentage = random.randint(60, 95) if "shorts" in url.lower() else random.randint(10, 50)
    age_limit = "18+" if harmful_percentage > 50 else "13+"

    return jsonify({
        "harmful_percentage": harmful_percentage,
        "age_limit": age_limit,
        "video_url": f"http://127.0.0.1:5000/video"
    })

@app.route("/video")
def serve_video():
    if not os.path.exists(VIDEO_PATH):
        return "Video not found", 404
    return send_file(VIDEO_PATH, mimetype="video/mp4")

if __name__ == "__main__":
    app.run(debug=True)
