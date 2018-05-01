#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

class Encoder():

    WHEEL_DIAMETER = 3.15
    TICKS_PER_REV = 960
    PI = 3.14159265

    count = 0
    direction = 0
    velocity = 0
    lastCount = 0

    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.tick)
        self.lastTime = time.time()

    def tick(self, value):
        self.count += self.direction
        # print("Pin " + str(self.pin) + " Count = " + str(self.count) + " Inches = " + str(self.getDistance()))

    def update(self):
        dCount = self.count - self.lastCount
        t = time.time()
        self.velocity = self.countToInches(dCount) / (t - self.lastTime)
        
        self.lastTime = t
        self.lastCount = self.count 

        print("Pin " + str(self.pin) + " Velocity = " + str(self.velocity))

    def getDistance(self):
        return self.countToInches(self.count)

    def countToInches(self, count):
        return(count * self.WHEEL_DIAMETER * self.PI / self.TICKS_PER_REV)

    def reset(self):
        self.count = 0
        self.direction = 0
        self.velocity = 0
        self.lastTime = time.time()
        self.lastCount = 0

    def setDirection(self, direction):
        self.direction = direction

    def stop(self):
        print("Encoder Stop " + str(self.pin))
        GPIO.cleanup()
