from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ROBOFLOW_API_URL = "https://detect.roboflow.com/rosario-g9eqt/1"
ROBOFLOW_API_KEY = "tuTdlZTbWrN3FISzqHsE"

def upload_to_free_image_host(image_file):
    response = requests.post(
        "https://freeimage.host/api/1/upload",
        data={"key": "YOUR_FREEIMAGE_API_KEY"},
        files={"source": image_file}
    )
    return response.json()["image"]["url"]

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    image_file = request.files['file']
    image_url = upload_to_free_image_host(image_file)

    roboflow_response = requests.post(
        f"{ROBOFLOW_API_URL}?api_key={ROBOFLOW_API_KEY}",
        json={"image": image_url}
    )

    return jsonify(roboflow_response.json())

if __name__ == '__main__':
    app.run(debug=True)