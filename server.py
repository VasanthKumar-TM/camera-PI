#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request
from camera import VideoCamera
import time
from time import sleep
import threading
import os
import RPi.GPIO as GPIO

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)


GPIO.setup(2, GPIO.OUT)



pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)

@app.route('/camera')
def camera():
    return render_template('camera.html')


@app.route('/camera_admin', methods=['POST'])
def cameraAdmin():
    if request.method=='POST':
        if(request.form.get('userid')=="gokartturbonites@gmail.com" and request.form.get('pwd')=="gokart@196"):
    	    return render_template('camera_admin.html')
        else:
            return render_template('index.html')

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/stop')
def stop():
    i=0
    p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
    p.start(2.5) # Initialization
    print("Trigger Extinguisher")
    try:
        while i<4:
            p.ChangeDutyCycle(7.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(10)
            time.sleep(0.5)
            p.ChangeDutyCycle(12.5)
            i+=1
    except KeyboardInterrupt:
        p.stop()
    pwm=GPIO.PWM(2, 50)
    pwm.start(0)
    arr=[1,2,3,4,5,6,7,8,9,10,11,12]
    while True:
        for i in range(2,14):
            print(i)
            sleep(0.3)
            pwm.ChangeDutyCycle(i)
        break
    pwm.stop()

    return "true"

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':

    app.run(host='0.0.0.0', port='5000', debug=False)
    

