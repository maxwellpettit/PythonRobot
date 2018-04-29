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
        gyroData = self.mpu.get_gyro_data()
        gz = gyroData['z']

        t = time.time()
        self.yaw += (gz - self.GYRO_Z_OFFSET) * (t - self.lastTime)

        # print("gz = " + str(gz))
        # print("Yaw = " + str(self.yaw))

        self.lastTime = t