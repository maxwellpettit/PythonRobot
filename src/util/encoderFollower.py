#!/bin/python

from util import PidController

class EncoderFollower():

    # Feed back gains
    kP = 0.1
    kI = 0
    kD = 0

    done = False

    def __init__(self, target):
        self.target = target
        self.leftPid = PidController(self.kP, self.kI, self.kD, False)
        self.leftPid.THRESHOLD = 0.05
        self.rightPid = PidController(self.kP, self.kI, self.kD, False)
        self.rightPid.THRESHOLD = 0.05

    def calculate(self, leftDistance, rightDistance):
        # Feed back
        leftOutput = self.leftPid.calculate(self.target, leftDistance)
        rightOutput = self.rightPid.calculate(self.target, rightDistance)
        if (self.leftPid.done and self.rightPid.done):
            self.done = True

        return leftOutput, rightOutput
