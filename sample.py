import cv2

from flask import Flask, render_template, Response, stream_with_context, request

import numpy as np 
from picamera.array import PiRGBArray
from picamera import PiCamera 

fire_cascade = cv2.CascadeClassifier('fire_detection.xml')
app = Flask('__name__')

@app.route('/')
def start():
    return "welcome "

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

def video_stream():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(640, 480))
    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = image.array
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fire = fire_cascade.detectMultiScale(frame, 1.2, 5)
        for (x, y, w, h) in fire:
            cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            print("fire is detected")
            
        if(True):
            ret, buffer = cv2.imencode('.jpeg',frame)
            frame = buffer.tobytes()
            rawCapture.truncate(0)
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame +b'\r\n')


app.run(host='127.0.0.1', port='5000', debug=False)