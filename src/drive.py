#!/bin/python

import time
from hardware import RRB3, Encoder
from operatorInterface import OperatorInterface

class Drive():

    BATTERY_VOLTS = 9
    MOTOR_VOLTS = 6

    DEADBAND = 0.2
    MAX_OUTPUT = 1

    MANUAL = 0
    SONIC = 1
    PROFILE = 2

    driveMode = MANUAL

    def __init__(self, oi):
        self.oi = oi
        self.board = RRB3(self.BATTERY_VOLTS, self.MOTOR_VOLTS)
        self.leftEncoder = Encoder(5)
        self.rightEncoder = Encoder(6)

    def update(self):
        if (self.driveMode == self.MANUAL):
            self.tankDrive(self.oi.getLeft(), self.oi.getRight())
        elif (self.driveMode == self.SONIC):
            output = self.calculateSonic()
            self.tankDrive(output, output)

    def setSonicFollower(self, follower):
        self.driveMode = self.SONIC
        self.follower = follower

    def calculateSonic(self):
        distance = self.board.get_distance_in()
        print("Distance = " + str(distance) + " inches")
        output = self.follower.calculate(distance)
        if (self.follower.done):
            self.driveMode = self.MANUAL
        return output

    def tankDrive(self, left, right):
        self.board.set_motors(self.constrain(left), int(left >= 0), self.constrain(right), int(right >= 0))
        self.leftEncoder.setDirection(left)
        self.rightEncoder.setDirection(right)

    # Limit motor output to range [self.DEADBAND, self.MAX_OUTPUT]
    def constrain(self, output):
        if (output == 0):
             return 0
        else:
             return max(self.clamp(output), self.DEADBAND)
    
    def clamp(self, output):
        output = abs(output)
        if (output > self.MAX_OUTPUT):
            return self.MAX_OUTPUT
        else:
            return output

    def stop(self):
        print("Drive Stop")
        self.leftEncoder.stop()
        self.rightEncoder.stop()
        self.board.cleanup()
