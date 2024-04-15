from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('models/covid_classifier_model.h5')

# Preprocess the uploaded image
def preprocess_image(image):
    # Resize the image to (200, 200)
    image = image.resize((200, 200))
    # Convert the image to a numpy array
    image_array = np.array(image) / 255.0  # Normalize pixel values to [0, 1]
    # Add color channel dimension
    image_array = np.expand_dims(image_array, axis=-1)
    # Stack the image along the color channel to make it RGB (3 channels)
    image_array = np.repeat(image_array, 3, axis=-1)
    # Expand dimensions to create a batch dimension
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        image = Image.open(file)
        image_array = preprocess_image(image)
        prediction = model.predict(image_array)
        result = 'COVID-19 Positive' if prediction[0][0] < 0.5 else 'COVID-19 Negative'
        print("Prediction Result:", result)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
