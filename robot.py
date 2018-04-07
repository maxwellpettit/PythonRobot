#!/bin/python

import datetime, threading, time
from drive import Drive
#from operatorInterface import OperatorInterface

class Robot():

    PERIODIC_DELAY = 0.1

    stopped = False

    def __init__(self):
        self.oi = 0 # = OperatorInterface()
        self.drive = Drive(self.oi)

    def update(self):
        self.drive.update()
    
    def stop(self):
        self.stopped = True
        self.drive.stop()
        #self.oi.stop()

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