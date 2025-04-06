import os
import uuid
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Replace with your actual Render domain
BASE_URL = 'https://flask-esp32-roboflow.onrender.com'

@app.route('/')
def home():
    return 'ESP32-CAM Flask-Roboflow Server'

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Build public image URL
    image_url = f"{BASE_URL}/{filepath}"

    # Send to Roboflow
    roboflow_url = "https://detect.roboflow.com/infer/workflows/rosario-g9eqt/custom-workflow"
    headers = {'Content-Type': 'application/json'}
    data = {
        "api_key": "tuTdlZTbWrN3FISzqHsE",  # Your Roboflow API key
        "inputs": {
            "image": {
                "type": "url",
                "value": image_url
            }
        }
    }

    response = requests.post(roboflow_url, json=data, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Roboflow request failed", "details": response.text}), 500

    return jsonify(response.json())
