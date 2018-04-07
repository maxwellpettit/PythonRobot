#!/bin/python

import datetime

class PidController():

    MAX_OUTPUT = 1
    MIN_OUTPUT = -1
    THRESHOLD = 0.05

    kP = 0
    kI = 0
    kD = 0

    lastTime = 0
    lastError = 0
    errorIntegral = 0

    def __init__(self, kP, kI, kD):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.lastTime = datetime.datetime.now()

    def calculate(self, target, input, time):
        output = 0

        if (input > (target * (1 - self.THRESHOLD)) and input < (target * (1 + self.THRESHOLD))): 
            error = target - input
            dT = time - self.lastTime
            errorDeriv = (self.lastError - error) / dT
            self.errorIntegral += error * dT

            output = self.kP * error + self.kI * self.errorIntegral + self.kD * errorDeriv
            output = self.clamp(output)

        return output

    def clamp(self, output):
        if (output > self.MAX_OUTPUT):
            return self.MAX_OUTPUT
        elif (output < self.MIN_OUTPUT):
            return self.MIN_OUTPUT
        else:
            return output
