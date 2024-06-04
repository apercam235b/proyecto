import sys
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
servoPINbase = 11
servoPINbrazo = 13

GPIO.setup(servoPINbase, GPIO.OUT)
GPIO.setup(servoPINbrazo, GPIO.OUT)

brazo = GPIO.PWM(servoPINbrazo, 50)
base = GPIO.PWM(servoPINbase, 50)

brazo.start(0)
base.start(0)

brazo.ChangeDutyCycle(7.5)
base.ChangeDutyCycle(7.5)

time.sleep(1)