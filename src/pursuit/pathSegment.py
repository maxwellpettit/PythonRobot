#!/usr/bin/python3

from math import sqrt


class PathSegment():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.dx = x2 - x1
        self.dy = y2 - y1

        self.calculateStandard()
        self.length = self.getDistance(x1, y1, x2, y2)

    def calculateStandard(self):
        """
        Calculate the standard form for the line segment 
        (i.e. ax + by + c = 0)
        """
        self.a = self.y1 - self.y2
        self.b = self.x2 - self.x1
        self.c = -(self.a * self.x1 + self.b * self.y1)

    @staticmethod
    def getDistance(x1, y1, x2, y2):
        """
        Calculate the distance between two points
        """
        return sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def dotProduct(self, x, y):
        """
        Calculate the dot product of vectors (x-x1, y-y1) and (x2-x1, y2-y1)
        """
        dx = x - self.x1
        dy = y - self.y1
        return self.dx * dx + self.dy * dy

    def findClosestPoint(self, xv, yv):
        """
        Find point on path segment closest to vehicle
        https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
        """
        den = self.a**2 + self.b**2
        x = (self.b * (self.b * xv - self.a * yv) - self.a * self.c) / den
        y = (self.a * (-self.b * xv + self.a * yv) - self.b * self.c) / den

        # Calculate the percentage completed of the segment
        index = self.dotProduct(x, y) / (self.length**2)

        return (x, y, index)

    def findCircleIntersection(self, x, y, radius):
        """
        Find intersection between path segment and a circle. 
        (x, y) = closest point on path to vehicle, 
        radius = lookahead distance
        http://mathworld.wolfram.com/Circle-LineIntersection.html
        """
        x1 = self.x1 - x
        y1 = self.y1 - y
        x2 = self.x2 - x
        y2 = self.y2 - y
        dx = x2 - x1
        dy = y2 - y1
        dr2 = dx * dx + dy * dy
        det = x1 * y2 - x2 * y1

        discrim = dr2 * radius * radius - det * det
        if (discrim >= 0):
            sqrtDiscrim = sqrt(discrim)
            sign = -1 if (dy < 0) else 1

            posX = (det * dy + sign * dx * sqrtDiscrim) / dr2 + x
            posY = (-det * dx + abs(dy) * sqrtDiscrim) / dr2 + y
            negX = (det * dy - sign * dx * sqrtDiscrim) / dr2 + x
            negY = (-det * dx - abs(dy) * sqrtDiscrim) / dr2 + y

            posDot = self.dotProduct(posX, posY)
            negDot = self.dotProduct(negX, negY)

            # print('pos x = ' + str(posX) + ', pos y = ' + str(posY))
            # print('neg x = ' + str(negX) + ', neg y = ' + str(negY))
            # print('posDot = ' + str(posDot))
            # print('negDot = ' + str(negDot))

            # Return the point on the segment closest to the end
            if (posDot < 0 and negDot >= 0):
                return (negX, negY)
            elif (posDot >= 0 and negDot < 0):
                return (posX, posY)
            else:
                dPos = PathSegment.getDistance(self.x2, self.y2, posX, posY)
                dNeg = PathSegment.getDistance(self.x2, self.y2, negX, negY)
                if (dPos < dNeg):
                    return (posX, posY)
                else:
                    return (negX, negY)

        else:
            return (None, None)


def main():
    seg1 = PathSegment(5, 0, 8, -10)
    print(str(seg1.a) + ' ' + str(seg1.b) + ' ' + str(seg1.c))

    (x, y, index) = seg1.findClosestPoint(0, 0)
    print(str(x) + ' ' + str(y))

    (x, y) = seg1.findCircleIntersection(0, 0, 15)
    print(str(x) + ' ' + str(y))


if __name__ == '__main__':
    main()
