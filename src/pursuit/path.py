#!/usr/bin/python3

from math import sqrt, cos, sin
from pursuit import PathSegment


class Path():

    segments = []

    def addSegment(self, segment):
        self.segments.append(segment)

    def findGoalPoint(self, xv, yv, lookahead):
        s = 0
        while (len(self.segments) > s):
            segment = self.segments[s]
            d = PathSegment.getDistance(xv, yv, segment.x2, segment.y2)

            if (d >= lookahead):
                (x, y, index) = segment.findClosestPoint(xv, yv)

                if (len(self.segments) > (s + 1)):
                    (x2, y2, index2) = self.segments[1].findClosestPoint(xv, yv)
                    d1 = PathSegment.getDistance(xv, yv, x, y)
                    d2 = PathSegment.getDistance(xv, yv, x2, y2)
                    if (d2 <= d1 and index2 > 0):
                        segment = self.segments[s + 1]
                        (x, y, index) = (x2, y2, index2)

                        for i in range(0, s + 1):
                            self.segments.pop(i)
                            print('Removing segment ' + str(i))

                print('Closest (x, y) = (' + str(x) + ', ' + str(y) + ')')
                return segment.findFirstCircleIntersection(x, y, lookahead)

            s += 1

        return (None, None)
