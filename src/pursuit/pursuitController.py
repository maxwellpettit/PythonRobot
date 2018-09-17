#!/usr/bin/python3

from math import cos, sin, radians
from pursuit import PathSegment
from control import VelocityController


class PursuitController():

    WHEELBASE = 11
    PID_FREQUENCY = 2
    pidIndex = 0

    def __init__(self, path, lookahead, velocity):
        self.path = path
        self.lookahead = lookahead
        self.velocity = velocity
        self.left = VelocityController()
        self.right = VelocityController()

    def calculate(self, x, y, heading, leftVelocity, rightVelocity):
        print('')
        print('Pose = (' + str(x) + ', ' + str(y) + ')')

        left = 0
        right = 0
        if (self.pidIndex % self.PID_FREQUENCY == 0):
            (l, r) = self.update(x, y, heading)
            left = self.left.calculate(leftVelocity, l)
            right = self.right.calculate(rightVelocity, r)
            self.pidIndex = 1
        else:
            left = self.left.calculate(leftVelocity)
            right = self.right.calculate(rightVelocity)
            self.pidIndex += 1

        return (left, right)

    def update(self, x, y, heading):
        (xg, yg) = self.path.findGoalPoint(x, y, self.lookahead)
        print('(xg, yg) = (' + str(xg) + ', ' + str(yg) + ')')
        if (xg is not None and yg is not None):
            (xgv, ygv) = self.transformToVehicle(x, y, xg, yg, heading)
            print('(xgv, ygv) = (' + str(xgv) + ', ' + str(ygv) + ')')
            return self.outputKinematics(xgv, ygv)

        return (0, 0)

    def transformToVehicle(self, xv, yv, xg, yg, heading):
        """
        Transform goal point to coordinates relative to vehicle's current heading
        (i.e. treat vehicle heading as the y-axis)
        """
        heading = radians(heading)
        s = round(sin(heading), 5)
        c = round(cos(heading), 5)
        xgv = (xg - xv) * s - (yg - yv) * c
        ygv = (xg - xv) * c + (yg - yv) * s
        return (xgv, ygv)

    def outputKinematics(self, xgv, ygv):
        """
        Calculate left/right velocity based on the transformed goal point
        """
        d = PathSegment.getDistance(0, 0, xgv, ygv)
        deltaV = 0
        if (xgv != 0):
            radius = d / (2 * xgv)
            omega = self.velocity / radius
            deltaV = omega * self.WHEELBASE

        print('deltaV = ' + str(deltaV))
        leftVelocity = 0
        rightVelocity = 0
        if (ygv >= 0):
            leftVelocity = self.velocity + deltaV
            rightVelocity = self.velocity - deltaV
            if (leftVelocity < 0):
                leftVelocity = 0
            if (rightVelocity < 0):
                rightVelocity = 0

        print('Velocity = (' + str(leftVelocity) + ', ' + str(rightVelocity) + ')')
        return (leftVelocity, rightVelocity)
