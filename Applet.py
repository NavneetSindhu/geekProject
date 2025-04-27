# Applet.py
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
import tensorflow as tf

# Initialize Flask app
app = Flask(__name__)

# Load the model
MODEL_PATH = 'Skin_Diseases (2).h5'
model = load_model(MODEL_PATH)

# Setup graph (for older TensorFlow versions)
global graph
graph = tf.compat.v1.get_default_graph()

# Disease Labels
disease_info = {
    'Acne': {
        'advice': "Maintain a regular skincare routine. Avoid oily products and consult a dermatologist if necessary."
    },
    'Melanoma': {
        'advice': "Melanoma is serious. Seek immediate medical consultation for biopsy and treatment."
    },
    'Psoriasis': {
        'advice': "Use moisturizers, avoid triggers, and consult a dermatologist for treatment options."
    },
    'Rosacea': {
        'advice': "Avoid spicy foods, alcohol, and extreme temperatures. Consult a dermatologist."
    },
    'Vitiligo': {
        'advice': "Use sunscreen regularly and consult a dermatologist for therapies."
    }
}

@app.route('/', methods=['GET'])
def index():
    return render_template('templates/index.html')

@app.route('/predict', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    basepath = os.path.dirname(__file__)
    uploads_dir = os.path.join(basepath, 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, secure_filename(f.filename))
    f.save(file_path)

    # Prepare image
    img = image.load_img(file_path, target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    with graph.as_default():
        preds = model.predict(x)
        pred_idx = np.argmax(preds[0])
        confidence = float(np.max(preds[0])) * 100

    # Disease names
    labels = ['Acne', 'Melanoma', 'Psoriasis', 'Rosacea', 'Vitiligo']
    predicted_disease = labels[pred_idx]
    advice = disease_info[predicted_disease]['advice']

    return jsonify({
        'disease': predicted_disease,
        'confidence': f"{confidence:.2f}",
        'advice': advice
    })

if __name__ == '__main__':
    app.run(debug=False, threaded=False)
