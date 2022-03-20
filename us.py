import RPi.GPIO as GPIO

import time

from rpi_lcd import LCD

GPIO.setmode(GPIO.BCM)
TRIG = 17

ECHO = 27

lcd=LCD()

lcd.text("hello",1)
lcd.text("hello",2)

print("Distance Measurement In Progress")

GPIO.setup(TRIG,GPIO.OUT)

GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)

print("Waiting For Sensor To Settle")
time.sleep(10)
while True:
	lcd.clear()
	time.sleep(0.8) 
	GPIO.output(TRIG, True)
	
	time.sleep(0.00001)
	
	GPIO.output(TRIG, False)
	
	while GPIO.input(ECHO)==0:
	
	  pulse_start = time.time()
	
	while GPIO.input(ECHO)==1:
	
	  pulse_end = time.time()
	
	pulse_duration = pulse_end - pulse_start
	
	distance1 = pulse_duration * 17150
	
	distance1 = round(distance1, 2)
	#print("Distance:",distance1,"cm")
	
	time.sleep(0.8)	


	GPIO.output(TRIG, True)
	
	time.sleep(0.00001)
	
	GPIO.output(TRIG, False)
	
	while GPIO.input(ECHO)==0:
	
	  pulse_start = time.time()
	
	while GPIO.input(ECHO)==1:
	
	  pulse_end = time.time()
	
	pulse_duration = pulse_end - pulse_start
	
	distance2 = pulse_duration * 17150
	
	distance2 = round(distance2, 2)
	#print("Distance:",distance2,"cm")
	op=round(((distance2-distance1)/1.60002)/27.778,2)
	print("Speed is: ",op)
	lcd.text(str(op),1)	
	
GPIO.cleanup()