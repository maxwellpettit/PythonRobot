from pursuit import Path, PathSegment, PursuitController
from control import VelocityController


def main():
    seg1 = PathSegment(0, 0, 0, -5)
    seg2 = PathSegment(0, -5, 5, -5)
    seg3 = PathSegment(5, -5, 7, -7)
    path = Path()
    path.addSegment(seg1)
    path.addSegment(seg2)
    path.addSegment(seg3)

    pursuit = PursuitController(path, 2, 10)
    pursuit.PID_FREQUENCY = 1
    update(pursuit, 0, 0, 90)
    update(pursuit, 0, -2, 90)
    update(pursuit, 0, -4, 90)
    update(pursuit, 0, -5, 0)
    update(pursuit, 2, -5, 0)
    update(pursuit, 4, -5, 0)


def update(pursuit, x, y, heading):
    print('(x, y) = (' + str(x) + ', ' + str(y) + ')')
    (left, right) = pursuit.calculate(x, y, heading, 0, 0)
    print('Output = (' + str(left) + ' ' + str(right) + ')')
    print('')


if __name__ == '__main__':
    main()