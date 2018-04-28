#!/usr/bin/python3

from control import PidController, GyroFollower

class GyroCommand():

    def __init__(self, drive, angle):
        self.drive = drive
        self.angle = angle

    def run(self):
        self.drive.setGyroFollower(GyroFollower(self.angle))
