#!/usr/bin/python3

import math

class PoseEstimator():

    poseX = 0.0
    poseY = 0.0
    poseHeading = 0.0

    prevLeftDistance = 0.0
    prevRightDistance = 0.0

    count = 0

    def update(self, leftDistance, rightDistance, heading):

        centerDistance = (leftDistance - self.prevLeftDistance + rightDistance - self.prevRightDistance) / 2

        # Approximate X, Y coordinates using right triangle
        self.poseX += centerDistance * math.cos(heading)
        self.poseY += centerDistance * math.sin(heading)

        self.poseHeading = heading
        self.prevLeftDistance = leftDistance
        self.prevRightDistance = rightDistance

        self.count += 1
        if (self.count == 20):
            print('Pose: (' + self.poseX + ', ' + self.poseY + ', ' + self.poseHeading + ')')
            self.count = 0
            
    def getPose(self):
        return self.poseX, self.poseY, self.poseHeading
