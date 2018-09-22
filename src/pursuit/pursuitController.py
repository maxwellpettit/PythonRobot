#!/usr/bin/python3

from math import cos, sin, radians
from control import VelocityController


class PursuitController():

    # Distance between the wheels of the vehicle
    WHEELBASE = 7
    # Ratio of velocity PID controller updates to pursuit calculations
    PID_FREQUENCY = 2

    pidIndex = 0
    done = False

    def __init__(self, path, lookahead, velocity):
        self.path = path
        self.lookahead = lookahead
        self.velocity = velocity
        self.left = VelocityController()
        self.right = VelocityController()

    def calculate(self, x, y, heading, leftVelocity, rightVelocity):
        """
        Calculate the left/right motor outputs using velocity controllers
        """
        print('')
        print('Pose = (' + str(x) + ', ' + str(y) + ')')

        left = 0
        right = 0
        # Update output velocity using pure pursuit
        if (self.pidIndex % self.PID_FREQUENCY == 0):
            (l, r) = self.update(x, y, heading)
            left = self.left.calculate(leftVelocity, l)
            right = self.right.calculate(rightVelocity, r)
            self.pidIndex = 1

        # Let velocity controller update to reach target velocity
        else:
            left = self.left.calculate(leftVelocity)
            right = self.right.calculate(rightVelocity)
            self.pidIndex += 1

        return (left, right)

    def update(self, xv, yv, heading):
        """
        Calculate the desired left/right linear velocity using pure pursuit
        https://www.ri.cmu.edu/pub_files/pub3/coulter_r_craig_1992_1/coulter_r_craig_1992_1.pdf
        http://www8.cs.umu.se/research/ifor/IFORnav/reports/rapport_MartinL.pdf
        """
        # Find goal point on path
        (xg, yg) = self.path.findGoalPoint(xv, yv, self.lookahead)
        print('(xg, yg) = (' + str(xg) + ', ' + str(yg) + ')')

        if (xg is not None and yg is not None):
            # Transform goal point relative to vehicle heading
            (xgv, ygv) = self.transformToVehicle(xv, yv, xg, yg, heading)
            print('(xgv, ygv) = (' + str(xgv) + ', ' + str(ygv) + ')')

            # Calculate left/right wheel velocity based on goal point
            return self.outputKinematics(xgv, ygv)

        else:
            self.done = True

        return (0, 0)

    def transformToVehicle(self, xv, yv, xg, yg, heading):
        """
        Transform goal point to coordinates relative to vehicle's current heading
        (i.e. treat vehicle as (0, 0) with heading as the y-axis)
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
        d2 = xgv**2 + ygv**2
        deltaV = 0
        if (xgv != 0):
            radius = d2 / (2 * xgv)
            omega = self.velocity / radius
            deltaV = omega * self.WHEELBASE

        leftVelocity = 0
        rightVelocity = 0
        if (ygv >= 0):
            leftVelocity = self.velocity + deltaV
            rightVelocity = self.velocity - deltaV

        print('Velocity = (' + str(leftVelocity) + ', ' + str(rightVelocity) + ')')
        return (leftVelocity, rightVelocity)
