#!/bin/python

import datetime
from rrb3 import RRB3
from operatorInterface import OperatorInterface
from encoder import Encoder

class Drive():

    MANUAL = 0
    AUTO = 1
    PROFILE = 2

    driveMode = MANUAL
    BATTERY_VOLTS = 9
    MOTOR_VOLTS = 6

    leftSetpoint = 0
    rightSetpoint = 0

    def __init__(self, oi):
        print("Drive Init")

        self.oi = oi
        self.board = RRB3(self.BATTERY_VOLTS, self.MOTOR_VOLTS)
        self.leftEncoder = Encoder(2)
        self.rightEncoder = Encoder(3)

    def update(self):
        print("Drive Update")
        #distIn = self.board.get_distance_in()
        #print("Distance =" + str(distIn) + " inches")

        if (self.driveMode == self.MANUAL):
            self.tankDrive(self.oi.getLeft(), self.oi.getRight())
        elif (self.driveMode == self.AUTO):
            if (self.pid):
                setpoint = self.pid.calculate(self.autoTarget, self.board.get_distance_in(), datetime.datetime.now())
                self.leftSetpoint = setpoint
                self.rightSetpoint = setpoint
            self.tankDrive(self.leftSetpoint, self.rightSetpoint)

    def tankDrive(self, left, right):
        print("Tank Drive (" + str(left) + ", " + str(right) + ")")
        self.board.set_motors(abs(left), int(left >= 0), abs(right), int(right >= 0))
        self.leftEncoder.setDirection(left)
        self.rightEncoder.setDirection(right)

    def setAutoMode(self, target, pid):
        self.autoTarget = target
        self.pid = pid
        self.driveMode = self.AUTO
        self.oi.stop

    def stop(self):
        print("Drive Stop")
        self.leftEncoder.stop()
        self.rightEncoder.stop()
        self.board.cleanup()

