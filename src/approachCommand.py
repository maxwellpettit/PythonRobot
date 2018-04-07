#!/bin/python

from pidController import PidController

class ApproachCommand():

    DISTANCE_KP = 0.1
    DISTANCE_KI = 0
    DISTANCE_KD = 0.001

    def __init__(self, drive, distance):
        self.drive = drive
        self.distance = distance

    def run(self):
        pid = PidController(self.DISTANCE_KP, self.DISTANCE_KI, self.DISTANCE_KD)
        self.drive.setAutoMode(self.distance, pid)
