import re
from collections import defaultdict


REGEXP = 'position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>'

def get_data(n):
    data = {0: '10.txt', 1: '10-exemple1.txt'}
    points = list()
    with open(data[n]) as f:
        for line in f:
            match = re.match(REGEXP, line)
            points.append([int(_) for _ in match.group(1, 2, 3, 4)])
    return points


def display_area(points):
    area = defaultdict(lambda: defaultdict(int))
    for x, y, vx, vy in points:
        area[x][y] = 1
    xmin = min(point[0] for point in points)
    xmax = max(point[0] for point in points)
    ymin = min(point[1] for point in points)
    ymax = max(point[1] for point in points)
    for y in range(ymin, ymax + 1):
        print(''.join('#' if area[x][y] else '.' for x in range(xmin, xmax + 1)))
    print()


def code():
    points = get_data(0)
    #display_area(points)
    heightmin = float('inf')
    seconds = 0
    while 1:
        seconds += 1
        # ending test is minimum height
        for index, (x, y, vx, vy) in enumerate(points):
            points[index] = (x + vx, y + vy, vx, vy)

        ymin = min(point[1] for point in points)
        ymax = max(point[1] for point in points)
        height = ymax - ymin + 1
        if height < heightmin:
            heightmin = height
        if height > heightmin:
            for index, (x, y, vx, vy) in enumerate(points):
                points[index] = (x - vx, y - vy, vx, vy)
            display_area(points)
            print('seconds:', seconds - 1)
            break


code()
