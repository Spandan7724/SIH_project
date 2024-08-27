# DeepFake Detection Web App

## Description
This project implements a web application for detecting deepfake videos using machine learning models. Users can upload a video file, and the application will analyze it to determine if it is likely a deepfake or genuine.

The web app leverages a pre-trained ResNet50 model for feature extraction and classification. It provides a user-friendly interface where users can upload videos, and the application processes them using Flask and TensorFlow/Keras.

## Features
- **Video Upload:** Users can upload video files (MP4 format).
- **Real-time Analysis:** The application provides real-time analysis of uploaded videos.
- **Detection Accuracy:** Utilizes machine learning models to classify videos as fake or genuine.
- **User Interface:** Simple and intuitive web interface for ease of use.

## Requirements
- Python 3.8.19
- Flask
- TensorFlow/Keras
- OpenCV (for video processing)
- Other dependencies listed in `requirements.txt`

## Installation
Clone the repository:
```bash
git clone https://github.com/Spandan7724/deepfake_detection_webapp.git
```
Navigate to the project directory:
```bash
cd deepfake_detection_webapp
```
Install dependencies:
```bash 
pip install -r requirements.txt
```

## Running the Application

1. Move into the flask directory 
```bash
cd flask
```

2. Run the Flask application:
```bash
python app.py
```
3. Open a web browser and go to <http://localhost:5000> to access the application.

## Example

![Alt Text](assets/Screenshot%202024-06-16%20143006.png)


![Alt Text](assets/Screenshot%202024-06-16%20143104.png)
