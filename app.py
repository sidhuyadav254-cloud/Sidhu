# backend/app.py
from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)
    harmful_frames, total_frames = 0, 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Simulate detection: Replace this with ML model inference
        if contains_harmful_content(frame):
            harmful_frames += 1
        total_frames += 1

    cap.release()
    percent_harmful = (harmful_frames / total_frames) * 100 if total_frames else 0
    age_limit = 18 if percent_harmful > 10 else 13 if percent_harmful > 0 else 0
    return percent_harmful, age_limit

def contains_harmful_content(frame):
    # ML model inference would go here.
    # For demo, randomly assign as non-harmful
    return False

@app.route('/analyze', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_path = "temp_video.mp4"
    file.save(file_path)
    percent_harmful, age_limit = analyze_video(file_path)
    return jsonify({
        "harmful_content_percent": percent_harmful,
        "suggested_age_limit": age_limit
    })

if __name__ == '__main__':
    app.run(debug=True)
