#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep

p1 = 13
p2 = 15

def setup_board():
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(p1, GPIO.OUT)
    GPIO.output(p1, 0)

    GPIO.setup(p2, GPIO.OUT)
    GPIO.output(p2, 0)

if __name__ == '__main__':
    try:
        setup_board()
        while True:
            GPIO.output(p1, 1)
            GPIO.output(p2, 0)
            sleep(.2)
            GPIO.output(p1, 0)
            GPIO.output(p2, 1)
            sleep(.3)
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping")
        GPIO.cleanup()
