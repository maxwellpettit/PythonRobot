#!/usr/bin/python3

from hardware import RRB3, Encoder, SimpleGyro
from control import PoseEstimator


class Drive():

    BATTERY_VOLTS = 9
    MOTOR_VOLTS = 6

    DEADBAND = 0.2
    MAX_OUTPUT = 1

    MANUAL = 0
    SONIC = 1
    ENCODER = 2
    GYRO = 3
    VELOCITY = 4
    PROFILE = 5
    PURSUIT = 6

    driveMode = MANUAL
    controller = None

    def __init__(self, oi):
        self.oi = oi
        self.board = RRB3(self.BATTERY_VOLTS, self.MOTOR_VOLTS)
        self.leftEncoder = Encoder(19)
        self.rightEncoder = Encoder(26)
        self.gyro = SimpleGyro()
        self.poseEstimator = PoseEstimator()

    def update(self):
        self.updateSensors()

        if (self.driveMode == self.MANUAL):
            self.tankDrive(self.oi.getLeft(), self.oi.getRight())
        elif (self.driveMode == self.SONIC):
            output = self.calculateSonic()
            self.tankDrive(output, output)
        elif (self.driveMode == self.ENCODER):
            output = self.calculateEncoder()
            self.tankDrive(output, output)
        elif (self.driveMode == self.GYRO):
            output = self.calculateGyro()
            self.tankDrive(-output, output)
        elif (self.driveMode == self.VELOCITY):
            output = self.calculateVelocity()
            self.tankDrive(output, output)
        elif (self.driveMode == self.PURSUIT):
            (left, right) = self.calculatePursuit()
            self.tankDrive(left, right)

    def updateSensors(self):
        self.gyro.update()
        self.leftEncoder.update()
        self.rightEncoder.update()
        self.poseEstimator.update(self.leftEncoder.getDistance(), self.rightEncoder.getDistance(), self.gyro.yaw)

    def setController(self, controller, driveMode):
        self.controller = controller
        self.driveMode = driveMode

    def calculateSonic(self):
        distance = self.board.get_distance_in()
        print("Distance: " + str(distance))
        output = self.controller.calculate(distance)
        if (self.controller.done):
            self.driveMode = self.MANUAL
        return output

    def calculateEncoder(self):
        distance = (self.leftEncoder.getDistance() + self.rightEncoder.getDistance()) / 2
        print("Distance: " + str(distance))
        output = self.controller.calculate(distance)
        if (self.controller.done):
            self.driveMode = self.MANUAL
        return output

    def calculateGyro(self):
        angle = self.gyro.yaw
        print("Yaw: " + str(angle))
        output = self.controller.calculate(angle)
        if (self.controller.done):
            self.driveMode = self.MANUAL
        return output

    def calculateVelocity(self):
        velocity = (self.rightEncoder.velocity + self.leftEncoder.velocity) / 2
        print("Velocity: " + str(velocity))
        output = self.controller.calculate(velocity)
        if (self.controller.done):
            self.driveMode = self.MANUAL
        return output

    def calculatePursuit(self):
        (left, right) = self.controller.calculate(self.poseEstimator.poseX,
                                                  self.poseEstimator.poseY, self.poseEstimator.poseHeading,
                                                  self.leftEncoder.velocity, self.rightEncoder.velocity)
        if (self.controller.done):
            self.driveMode = self.MANUAL
        return (left, right)

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

    def sign(self, number):
        if (number > 0):
            return 1
        elif (number < 0):
            return -1
        else:
            return 0

    def stop(self):
        print("Drive Stop")
        self.leftEncoder.stop()
        self.rightEncoder.stop()
        self.board.cleanup()
