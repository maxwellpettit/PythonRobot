#!/bin/python

import datetime, threading, time, traceback
from drive import Drive
from operatorInterface import OperatorInterface
from pidController import PidController

class Robot():

    PERIODIC_DELAY = 0.1

    DISTANCE_KP = 0.1
    DISTANCE_KI = 0
    DISTANCE_KD = 0

    stopped = False

    def __init__(self):
        self.oi = OperatorInterface()
        self.drive = Drive(self.oi)

        # Test distance PID
        pid = PidController(self.DISTANCE_KP, self.DISTANCE_KI, self.DISTANCE_KD)
        self.drive.setAutoMode(20, pid)

    def update(self):
        self.drive.update()

    def stop(self):
        self.stopped = True
        self.drive.stop()
        self.oi.stop()

    def periodic(self):
        next = time.time()
        while (not self.stopped):
            try:
                self.update()

                print(datetime.datetime.now())
                next = next + self.PERIODIC_DELAY
                time.sleep(max(0, next - time.time()))
            except:
                print("Exception in Periodic")
                traceback.print_exc()
                self.stop()


# Main function that initializes the robot and periodically updates the robot
def main():
    robot = Robot()

    updateThread = threading.Thread(target=robot.periodic)
    updateThread.start()

    try:
        while (updateThread.isAlive()):
            updateThread.join(1)

    except KeyboardInterrupt:
        print("Stopped Via Keyboard")
        robot.stop()

    except:
        print("Stopped Via Unknown Exception")
        robot.stop()

if __name__ == '__main__':
    main()
