import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from inference_sdk import InferenceHTTPClient

app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Replace with your Render domain (NO trailing slash)
BASE_URL = "https://flask-esp32-roboflow.onrender.com"

# Roboflow client config
client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="tuTdlZTbWrN3FISzqHsE"
)

@app.route('/')
def home():
    return jsonify({"message": "Flask server is live"}), 200

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    image_file = request.files['file']
    if image_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save file with a unique name
    unique_filename = str(uuid.uuid4()) + ".jpg"
    save_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    image_file.save(save_path)

    # Create public URL
    image_url = f"{BASE_URL}/uploads/{unique_filename}"

    try:
        # Send to Roboflow custom workflow
        result = client.run_workflow(
            workspace_name="rosario-g9eqt",
            workflow_id="custom-workflow",
            images={"image": image_url},
            use_cache=True
        )

        return jsonify({
            "image_url": image_url,
            "roboflow_result": result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/uploads/<filename>')
def serve_uploaded_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
