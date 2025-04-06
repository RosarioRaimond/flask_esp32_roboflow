# ESP32-CAM Flask Server with Roboflow Integration

This Flask server receives an image from the ESP32-CAM, uploads it to freeimage.host, sends the image URL to Roboflow, and returns the inference result.

## Setup

1. Replace `YOUR_MODEL`, `YOUR_API_KEY`, and `YOUR_FREEIMAGE_API_KEY` in `app.py`.
2. Install dependencies: `pip install -r requirements.txt`
3. Run locally: `python app.py`

## Deployment (Render)

1. Push to GitHub.
2. Create a new Web Service on Render.
3. Use `gunicorn` as the web command: `gunicorn app:app`.