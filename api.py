import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import cv2
from keras.models import load_model
from keras_preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
import numpy as np

app = FastAPI()

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

@app.post("/detect_deepfake/")
async def detect_deepfake(file: UploadFile = File(...)):
    try:
        video_path = f"temp_{file.filename}"
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        cap = cv2.VideoCapture(video_path)
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
        if os.path.exists(video_path):
            os.remove(video_path)

        final_output = get_final_output(fake_count, real_count)
        return JSONResponse(status_code=200, content={
            "result": final_output,
            "total_frames": total_frames,
            "fake_count": fake_count,
            "real_count": real_count
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
