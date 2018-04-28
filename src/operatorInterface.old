#!/usr/bin/python3

from hardware import XboxController

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

    def setACommand(self, command):
        self.aCommand = command

    def setXCommand(self, command):
        self.xCommand = command

    def setBCommand(self, command):
        self.bCommand = command

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
        if (controlId == 8 and value == 1):
            print("X Button - " + str(value))
            self.xCommand.run()
        if (controlId == 7 and value == 1):
            print("B Button - " + str(value))
            self.bCommand.run()
        if (controlId == 6 and value == 1):
            print("A Button - " + str(value))
            self.aCommand.run()

    def stop(self):
        print("OI Stop")
        self.controller.stop()
