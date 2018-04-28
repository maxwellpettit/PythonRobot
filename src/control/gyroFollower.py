#!/usr/bin/python3

from control import PidController

class GyroFollower():

    kP = 0.0025
    kI = 0
    kD = 0

    done = False

    def __init__(self, target):
        self.target = target
        self.pid = PidController(self.kP, self.kI, self.kD, True)

    def calculate(self, angle):
        output = self.pid.calculate(self.target, angle)
        if (self.pid.done):
            self.done = True
        
        return output
