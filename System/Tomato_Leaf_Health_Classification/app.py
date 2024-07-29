import os
import cv2

from flask import Flask, request, url_for, render_template, redirect
from werkzeug.utils import secure_filename

import numpy as np
import pandas as pd

from tensorflow.keras.models import load_model

# disable scientific notation for clarity
np.set_printoptions(suppress=True)

PEOPLE_FOLDER = 'static/uploaded_images'
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

model = load_model("model.h5", compile=False)

class_names = ['Healthy_Leaf', 'Diseased_Leaf']

treatment = {
    'Healthy_Leaf': {
        "symptom": "Healthy tomato leaves typically exhibit vibrant green coloration with no visible signs of damage or discoloration. ",
        "organic_control": "To maintain leaf health organically, regular pruning of affected foliage and ensuring adequate spacing between plants to promote air circulation can help prevent disease. Alternatively, applying neem oil or a garlic-based spray can act as organic deterrents against pests and pathogens. ",
        "chemical_control": "For chemical control, fungicides containing chlorothalonil or copper-based compounds can effectively prevent fungal infections and maintain leaf health."
    },
    
    'Diseased_Leaf': {
        "symptom": "Diseased tomato leaves may show symptoms such as yellowing, browning, or spotting, indicating the presence of a fungal or bacterial infection.",
        "organic_control": "To combat disease organically, removing infected leaves promptly and ensuring proper sanitation practices in the garden can help prevent further spread. Additionally, applying a mixture of baking soda and water or a compost tea solution can help suppress fungal growth.",
        "chemical_control": "Chemical control involves using fungicides like maneb or captan, which effectively target fungal pathogens and halt the progression of disease on tomato leaves."
    }
}


def predict(img_bytes, model_):
    
    image = cv2.imread(img_bytes)
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1
    
    prediction = model_.predict(image)
    index_ = np.argmax(prediction)
    class_name = class_names[index_]
    confidence_score = prediction[0][index_]
    
    # Print prediction and confidence score
    # print("Class:", class_name[2:], end="")
    # print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
    
    return class_name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnose')
def diagnose():
    return render_template(
        'diagnose.html',
        full_filename="/static/images/display_image.png",
    )
    
@app.route('/predict', methods=['POST'])
def upload_file():
    uploaded_img = request.files['file']

    if len(uploaded_img.filename):
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploaded_img.filename))
        file_path= os.path.join('static/uploaded_images', secure_filename(uploaded_img.filename))
        uploaded_img.save(file_path)
        
        prediction_name = predict(file_path, model)
        
        symptom = treatment[prediction_name].get("symptom")
        organic_control = treatment[prediction_name].get("organic_control")
        chemical_control = treatment[prediction_name].get("chemical_control")
        
        return render_template(
            'diagnose.html',
            prediction_name=prediction_name,
            symptom=symptom,
            organic_control=organic_control,
            chemical_control=chemical_control,
            full_filename=full_filename
        )
    
    else:
        return redirect(url_for("diagnose"))


if __name__ == '__main__':
    app.run()
