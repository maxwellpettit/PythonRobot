#!/usr/bin/python3

from control import PidController, SonicFollower

class SonicCommand():

    def __init__(self, drive, distance):
        self.drive = drive
        self.distance = distance

    def run(self):
        self.drive.setSonicFollower(SonicFollower(self.distance))
