import re
import collections


DATA = '06.txt'


def get_data():
    points = list()
    with open(DATA) as f:
        for line in f:
            match = re.match(r'(\d+), (\d+)', line)
            points.append(list(int(_) for _ in match.groups()))

    xmin, xmax = float('inf'), 0
    ymin, ymax = float('inf'), 0
    for x, y in points:
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        ymin = min(ymin, y)
        ymax = max(ymax, y)

    return points, xmin, xmax, ymin, ymax


def nearest_neighbour(point, points):
    dist = dict()
    x, y = point
    for index, (x2, y2) in enumerate(points):
        dist[index] = abs(x - x2) + abs(y - y2)
    dist2 = sorted(dist.items(), key=lambda x: x[1])
    if dist2[0][1] == dist2[1][1]:
        return None  # same distance for the two nearest neighbours
    else:
        return dist2[0][0]


def distance_neighbours(point, points):
    sumdist = 0
    x, y = point
    for x2, y2 in points:
        sumdist += abs(x - x2) + abs(y - y2)
    return sumdist


def code1():
    points, xmin, xmax, ymin, ymax = get_data()

    # an area is infinite if it touches the border of the study area
    infinite = set()

    size = collections.defaultdict(int)
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            nearest = nearest_neighbour((x, y), points)
            if nearest is not None:
                size[nearest] += 1
                if x == xmin or x == xmax or y == ymin or y == ymax:
                    infinite.add(nearest)

    for point in infinite:
        size[point] = 0

    print('1>', max(size.values()))


def code2():
    points, xmin, xmax, ymin, ymax = get_data()

    area10000 = 0
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            sumdist = distance_neighbours((x, y), points)
            if sumdist < 10000:
                area10000 += 1

    print('2>', area10000)


code1()
code2()
