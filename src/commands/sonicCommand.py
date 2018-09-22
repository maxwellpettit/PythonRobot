#!/usr/bin/python3

from control import SonicController

class SonicCommand():

    def __init__(self, drive, distance):
        self.drive = drive
        self.distance = distance

    def run(self):
        self.drive.setController(SonicController(self.distance), self.drive.SONIC)
