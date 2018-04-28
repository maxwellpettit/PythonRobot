#!/usr/bin/python3

import time
import math
from hardware import MPU6050

class Gyro():

    yaw = 0

    # Sensor initialization
    def __init__(self):
        self.mpu = MPU6050()
        self.mpu.dmpInitialize()
        self.mpu.setDMPEnabled(True)

        self.mpu.setXGyroOffsetUser(8)
        self.mpu.setYGyroOffsetUser(-95)
        self.mpu.setZGyroOffsetUser(-23)

        # get expected DMP packet size for later comparison
        self.packetSize = self.mpu.dmpGetFIFOPacketSize()

    def update(self):
        # Get INT_STATUS byte
        mpuIntStatus = self.mpu.getIntStatus()

        if mpuIntStatus >= 2: # check for DMP data ready interrupt (this should happen frequently)
            # get current FIFO count
            fifoCount = self.mpu.getFIFOCount()

            # check for overflow (this should never happen unless our code is too inefficient)
            if fifoCount == 1024:
                # reset so we can continue cleanly
                self.mpu.resetFIFO()

            # wait for correct available data length, should be a VERY short wait
            fifoCount = self.mpu.getFIFOCount()
            while fifoCount < self.packetSize:
                fifoCount = self.mpu.getFIFOCount()

            result = self.mpu.getFIFOBytes(self.packetSize)
            q = self.mpu.dmpGetQuaternion(result)
            g = self.mpu.dmpGetGravity(q)
            ypr = self.mpu.dmpGetYawPitchRoll(q, g)

            self.yaw = ypr['yaw'] * 180 / math.pi
            # pitch = ypr['pitch'] * 180 / math.pi
            # roll = ypr['roll'] * 180 / math.pi
            
            # print("Yaw: " + str(self.yaw))
            # print("Pitch: " + str(pitch))
            # print("Roll: " + str(roll))

            # track FIFO count here in case there is > 1 packet available
            # (this lets us immediately read more without waiting for an interrupt)        
            fifoCount -= self.packetSize