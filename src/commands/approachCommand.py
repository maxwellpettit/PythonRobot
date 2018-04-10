#!/bin/python

from util import PidController, SonicFollower

class ApproachCommand():

    def __init__(self, drive, distance):
        self.drive = drive
        self.distance = distance

    def run(self):
        self.drive.setSonicFollower(SonicFollower(self.distance))
