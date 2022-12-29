"""
--- 2018 --- Day 25: Four-Dimensional Adventure ---
"""


import functools


EXAMPLES1 = (
    ('25-exemple1.txt', 2),
    ('25-exemple2.txt', 4),
)

EXAMPLES2 = (
)

INPUT = '25.txt'


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()
    points = []
    for line in lines:
        point = tuple(int(_) for _ in line.strip().split(','))
        points.append(point)
    return points


def distance(point1, point2):
    return sum(abs(x - y) for x, y in zip(point1, point2))


def belongs(point, constellation):
    for point2 in constellation:
        if distance(point, point2) <= 3:
            return True
    return False


def code1(points):
    constellations = []
    for point in points:
        point_constellations = []
        for constellation in constellations:
            if belongs(point, constellation):
                constellation.add(point)
                point_constellations.append(constellation)
        if not point_constellations:
            constellations.append({point})
        else:
            new_constellation = functools.reduce(lambda x, y: x.union(y), point_constellations)
            for constellation in point_constellations:
                constellations.remove(constellation)
            constellations.append(new_constellation)
    return len(constellations)


def code2(data):
    return None


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
