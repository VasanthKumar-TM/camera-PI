import cv2
from flask import Flask, render_template, Response, stream_with_context, request
import numpy as np
import time
from picamera.array import PiRGBArray
from picamera import PiCamera 
#from gpiozero import AngularServo
from time import sleep
import RPi.GPIO as GPIO
#servo =AngularServo(17, min_angle=0, max_angle=360)


fire_cascade = cv2.CascadeClassifier('fire_detection.xml')

app = Flask('__name__')

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization


@app.route('/camera')
def camera():
    return render_template('camera_admin.html')


@app.route('/')
def start():
    return render_template('index.html')


@app.route('/stop')
def stop():
    print("Trigger Extinguisher")
    i=0
    """while (True):
        servo =AngularServo(17, min_angle=0, max_angle=360)
        servo.angle = 180
        sleep(5)
        i+=1"""
    try:
      while True:
        p.ChangeDutyCycle(5)
        time.sleep(0.5)
        p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(10)
        time.sleep(0.5)
        p.ChangeDutyCycle(12.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(10)
        time.sleep(0.5)
        p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(5)
        time.sleep(0.5)
        p.ChangeDutyCycle(2.5)
        time.sleep(0.5)
    except KeyboardInterrupt:
      p.stop()
      GPIO.cleanup()
    return "true"

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

app.run(host='0.0.0.0', port='5000', debug=False)