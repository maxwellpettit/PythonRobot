#!/bin/python

import time
from hardware import RRB3, Encoder, mpu6050
from operatorInterface import OperatorInterface

class Drive():

    BATTERY_VOLTS = 9
    MOTOR_VOLTS = 6

    DEADBAND = 0.2
    MAX_OUTPUT = 1

    MANUAL = 0
    SONIC = 1
    ENCODER = 2
    PROFILE = 3

    driveMode = MANUAL

    x = 0
    y = 0
    z = 0

    def __init__(self, oi):
        self.oi = oi
        self.board = RRB3(self.BATTERY_VOLTS, self.MOTOR_VOLTS)
        self.leftEncoder = Encoder(19)
        self.rightEncoder = Encoder(26)
        #self.gyro = mpu6050(0x68)

    def update(self):
        #gyro_data = self.gyro.get_gyro_data()
        #self.x += gyro_data["x"]
        #self.y += gyro_data["y"]
        #self.z += gyro_data["z"]
        #print("Gyro: " + str(self.x) + ", " + str(self.y) + ", " + str(self.z))
        if (self.driveMode == self.MANUAL):
            leftDistance = self.leftEncoder.getInches()
            rightDistance = self.rightEncoder.getInches()
            print("Distance = (" + str(leftDistance) + ", " + str(rightDistance) + ") inches")
            self.tankDrive(self.oi.getLeft(), self.oi.getRight())
        elif (self.driveMode == self.SONIC):
            output = self.calculateSonic()
            self.tankDrive(output, output)
        elif (self.driveMode == self.ENCODER):
            left, right = self.calculateEncoder()
            self.tankDrive(left, right)

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
