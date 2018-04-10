#!/bin/python

from util import PidController, SonicFollower

class ApproachCommand():

    def __init__(self, drive, distance):
        self.drive = drive
        self.follower = SonicFollower(distance)

    def run(self):
        self.drive.setSonicFollower(self.follower)
