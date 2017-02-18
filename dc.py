import RPi.GPIO as GPIO
from time import sleep

class DCmotor():
    def __init__(self, wire1, wire2):
        self.wire1 = wire1
        self.wire2 = wire2
        self.state = 'up'

        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.wire1, GPIO.OUT)
        GPIO.output(self.wire1, 0)        

        GPIO.setup(self.wire2, GPIO.OUT)
        GPIO.output(self.wire2, 0)
        
    def up(self):
        GPIO.output(self.wire1, 1)
        GPIO.output(self.wire2, 0)
        sleep(.2)
        GPIO.output(self.wire1, 0)
        GPIO.output(self.wire2, 0)
        self.state = 'up'
    
    def down(self):
        GPIO.output(self.wire1, 0)
        GPIO.output(self.wire2, 1)
        sleep(.6)
        GPIO.output(self.wire1, 0)
        GPIO.output(self.wire2, 0)
        self.state = 'down'
        
    def get_state(self):
        return self.state

