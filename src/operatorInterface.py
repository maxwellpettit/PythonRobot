#!/bin/python

from xboxController import XboxController

class OperatorInterface():

    def __init__(self):
        # Setup xbox controller with callbacks
        self.controller = XboxController(
            controllerCallBack = self.handleInput,
            joystickNo = 0,
            deadzone = 0.2,
            invertYAxis = True
        )

        self.controller.start()

    def getLeft(self):
        return self.controller.LTHUMBY

    def getRight(self):
        return self.controller.RTHUMBY

    def setXCommand(self, command):
        self.xCommand = command

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
            self.xCommand.run()

    def stop(self):
        print("OI Stop")
        self.controller.stop()
