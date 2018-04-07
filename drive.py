#!/bin/python

from enum import Enum
#from rrb3 import RRB3
#from operatorInterface import OperatorInterface
from encoder import Encoder

class Drive():

    class DriveMode(Enum):
        AUTO = 0
        PROFILE = 1
        MANUAL = 2

    driveMode = DriveMode.MANUAL
    
    BATTERY_VOLTS = 9
    MOTOR_VOLTS = 6

    leftSetpoint = 0
    rightSetpoint = 0

    def __init__(self, oi):
        print("Drive Init")

        self.oi = oi
        #self.board = RRB3(self.BATTERY_VOLTS, self.MOTOR_VOLTS)
        self.leftEncoder = Encoder(2)
        self.rightEncoder = Encoder(3)

    def update(self):
        print("Drive Update")

        if (self.driveMode == self.DriveMode.MANUAL):
            #self.tankDrive(self.oi.getLeft(), self.oi.getRight())
            self.tankDrive(0, 0)
        elif (self.driveMode == self.DriveMode.AUTO):
            self.tankDrive(self.leftSetpoint, self.rightSetpoint)

    def tankDrive(self, left, right):
        print("Tank Drive (" + str(left) + ", " + str(right) + ")")
        #self.board.set_motors(abs(left), int(left >= 0), abs(right), int(right >= 0))
        self.leftEncoder.setDirection(left)
        self.rightEncoder.setDirection(right)

    def stop(self):
        print("Drive Stop")
        self.leftEncoder.stop()
        self.rightEncoder.stop()
        #self.board.cleanup()
        