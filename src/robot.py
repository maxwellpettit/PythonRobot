#!/usr/bin/python3

import datetime, threading, time, traceback
from drive import Drive
from operatorInterface import OperatorInterface
from commands import SonicCommand, StopCommand, EncoderCommand, GyroCommand

class Robot():

    # 100 ms update loop (stable)
    PERIODIC_DELAY = 0.05

    stopped = False

    def __init__(self):
        self.oi = OperatorInterface()
        self.drive = Drive(self.oi)

        aCommand = EncoderCommand(self.drive, 24)
        self.oi.bindCommand('BTN_A', aCommand)

        xCommand = SonicCommand(self.drive, 12)
        self.oi.bindCommand('BTN_X', xCommand)

        yCommand = GyroCommand(self.drive, 45)
        self.oi.bindCommand('BTN_Y', yCommand)

        stopCommand = StopCommand(self)
        self.oi.bindCommand('BTN_B', stopCommand)

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

                next = next + self.PERIODIC_DELAY
                delay = max(0, next - time.time())
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
