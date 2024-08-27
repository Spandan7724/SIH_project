from flask import Flask, render_template, request, redirect, url_for, Response
import os
import cv2
from keras.models import load_model
from keras_preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
import numpy as np

app = Flask(__name__)

MODEL_PATH = "C:/Users/91898/Code/deepfake_detection_webapp/model_resnet50.h5"
model = load_model(MODEL_PATH)


def preprocess_image(image):
    image = cv2.resize(image, (224, 224))
    image = img_to_array(image)
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0)
    return image


def get_final_output(fake_count, real_count):
    if fake_count > real_count:
        return "Fake"
    elif real_count > fake_count:
        return "Real"
    else:
        return "Equal Number of Real and Fake Frames"


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file_path = os.path.join('static', 'videos', filename)

            # Ensure the static directory exists
            if not os.path.exists('static'):
                os.makedirs('static')

            file.save(file_path)

            cap = cv2.VideoCapture(file_path)
            fake_count = 0
            real_count = 0
            total_frames = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                total_frames += 1

                processed_frame = preprocess_image(frame)

                prediction = model.predict(processed_frame)
                prediction_class = np.argmax(prediction)

                if prediction_class == 0:
                    fake_count += 1
                else:
                    real_count += 1

            cap.release()

            # Remove the file after processing
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                print("The file does not exist:", file_path)

            final_output = get_final_output(fake_count, real_count)
            return redirect(url_for('result', filename=filename, final_output=final_output, total_frames=total_frames, fake_count=fake_count, real_count=real_count))

    return render_template('index.html')


@app.route('/result')
def result():
    filename = request.args.get('filename')
    final_output = request.args.get('final_output')
    total_frames = request.args.get('total_frames')
    fake_count = request.args.get('fake_count')
    real_count = request.args.get('real_count')
    return render_template('result.html', filename=filename, final_output=final_output, total_frames=total_frames, fake_count=fake_count, real_count=real_count)


if __name__ == '__main__':
    app.run(debug=True)
