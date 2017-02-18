import RPi.GPIO as GPIO
from time import sleep

class motor():
    def __init__(self, step_pin, dir_pin):
        self.pos = 0
        self.step_pin = step_pin
        self.dir_pin = dir_pin

        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.output(self.step_pin, 0)

        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.output(self.dir_pin, 0)
        
    def move(self, movement_info, speed):
        for mag, dir in movement_info:
            if mag:
                GPIO.output(self.dir_pin, dir)
                GPIO.output(self.step_pin, 1)
                GPIO.output(self.step_pin, 0)
                sleep(speed)
            else:
                sleep(speed)
                    
    def goto(self, dest, speed):
        dif = dest - self.pos
        if dif == 0:
            return
        else:
            GPIO.output(self.dir_pin, 1 if dif > 0 else 0)
            for x in range(abs(dif)):
                GPIO.output(self.step_pin, 1)
                GPIO.output(self.step_pin, 0)
                sleep(speed)
        
        # self.pos = dest
    
    def set_pos(self, num):
        self.pos = num
        
    # def get_pos(self):
        # return self.pos
    
    def reset(self):
        GPIO.output(self.dir_pin, 0)
        for x in range(400):
            GPIO.output(self.step_pin, 1)
            sleep(.0025)
            GPIO.output(self.step_pin, 0)
            sleep(.0025)
        sleep(.2)