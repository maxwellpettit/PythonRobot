#!/usr/bin/python3

from control import VelocityController
from pursuit import PathSegment, Path, PursuitController


class PursuitCommand():
    def __init__(self, drive):
        self.drive = drive
        seg1 = PathSegment(0, 0, 0, 30)
        seg2 = PathSegment(0, 30, 20, 30)
        seg3 = PathSegment(20, 30, 20, 50)
        path = Path()
        path.addSegment(seg1)
        path.addSegment(seg2)
        path.addSegment(seg3)
        self.controller = PursuitController(path, 5, 8)

    def run(self):
        self.drive.setController(self.controller, self.drive.PURSUIT)
