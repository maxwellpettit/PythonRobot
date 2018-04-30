#!/usr/bin/python3

import asyncio, threading
from hardware import Controller

class OperatorInterface():

    def __init__(self):
        self.controller = Controller()
        loop = asyncio.get_event_loop()
        t = threading.Thread(target=self.controller.start, args=(loop,))
        t.start()

    def bindCommand(self, button, command):
        self.controller.bindCommand(button, command.run)

    def getLeft(self):
        return self.controller.leftY

    def getRight(self):
        return self.controller.rightY

    def stop(self):
        print("OI Stop")
        self.controller.stop()
