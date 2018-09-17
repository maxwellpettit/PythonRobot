#!/usr/bin/python3

from math import cos, sin, radians

class PoseEstimator():

    poseX = 0.0
    poseY = 0.0
    poseHeading = 0.0

    prevLeftDistance = 0.0
    prevRightDistance = 0.0

    def update(self, leftDistance, rightDistance, heading):

        centerDistance = (leftDistance - self.prevLeftDistance + rightDistance - self.prevRightDistance) / 2.0

        # Approximate X, Y coordinates using right triangle
        self.poseX += centerDistance * cos(radians(heading))
        self.poseY += centerDistance * sin(radians(heading))

        self.poseHeading = heading
        self.prevLeftDistance = leftDistance
        self.prevRightDistance = rightDistance

    def getPose(self):
        return self.poseX, self.poseY, self.poseHeading
