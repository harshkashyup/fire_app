from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
from detect_fire import detect_fire_from_image

app = Flask(__name__)

def readb64(base64_string):
    img_data = base64.b64decode(base64_string.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

def encode_image_to_base64(img):
    _, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer).decode()
    return f"data:image/jpeg;base64,{jpg_as_text}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400

    img_b64 = data['image']
    img = readb64(img_b64)

    fire_detected, fire_mask = detect_fire_from_image(img)
    fire_mask_b64 = encode_image_to_base64(fire_mask)

    return jsonify({
        'fire_detected': fire_detected,
        'fire_mask': fire_mask_b64
    })

if __name__ == '__main__':
    app.run(debug=True)
