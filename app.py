from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import cv2
import numpy as np
import requests
from PIL import Image
import io
import base64
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

class ContentAnalyzer:
    def __init__(self):
        # Initialize with some pre-trained models (in production, use actual ML models)
        self.violence_keywords = [
            'kill', 'murder', 'blood', 'gun', 'weapon', 'violence', 'fight',
            'attack', 'horror', 'terror', 'scary', 'ghost', 'demon', 'zombie'
        ]
        
        self.age_limits = {
            'G': {'min_age': 0, 'max_age': 100, 'description': 'General Audience'},
            'PG': {'min_age': 7, 'max_age': 100, 'description': 'Parental Guidance'},
            'PG-13': {'min_age': 13, 'max_age': 100, 'description': 'Parents Strongly Cautioned'},
            'R': {'min_age': 17, 'max_age': 100, 'description': 'Restricted'},
            'NC-17': {'min_age': 18, 'max_age': 100, 'description': 'Adults Only'}
        }
    
    def analyze_video_content(self, video_data=None, video_url=None, metadata=None):
        """
        Analyze video content for harmful elements
        In production, this would use computer vision and NLP models
        """
        
        # Simulate analysis (replace with actual ML models)
        violence_score = self._simulate_violence_detection(video_data, metadata)
        horror_score = self._simulate_horror_detection(video_data, metadata)
        language_score = self._simulate_language_analysis(metadata)
        
        # Calculate overall harmful content percentage
        harmful_percentage = (violence_score + horror_score + language_score) / 3
        
        # Determine age limit
        age_limit = self._determine_age_limit(harmful_percentage, violence_score, horror_score)
        
        return {
            'harmful_percentage': round(harmful_percentage, 2),
            'age_limit': age_limit,
            'age_description': self.age_limits[age_limit]['description'],
            'min_age': self.age_limits[age_limit]['min_age'],
            'breakdown': {
                'violence': round(violence_score, 2),
                'horror': round(horror_score, 2),
                'language': round(language_score, 2)
            },
            'warnings': self._generate_warnings(violence_score, horror_score, language_score),
            'timestamp': datetime.now().isoformat()
        }
    
    def _simulate_violence_detection(self, video_data, metadata):
        """Simulate violence detection (replace with actual CV model)"""
        # In production, use OpenCV and ML models to analyze frames
        return np.random.uniform(0, 100)
    
    def _simulate_horror_detection(self, video_data, metadata):
        """Simulate horror content detection"""
        return np.random.uniform(0, 100)
    
    def _simulate_language_analysis(self, metadata):
        """Simulate inappropriate language detection"""
        if metadata and 'title' in metadata:
            title_lower = metadata['title'].lower()
            for keyword in self.violence_keywords:
                if keyword in title_lower:
                    return min(100, 30 + np.random.uniform(0, 70))
        return np.random.uniform(0, 50)
    
    def _determine_age_limit(self, harmful_percentage, violence_score, horror_score):
        """Determine appropriate age limit based on content analysis"""
        if harmful_percentage < 20:
            return 'G'
        elif harmful_percentage < 40:
            return 'PG'
        elif harmful_percentage < 60:
            return 'PG-13'
        elif harmful_percentage < 80:
            return 'R'
        else:
            return 'NC-17'
    
    def _generate_warnings(self, violence, horror, language):
        """Generate content warnings based on analysis"""
        warnings = []
        
        if violence > 70:
            warnings.append("High violence content")
        elif violence > 40:
            warnings.append("Moderate violence")
            
        if horror > 70:
            warnings.append("Intense horror scenes")
        elif horror > 40:
            warnings.append("Mild horror elements")
            
        if language > 60:
            warnings.append("Strong language")
            
        return warnings if warnings else ["Generally safe content"]

# Initialize analyzer
analyzer = ContentAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_content():
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract video data (in production, handle actual video processing)
        video_url = data.get('video_url')
        video_data = data.get('video_data')  # Base64 encoded video
        metadata = data.get('metadata', {})
        
        # Perform content analysis
        analysis_result = analyzer.analyze_video_content(
            video_data=video_data,
            video_url=video_url,
            metadata=metadata
        )
        
        return jsonify({
            'success': True,
            'analysis': analysis_result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analyze-youtube', methods=['POST'])
def analyze_youtube():
    try:
        data = request.json
        youtube_url = data.get('youtube_url')
        
        if not youtube_url:
            return jsonify({'error': 'YouTube URL required'}), 400
        
        # In production, use YouTube API to get video metadata
        # For demo, we'll simulate analysis
        metadata = {
            'title': 'Sample Horror Video',
            'description': 'A scary movie trailer with intense scenes',
            'duration': '2:30'
        }
        
        analysis_result = analyzer.analyze_video_content(
            video_url=youtube_url,
            metadata=metadata
        )
        
        return jsonify({
            'success': True,
            'metadata': metadata,
            'analysis': analysis_result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
