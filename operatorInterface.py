#!/bin/python

from xboxController import XboxController

class OperatorInterface():

    controller = XboxController(
        controllerCallBack = handleInput,
        joystickNo = 0,
        deadzone = 0.1,
        invertYAxis = True
    )

    def __init__(self):
        print("OI Init")
        self.controller.start()

    def getLeft(self):
        return self.controller.LTHUMBY

    def getRight(self):
        return 0.0

    # Xbox Control Ids
    # LTHUMBX = 0
    # LTHUMBY = 1
    # RTHUMBX = 2
    # RTHUMBY = 3
    # RTRIGGER = 4
    # LTRIGGER = 5
    # A = 6
    # B = 7
    # X = 8
    # Y = 9
    # LB = 10
    # RB = 11
    # BACK = 12
    # START = 13
    # XBOX = 14
    # LEFTTHUMB = 15
    # RIGHTTHUMB = 16
    # DPAD = 17
    def handleInput(self, controlId, value):
        if controlId == 8:
            print("X Button")

    def stop(self):
        print("OI Stop")
        self.controller.stop()