from pursuit import Path, PathSegment, PursuitController


def main():
    (seg1, seg2, seg3) = path1()
    #(seg1, seg2, seg3) = path2()
    path = Path()
    path.addSegment(seg1)
    path.addSegment(seg2)
    path.addSegment(seg3)

    pursuit = PursuitController(path, 4, 8)
    pursuit.PID_FREQUENCY = 1
    pursuit.left.pid.kP = 0
    pursuit.right.pid.kP = 0

    updatePath1(pursuit)
    # updatePath2(pursuit)

    #testSegment()


def path1():
    seg1 = PathSegment(0, 0, 0, 36)
    seg2 = PathSegment(0, 36, 36, 36)
    seg3 = PathSegment(36, 36, 48, 48)
    return (seg1, seg2, seg3)


def updatePath1(pursuit):
    update(pursuit, 0, 0, 90)
    update(pursuit, 0, 4, 90)
    update(pursuit, 0, 30, 90)
    update(pursuit, -1, 35, 90)
    update(pursuit, 4, 36, 0)
    update(pursuit, 30, 36, 0)


def path2():
    seg1 = PathSegment(0, 0, 12, 12)
    seg2 = PathSegment(12, 12, 0, 24)
    seg3 = PathSegment(0, 24, 12, 36)
    return (seg1, seg2, seg3)


def updatePath2(pursuit):
    update(pursuit, 0, 0, 90)
    update(pursuit, 4, 4, 45)
    update(pursuit, 8, 8, 45)
    update(pursuit, 8, 16, 135)
    update(pursuit, 4, 20, 135)
    update(pursuit, 2, 21, 135)


def update(pursuit, x, y, heading):
    (left, right) = pursuit.calculate(x, y, heading, 0, 0)
    print('Output = (' + str(left) + ' ' + str(right) + ')')


def testSegment():
    print('')

    seg1 = PathSegment(0, 10, 10, 10)
    print(str(seg1.a) + ' ' + str(seg1.b) + ' ' + str(seg1.c))

    (x, y, index) = seg1.findClosestPoint(-1, 9)
    print(str(x) + ' ' + str(y))

    (x, y) = seg1.findCircleIntersection(x, y, 5)
    print(str(x) + ' ' + str(y) + ' ' + str(index))


if __name__ == '__main__':
    main()
