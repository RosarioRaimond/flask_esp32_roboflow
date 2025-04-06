import os
from flask import Flask, request, jsonify
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ROBOFLOW_API_KEY = "tuTdlZTbWrN3FISzqHsE"
WORKFLOW_URL = "https://detect.roboflow.com/infer/workflows/rosario-g9eqt/custom-workflow"

@app.route('/')
def home():
    return "Flask + 0x0.st + Roboflow app is running."

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    image_file = request.files['file']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save to local (optional but good for backup/debug)
    filename = secure_filename(image_file.filename)
    local_path = os.path.join(UPLOAD_FOLDER, filename)
    image_file.save(local_path)

    # Upload to 0x0.st
    with open(local_path, 'rb') as f:
        upload_response = requests.post("https://0x0.st", files={'file': f})
    if upload_response.status_code != 200:
        return jsonify({'error': 'Upload to 0x0.st failed'}), 500

    image_url = upload_response.text.strip()

    # Send image URL to Roboflow
    roboflow_payload = {
        "api_key": ROBOFLOW_API_KEY,
        "inputs": {
            "image": {"type": "url", "value": image_url}
        }
    }

    roboflow_response = requests.post(
        WORKFLOW_URL,
        headers={'Content-Type': 'application/json'},
        json=roboflow_payload
    )

    if roboflow_response.status_code != 200:
        return jsonify({'error': 'Roboflow failed', 'details': roboflow_response.text}), 500

    return roboflow_response.json()


if __name__ == '__main__':
    app.run(debug=True)
