#!/bin/python

import time

class PidController():

    THRESHOLD = 0.01

    kP = 0
    kI = 0
    kD = 0
    sign = 1

    lastTime = 0
    lastError = None
    errorIntegral = 0

    done = False

    def __init__(self, kP, kI, kD, flipSign, autoComplete = True):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        if (flipSign):
            self.sign = -1
        self.autoComplete = autoComplete
        self.lastTime = time.time()

    def calculate(self, target, input, dOffset = 0):
        output = 0

        t = time.time()
        minRange = target * (1 - self.THRESHOLD)
        maxRange = target * (1 + self.THRESHOLD)

        if (not self.autoComplete or (not self.done and (input < minRange or input > maxRange))):
            error = target - input
            dT = t - self.lastTime
            errorDeriv = 0
            if (self.lastError != None):
                errorDeriv = (error - self.lastError) / dT
            self.errorIntegral += error * dT

            output = self.sign * (self.kP * error + self.kI * self.errorIntegral + self.kD * (errorDeriv - dOffset))

            self.lastTime = t
            self.lastError = error
        elif (self.autoComplete):
            self.done = True
            print("PID DONE!")

        return output
