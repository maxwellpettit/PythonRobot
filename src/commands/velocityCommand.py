#!/usr/bin/python3

from control import PidController, VelocityFollower

class VelocityCommand():

    def __init__(self, drive, velocity):
        self.drive = drive
        self.velocity = velocity

    def run(self):
        self.drive.setVelocityFollower(VelocityFollower(self.velocity))
