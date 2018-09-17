#!/usr/bin/python3

from control import VelocityController
from pursuit import PathSegment, Path, PursuitController


class PursuitCommand():
    def __init__(self, drive):
        self.drive = drive
        seg1 = PathSegment(0, 0, 0, 12)
        seg2 = PathSegment(0, 12, 12, 12)
        seg3 = PathSegment(12, 12, 18, 18)
        path = Path()
        path.addSegment(seg1)
        path.addSegment(seg2)
        path.addSegment(seg3)
        self.controller = PursuitController(path, 5, 8)

    def run(self):
        self.drive.setController(self.controller, self.drive.PURSUIT)
