#!/usr/bin/python3

from control import PidController, GyroController

class GyroCommand():

    def __init__(self, drive, angle):
        self.drive = drive
        self.angle = angle

    def run(self):
        self.drive.setController(GyroController(self.angle), self.drive.GYRO)
