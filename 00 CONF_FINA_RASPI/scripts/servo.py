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

def posicion1():
    print('has elegido la posicion 1')
    brazo.ChangeDutyCycle(12.5)
    base.ChangeDutyCycle(2.5)
    time.sleep(1)
    brazo.ChangeDutyCycle(0)
    base.ChangeDutyCycle(0)
#    GPIO.cleanup()

def posicion2():
    print('has elegido la posicion 2')
    brazo.ChangeDutyCycle(12.5)
    base.ChangeDutyCycle(12.5)
    time.sleep(1)
    brazo.ChangeDutyCycle(0)
    base.ChangeDutyCycle(0)
#    GPIO.cleanup()

def detener_servo():
    brazo.ChangeDutyCycle(0)
    base.ChangeDutyCycle(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('elija un argumento, a o b')
        sys.exit(1)

    pos = sys.argv[1]

    if pos == "a":
        posicion1()
    elif pos == "b":
        posicion2()
    else:
        print('posicion no reconocida, elija posicion a o posicion b')
        detener_servo
        sys.exit(1)

    time.sleep(1)
    detener_servo()
    GPIO.cleanup()
