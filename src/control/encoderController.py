#!/usr/bin/python3

from control import PidController


class EncoderController():

    INCHES_TOLERANCE = 0.5

    kP = 0.1
    kI = 0
    kD = 0

    done = False

    def __init__(self, target):
        self.target = target
        self.pid = PidController(self.kP, self.kI, self.kD)
        self.pid.THRESHOLD = abs(self.INCHES_TOLERANCE / target)

    def calculate(self, distance):
        output = self.pid.calculate(self.target, distance)
        if (self.pid.done):
            self.done = True

        return output
