#!/bin/python

import time

class PidController():

    MAX_OUTPUT = 1
    MIN_OUTPUT = -1
    THRESHOLD = 0.01

    kP = 0
    kI = 0
    kD = 0
    sign = 1

    lastTime = 0
    lastError = None
    errorIntegral = 0

    done = False

    def __init__(self, kP, kI, kD, flipSign):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        if (flipSign):
            self.sign = -1
        self.lastTime = time.time()

    def calculate(self, target, input, time):
        output = 0

        minRange = target * (1 - self.THRESHOLD)
        maxRange = target * (1 + self.THRESHOLD)

        if (not self.done and (input < minRange or input > maxRange)):
            error = target - input
            dT = time - self.lastTime
            errorDeriv = 0
            if (self.lastError != None):
                errorDeriv = (error - self.lastError) / dT
            self.errorIntegral += error * dT

            output = self.sign * (self.kP * error + self.kI * self.errorIntegral + self.kD * errorDeriv)
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
