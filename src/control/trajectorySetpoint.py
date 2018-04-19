#!/bin/python

class TrajectorySetpoint:

    def __init__(self, time, distance, velocity, acceleration, heading):
        self.time = time
        self.distance = distance
        self.velocity = velocity
        self.acceleration = acceleration
        self.heading = heading