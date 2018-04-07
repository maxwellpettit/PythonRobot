#!/bin/python

import time

class PidController():

    MAX_OUTPUT = 1
    MIN_OUTPUT = -1
    THRESHOLD = 0.02

    kP = 0
    kI = 0
    kD = 0

    lastTime = 0
    lastError = None
    errorIntegral = 0

    done = False

    def __init__(self, kP, kI, kD):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.lastTime = time.time()

    def calculate(self, target, input, time):
        output = 0

        minRange = target * (1 - self.THRESHOLD)
        maxRange = target * (1 + self.THRESHOLD)

        if (not self.done and (input < minRange or input > maxRange)):
            error = input - target
            dT = time - self.lastTime
            errorDeriv = 0
            if (self.lastError != None):
                errorDeriv = (self.lastError - error) / dT
            self.errorIntegral += error * dT

            output = self.kP * error + self.kI * self.errorIntegral + self.kD * errorDeriv
            output = self.clamp(output)

            self.lastTime = time
            self.lastError = error
        else:
            self.done = True
            print("PID DONE!")

        return output

    def clamp(self, output):
        if (output > self.MAX_OUTPUT):
            return self.MAX_OUTPUT
        elif (output < self.MIN_OUTPUT):
            return self.MIN_OUTPUT
        else:
            return output
