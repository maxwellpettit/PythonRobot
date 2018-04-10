#!/bin/python

from util import PidController

class SonicFollower():

    DISTANCE_KP = 0.15
    DISTANCE_KI = 0
    DISTANCE_KD = 0.005

    done = False

    def __init__(self, target):
        self.target = target
        self.pid = PidController(self.DISTANCE_KP, self.DISTANCE_KI, self.DISTANCE_KD, True)

    def calculate(self, distance):
        output = self.pid.calculate(self.target, distance)
        if (self.pid.done):
            self.done = True
        
        return output
