#!/usr/bin/python3

import time
import math
from hardware import SimpleMpu6050

class SimpleGyro():

    # Measured average gyro z value when sensor at rest
    GYRO_Z_OFFSET = 0.75

    yaw = 0

    # Sensor initialization
    def __init__(self):
        self.mpu = SimpleMpu6050(0x68)
        self.lastTime = time.time()

    def update(self):
        try:
            gyroData = self.mpu.get_gyro_data()
            t = time.time()
            
            self.yaw += (gyroData['z'] - self.GYRO_Z_OFFSET) * (t - self.lastTime)
            self.lastTime = t

        except:
            print("I2C Read Error")