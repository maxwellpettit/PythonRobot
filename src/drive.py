#!/usr/bin/python3

import time
from hardware import RRB3, Encoder, Gyro
from operatorInterface import OperatorInterface

class Drive():

    BATTERY_VOLTS = 9
    MOTOR_VOLTS = 6

    DEADBAND = 0.2
    MAX_OUTPUT = 1

    MANUAL = 0
    SONIC = 1
    ENCODER = 2
    GYRO = 3
    PROFILE = 4

    driveMode = MANUAL

    def __init__(self, oi):
        self.oi = oi
        self.board = RRB3(self.BATTERY_VOLTS, self.MOTOR_VOLTS)
        self.leftEncoder = Encoder(19)
        self.rightEncoder = Encoder(26)
        self.gyro = Gyro()

    def update(self):
        self.gyro.update()

        if (self.driveMode == self.MANUAL):
            self.tankDrive(self.oi.getLeft(), self.oi.getRight())
        elif (self.driveMode == self.SONIC):
            output = self.calculateSonic()
            self.tankDrive(output, output)
        elif (self.driveMode == self.ENCODER):
            left, right = self.calculateEncoder()
            self.tankDrive(left, right)
        elif (self.driveMode == self.GYRO):
            output = self.calculateGyro()
            self.tankDrive(output, -output)

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

    def setEncoderFollower(self, follower):
        self.leftEncoder.reset()
        self.rightEncoder.reset()
        self.driveMode = self.ENCODER
        self.follower = follower

    def calculateEncoder(self):
        leftDistance = self.leftEncoder.getInches()
        rightDistance = self.rightEncoder.getInches()
        print("Distance = (" + str(leftDistance) + ", " + str(rightDistance) + ") inches")
        leftOutput, rightOutput = self.follower.calculate(leftDistance, rightDistance)
        if (self.follower.done):
            self.driveMode = self.MANUAL
        return leftOutput, rightOutput

    def setGyroFollower(self, follower):
        self.driveMode = self.GYRO
        self.follower = follower

    def calculateGyro(self):
        angle = self.gyro.yaw
        print("Yaw: " + str(angle))
        output = self.follower.calculate(angle)
        if (self.follower.done):
            self.driveMode = self.MANUAL
        return output

    def tankDrive(self, left, right):
        self.board.set_motors(self.constrain(left), self.sign(left), self.constrain(right), self.sign(right))
        self.leftEncoder.setDirection(left)
        self.rightEncoder.setDirection(right)

    def constrain(self, output):
        """
        Limit motor output to range [self.DEADBAND, self.MAX_OUTPUT]
        """
        
        if (output == 0):
            return 0
        else:
            output = abs(output)
            if (output > self.MAX_OUTPUT):
                return self.MAX_OUTPUT
            else:
                return max(output, self.DEADBAND)

    def sign(self, input): 
        if (input > 0): 
            return 1
        elif (input < 0):
            return -1
        else:
            return 0

    def stop(self):
        print("Drive Stop")
        self.leftEncoder.stop()
        self.rightEncoder.stop()
        self.board.cleanup()
