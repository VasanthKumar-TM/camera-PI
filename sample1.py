import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

GPIO.setup(3, GPIO.OUT)

pwm=GPIO.PWM(3, 50)

pwm.start(0)
arr=[1,2,3,4,5,6,7,8,9,10,11,12]
def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(3, True)
	pwm.ChangeDutyCycle(duty)
	sleep(0.1)
	GPIO.output(3, False)
	pwm.ChangeDutyCycle(0)

while True:
	
	for i in range(2,14):
		print(i)
		sleep(0.3)
		pwm.ChangeDutyCycle(i)
	break
	#pwm.ChangeDutyCycle(0)
		#SetAngle(90) 
pwm.stop()
GPIO.cleanup()