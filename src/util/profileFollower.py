#!/bin/python

from util import PidController

class ProfileFollower():

    # Max velocity in inches per second
    MAX_VELOCITY = 10

    # Feed forward gains
    kV = 1 / MAX_VELOCITY
    kA = 0

    # Feed back gains
    kP = 0.1
    kI = 0
    kD = 0
    kGyro = 0

    index = 0
    done = False

    def __init__(self, leftTrajectory, rightTrajectory):
        self.leftTrajectory = leftTrajectory
        self.rightTrajectory = rightTrajectory
        self.leftPid = PidController(self.kP, self.kI, self.kD, False, False)
        self.rightPid = PidController(self.kP, self.kI, self.kD, False, False)

    def calculate(self, leftDistance, rightDistance, heading):
        leftOutput = 0.0
        rightOutput = 0.0

        if (not self.done and self.index <= len(self.leftTrajectory)):
            leftSetpoint = self.leftTrajectory[self.index]
            rightSetpoint = self.rightTrajectory[self.index]

            # Feed back
            leftOutput = self.leftPid.calculate(leftSetpoint.distance, leftDistance, leftSetpoint.velocity)
            rightOutput = self.rightPid.calculate(rightSetpoint.distance, rightDistance, rightSetpoint.velocity)

            # Feed forward
            leftOutput += self.kV * leftSetpoint.velocity + self.kA * leftSetpoint.acceleration
            rightOutput += self.kV * rightSetpoint.velocity + self.kA * rightSetpoint.acceleration

            # Angle feed back gain
            angleGain = self.kGyro * ((heading - leftSetpoint.heading) % 360 - 180) 
            leftOutput -= angleGain
            rightOutput += angleGain

            self.index += 1
        else:
            self.done = True
            print("PROFILE DONE!")

        return leftOutput, rightOutput
