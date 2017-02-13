#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep
from multiprocessing import Process

def setup_board(STEP_PIN,DIR_PIN):
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(STEP_PIN, GPIO.OUT)
    GPIO.output(STEP_PIN, 0)

    GPIO.setup(DIR_PIN, GPIO.OUT)
    GPIO.output(DIR_PIN, 0)

def move(STEP_PIN,DIR_PIN,DIR_STATE):
    for x in range(400):
        GPIO.output(STEP_PIN, 1)
        GPIO.output(STEP_PIN, 0)
        sleep(.005)
    sleep(.2)
    GPIO.output(DIR_PIN, DIR_STATE)


if __name__ == '__main__':
    try:
        setup_board(7, 11)
        setup_board(24, 26)
        dir_state = 0
        while True:
            p1 = Process(target=move, args=(7, 11, dir_state))
            p2 = Process(target=move, args=(24, 26, dir_state))
            p1.start()
            p2.start()
            p1.join()
            p2.join()
            dir_state = (dir_state+1)%2
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping")
        GPIO.cleanup()
