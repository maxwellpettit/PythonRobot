#!/usr/bin/python3

import RPi.GPIO as GPIO

class Encoder():

    WHEEL_DIAMETER = 3.15
    TICKS_PER_REV = 960
    PI = 3.14159265

    count = 0
    direction = 0

    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.countTicks)

    def countTicks(self, value):
        self.count += self.direction
        # print("Pin " + str(self.pin) + " Count = " + str(self.count) + " Inches = " + str(self.getInches()))

    def getInches(self):
        return(self.count * self.WHEEL_DIAMETER * self.PI / self.TICKS_PER_REV)

    def reset(self):
        self.count = 0
        self.direction = 0

    def setDirection(self, direction):
        self.direction = direction

    def stop(self):
        print("Encoder Stop " + str(self.pin))
        GPIO.cleanup()
