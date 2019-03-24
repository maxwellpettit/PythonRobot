#!/usr/bin/python3

import threading
import time
import traceback
from drive import Drive
from operatorInterface import OperatorInterface


class Robot():

    # 100 ms update (stable frequency) / 50 ms update (maximum frequency)
    PERIODIC_DELAY = 0.05

    stopped = False

    def __init__(self):
        self.drive = Drive()
        self.oi = OperatorInterface(self.drive)
        self.drive.setOperatorInterface(self.oi)

    def update(self):
        self.drive.update()

    def stop(self):
        self.stopped = True
        self.drive.stop()
        self.oi.stop()

    def periodic(self):
        nextTime = time.time()
        while (not self.stopped):
            try:
                self.update()

                nextTime = nextTime + self.PERIODIC_DELAY
                delay = max(0, nextTime - time.time())
                if (delay == 0):
                    print("--------------THRASH--------------")
                time.sleep(delay)
            except:
                print("Exception in Periodic")
                traceback.print_exc()
                self.stop()


def main():
    """
    Main function that initializes the robot and periodically updates the robot
    """

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
        traceback.print_exc()
        robot.stop()


if __name__ == '__main__':
    main()
