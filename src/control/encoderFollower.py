#!/usr/bin/python3

from control import PidController

class EncoderFollower():

    INCHES_TOLERANCE = 0.5

    kP = 0.1
    kI = 0
    kD = 0

    done = False

    def __init__(self, target):
        self.target = target
        self.leftPid = PidController(self.kP, self.kI, self.kD, False)
        self.leftPid.THRESHOLD = abs(self.INCHES_TOLERANCE / target)
        self.rightPid = PidController(self.kP, self.kI, self.kD, False)
        self.rightPid.THRESHOLD = abs(self.INCHES_TOLERANCE / target)

    def calculate(self, leftDistance, rightDistance):
        leftOutput = self.leftPid.calculate(self.target, leftDistance)
        rightOutput = self.rightPid.calculate(self.target, rightDistance)
        if (self.leftPid.done and self.rightPid.done):
            self.done = True

        return leftOutput, rightOutput
