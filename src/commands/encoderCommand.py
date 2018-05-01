#!/usr/bin/python3

from control import PidController, EncoderController

class EncoderCommand():

    def __init__(self, drive, distance):
        self.drive = drive
        self.distance = distance

    def run(self):
        distance = self.distance + (self.drive.leftEncoder.getDistance() + self.drive.rightEncoder.getDistance()) / 2
        self.drive.setController(EncoderController(distance), self.drive.ENCODER)
