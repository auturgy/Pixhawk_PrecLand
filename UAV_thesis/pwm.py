import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(33,GPIO.OUT)

pwm = GPIO.PWM(33,1250)
pwm.start(0)
time.sleep(5)
pwm.ChangeDutyCycle(0)
time.sleep(30)




##pwm.ChangeDutyCycle(25)
##time.sleep(10)
##pwm.ChangeDutyCycle(50)
##time.sleep(10)
##pwm.ChangeDutyCycle(75)
##time.sleep(10)
##pwm.ChangeDutyCycle(100)
##time.sleep(10)
#for i in range (0,100,5):
#    pwm.ChangeDutyCycle(i)
#    time.sleep(.5)
#for i in range (100,0,-5):
#    pwm.ChangeDutyCycle(i)
#    time.sleep(5)

pwm.stop()
