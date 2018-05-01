#!/usr/bin/python3

from control import PidController

class GyroController():

    DEGREES_TOLERANCE = 2

    kP = 0.01
    kI = 0
    kD = 0

    done = False

    def __init__(self, target):
        self.target = target
        self.pid = PidController(self.kP, self.kI, self.kD, False)
        self.pid.THRESHOLD = abs(self.DEGREES_TOLERANCE / target)

    def calculate(self, angle):
        output = self.pid.calculate(self.target, angle)
        if (self.pid.done):
            self.done = True

        return output
