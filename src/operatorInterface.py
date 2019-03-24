#!/usr/bin/python3

import asyncio
import threading
from hardware import Controller
from commands import SonicCommand, StopCommand, EncoderCommand, GyroCommand, VelocityCommand, PursuitCommand


class OperatorInterface():

    def __init__(self, drive):
        self.drive = drive
        self.controller = Controller()
        loop = asyncio.get_event_loop()
        t = threading.Thread(target=self.controller.start, args=(loop,))
        t.start()

        self.bindCommands()

    def bindCommands(self):
        aCommand = EncoderCommand(self.drive, 24)
        self.bindCommand('BTN_A', aCommand)

        xCommand = SonicCommand(self.drive, 12)
        self.bindCommand('BTN_X', xCommand)

        yCommand = GyroCommand(self.drive, 45)
        self.bindCommand('BTN_Y', yCommand)

        bCommand = VelocityCommand(self.drive, 12)
        self.bindCommand('BTN_B', bCommand)

        stopCommand = StopCommand(self)
        self.bindCommand('BTN_SELECT', stopCommand)

        pursuitCommand = PursuitCommand(self.drive)
        self.bindCommand('BTN_START', pursuitCommand)

    def bindCommand(self, button, command):
        self.controller.bindCommand(button, command.run)

    def getLeft(self):
        return self.controller.leftY

    def getRight(self):
        return self.controller.rightY

    def stop(self):
        print("OI Stop")
        self.controller.stop()
