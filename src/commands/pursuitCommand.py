#!/usr/bin/python3

from pursuit import PathSegment, Path, PursuitController


class PursuitCommand():
    def __init__(self, drive):
        self.drive = drive
        self.createController()

    def createController(self):
        seg1 = PathSegment(0, 0, 5, 10)
        seg2 = PathSegment(5, 10, 0, 20)
        seg3 = PathSegment(0, 20, -5, 30)
        seg4 = PathSegment(-5, 30, 0, 40)
        path = Path()
        path.addSegment(seg1)
        path.addSegment(seg2)
        path.addSegment(seg3)
        path.addSegment(seg4)
        self.controller = PursuitController(path, 2, 8)

    def run(self):
        if (self.controller.done):
            self.createController()
        self.drive.setController(self.controller, self.drive.PURSUIT)
