#!/bin/python

from control import PidController

class SonicFollower():

    kP = 0.2
    kI = 0
    kD = 0.01

    done = False

    def __init__(self, target):
        self.target = target
        self.pid = PidController(self.kP, self.kI, self.kD, True)

    def calculate(self, distance):
        output = self.pid.calculate(self.target, distance)
        if (self.pid.done):
            self.done = True
        
        return output
