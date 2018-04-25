#!/usr/bin/python3

from control import PidController, EncoderFollower

class EncoderCommand():

    def __init__(self, drive, distance):
        self.drive = drive
        self.distance = distance

    def run(self):
        self.drive.setEncoderFollower(EncoderFollower(self.distance))
