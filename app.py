import os
import requests
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'
ROBOFLOW_API_KEY = os.getenv("tuTdlZTbWrN3FISzqHsE")
ROBOFLOW_MODEL_ENDPOINT = os.getenv("https://detect.roboflow.com/rosario-g9eqt/1")  # e.g., "https://detect.roboflow.com/your-model/1"

@app.route('/')
def home():
    return "ESP32-CAM Flask Server is Running!"

@app.route('/upload', methods=['POST'])
def upload():
    image_file = request.files.get("file")

    if not image_file:
        return jsonify({"error": "No file uploaded"}), 400

    # Save image to /tmp/
    filename = secure_filename(image_file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image_file.save(filepath)

    # Upload to Roboflow using the local file
    with open(filepath, "rb") as f:
        response = requests.post(
            ROBOFLOW_MODEL_ENDPOINT,
            params={"api_key": ROBOFLOW_API_KEY},
            files={"file": f},
        )

    try:
        result = response.json()
    except Exception as e:
        result = {"error": "Failed to parse Roboflow response", "details": str(e)}

    # Optionally delete the file
    os.remove(filepath)

    return jsonify(result)
