#!/usr/bin/python3

from control import PidController, VelocityController

class VelocityCommand():

    def __init__(self, drive, velocity):
        self.drive = drive
        self.velocity = velocity

    def run(self):
        self.drive.setController(VelocityController(self.velocity), self.drive.VELOCITY)
