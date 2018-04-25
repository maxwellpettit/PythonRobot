#!/usr/bin/python3

from control import PidController

class EncoderFollower():

    INCHES_PER_TICK = 2.2

    kP = 0.1
    kI = 0
    kD = 0

    done = False

    def __init__(self, target):
        self.target = target
        self.leftPid = PidController(self.kP, self.kI, self.kD, False)
        self.leftPid.THRESHOLD = self.INCHES_PER_TICK / target
        self.rightPid = PidController(self.kP, self.kI, self.kD, False)
        self.rightPid.THRESHOLD = self.INCHES_PER_TICK / target

    def calculate(self, leftDistance, rightDistance):
        # Feed back
        leftOutput = self.leftPid.calculate(self.target, leftDistance)
        rightOutput = self.rightPid.calculate(self.target, rightDistance)
        if (self.leftPid.done and self.rightPid.done):
            self.done = True

        return leftOutput, rightOutput
