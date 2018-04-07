#!/bin/python

import RPi.GPIO as GPIO

class Encoder():

    count = 0
    direction = 1

    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.countTicks, bouncetime=50)

    def countTicks(self, value):
        self.count += self.direction
        print("Pin " + str(self.pin) + " Count = " + str(self.count))

    def reset(self):
        self.count = 0
        self.direction = 1

    def setDirection(self, input):
        if (input >= 0):
            self.direction = 1
        else:
            self.direction = -1

    def stop(self):
        print("Encoder Stop " + str(self.pin))
        GPIO.cleanup()
