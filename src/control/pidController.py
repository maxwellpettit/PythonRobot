#!/usr/bin/python3

import time


class PidController():

    THRESHOLD = 0.01
    I_TERM_LIMIT = 1.0

    kP = 0
    kI = 0
    kD = 0
    sign = 1

    lastTime = 0
    lastError = None
    errorIntegral = 0

    done = False

    def __init__(self, kP, kI, kD, flipSign=False, autoComplete=True):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        if (flipSign):
            self.sign = -1
        self.autoComplete = autoComplete
        self.lastTime = time.time()

    def calculate(self, target, input):
        output = 0

        t = time.time()
        minRange = target * (1 - self.THRESHOLD)
        maxRange = target * (1 + self.THRESHOLD)

        if (not self.autoComplete or (not self.done and (input < minRange or input > maxRange))):
            error = target - input
            dT = t - self.lastTime
            errorDeriv = 0
            if (self.lastError != None and dT != 0):
                errorDeriv = (error - self.lastError) / dT
            self.errorIntegral += error * dT

            integral = self.errorIntegral * self.kI
            if (integral > self.I_TERM_LIMIT):
                integral = self.I_TERM_LIMIT
            elif (integral < -self.I_TERM_LIMIT):
                integral = -self.I_TERM_LIMIT

            output = self.sign * (self.kP * error + integral + self.kD * errorDeriv)

            self.lastTime = t
            self.lastError = error
        elif (self.autoComplete):
            self.done = True
            print("PID DONE!")

        return output
