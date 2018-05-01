#!/usr/bin/python3

from control import PidController

class VelocityController():

    # Max velocity in inches per second
    MAX_VELOCITY = 18

    # Feed forward gains
    kV = 1 / MAX_VELOCITY

    # Feed back gains
    kP = 0.05
    kI = 0
    kD = 0

    done = False

    def __init__(self, target = 0):
        self.pid = PidController(self.kP, self.kI, self.kD, False, False)
        self.target = target

    def calculate(self, velocity, target = None):
        if (target != None):
            self.target = target

        # Feed back
        output = self.pid.calculate(self.target, velocity)

        # Feed forward
        output += self.kV * self.target

        return output
