#!/usr/bin/python3

import time
from hardware import RRB3, Encoder, SimpleGyro
from operatorInterface import OperatorInterface

class Drive():

    BATTERY_VOLTS = 9
    MOTOR_VOLTS = 6

    DEADBAND = 0.3
    MAX_OUTPUT = 1

    MANUAL = 0
    SONIC = 1
    ENCODER = 2
    GYRO = 3
    VELOCITY = 4
    PROFILE = 5

    driveMode = MANUAL

    def __init__(self, oi):
        self.oi = oi
        self.board = RRB3(self.BATTERY_VOLTS, self.MOTOR_VOLTS)
        self.leftEncoder = Encoder(19)
        self.rightEncoder = Encoder(26)
        self.gyro = SimpleGyro()

    def update(self):
        self.updateSensors()

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
            self.tankDrive(-output, output)
        elif (self.driveMode == self.VELOCITY):
            output = self.calculateVelocity()
            self.tankDrive(output, output)

    def updateSensors(self):
        self.gyro.update()
        self.leftEncoder.update()
        self.rightEncoder.update()

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
        leftDistance = self.leftEncoder.getDistance()
        rightDistance = self.rightEncoder.getDistance()
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

    def setVelocityFollower(self, follower):
        self.driveMode = self.VELOCITY
        self.follower = follower

    def calculateVelocity(self):
        velocity = (self.rightEncoder.velocity + self.leftEncoder.velocity) / 2
        print("Velocity: " + str(velocity))
        output = self.follower.calculate(velocity)
        if (self.follower.done):
            self.driveMode = self.MANUAL
        return output

    def tankDrive(self, left, right):
        self.board.set_motors(self.constrain(left), self.sign(left), self.constrain(right), self.sign(right))
        self.leftEncoder.setDirection(self.sign(left))
        self.rightEncoder.setDirection(self.sign(right))

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
