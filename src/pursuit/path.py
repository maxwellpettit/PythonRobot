#!/usr/bin/python3

from pursuit import PathSegment


class Path():

    COMPLETION_TOLERANCE = 0.98

    segments = []

    def addSegment(self, segment):
        self.segments.append(segment)

    def findGoalPoint(self, xv, yv, lookahead):
        """
        Find the goal point on the path for the current vehicle position
        """
        while (len(self.segments) > 0):
            segment = self.segments[0]

            # Find first path segment where d >= lookahead
            d = PathSegment.getDistance(xv, yv, segment.x2, segment.y2)
            if (d >= lookahead):
                # Find closest point on path segment
                (x, y, index) = segment.findClosestPoint(xv, yv)

                # Check if vehicle closer to next segment
                (x, y, index, segment) = self.checkNextSegment(xv, yv, x, y, index, segment)

                # Check if segment is complete
                self.checkSegmentComplete(index)

                print('Closest (x, y) = (' + str(x) + ', ' + str(y) + ') Index = ' + str(index))

                # Find intersection between path and circle with radius = lookahead
                return segment.findCircleIntersection(x, y, lookahead)

            # If last segment, return the end of the segment
            elif (len(self.segments) == 1):
                # Find closest point on path segment
                (x, y, index) = segment.findClosestPoint(xv, yv)

                # Check if segment is complete
                self.checkSegmentComplete(index)

                # Goal point is the end of the segment
                return (segment.x2, segment.y2)

            # If too close to end of path, move to next segment
            else:
                print('Distance to path < lookahead. Removing segment.')
                self.segments.pop(0)

        return (None, None)

    def checkNextSegment(self, xv, yv, x, y, index, segment):
        """
        Check if the next segment is closer to the vehicle
        """
        if (len(self.segments) > 1):
            (x2, y2, index2) = self.segments[1].findClosestPoint(xv, yv)
            d1 = PathSegment.getDistance(xv, yv, x, y)
            d2 = PathSegment.getDistance(xv, yv, x2, y2)

            # Next segment is closer, so remove previous segment
            if (d2 <= d1 and index2 > 0):
                segment = self.segments[1]
                (x, y, index) = (x2, y2, index2)

                self.segments.pop(0)
                print('Next Segment is closer. Removing previous segment.')

        return (x, y, index, segment)

    def checkSegmentComplete(self, index):
        if (index >= self.COMPLETION_TOLERANCE):
            self.segments.pop(0)
            print('Segment Complete')
