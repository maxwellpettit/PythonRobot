#!/usr/bin/python3

class StopCommand():

    def __init__(self, robot):
        self.robot = robot

    def run(self):
        self.robot.stop()
