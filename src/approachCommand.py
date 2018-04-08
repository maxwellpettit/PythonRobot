#!/bin/python

from pidController import PidController

class ApproachCommand():

    DISTANCE_KP = 0.15
    DISTANCE_KI = 0
    DISTANCE_KD = 0.005

    def __init__(self, drive, distance):
        self.drive = drive
        self.distance = distance

    def run(self):
        pid = PidController(self.DISTANCE_KP, self.DISTANCE_KI, self.DISTANCE_KD, True)
        self.drive.setAutoMode(self.distance, pid)
