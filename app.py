from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import random
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None, None, "Cannot open video file"

    harmful_frames = 0
    analyzed_frames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        analyzed_frames += 1
        # Simulated harmful content detection: 10% chance frame is harmful
        if contains_harmful_content(frame):
            harmful_frames += 1

    cap.release()

    if analyzed_frames == 0:
        return None, None, "No frames processed from video"

    percent_harmful = (harmful_frames / analyzed_frames) * 100

    # Example age limit logic based on harmful content percentage
    if percent_harmful > 10:
        age_limit = 18
    elif percent_harmful > 0:
        age_limit = 13
    else:
        age_limit = 0  # Suitable for all ages

    return percent_harmful, age_limit, None

def contains_harmful_content(frame):
    # Demo function: randomly flag frames "harmful"
    return random.random() < 0.1  # 10% chance

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify(error="No file part in the request"), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    filename = "temp_uploaded_video.mp4"
    file.save(filename)

    percent_harmful, age_limit, error = analyze_video(filename)

    os.remove(filename)  # Clean up uploaded file

    if error:
        return jsonify(error=error), 500

    return jsonify(
        harmful_content_percent=round(percent_harmful, 2),
        suggested_age_limit=age_limit
    )

if __name__ == '__main__':
    app.run(debug=True)
