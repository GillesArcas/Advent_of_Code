"""
--- 2022 --- Day 18: Boiling Boulders ---
"""


EXAMPLES1 = (
    ('18-exemple1.txt', 64),
)

EXAMPLES2 = (
    ('18-exemple1.txt', 58),
)

INPUT = '18.txt'


def read_data(filename):
    with open(filename) as f:
        data = [tuple(int(_) for _ in line.strip().split(',')) for line in f.readlines()]

    xmin = min(x for x, y, z in data) - 1
    xmax = max(x for x, y, z in data) + 1
    ymin = min(y for x, y, z in data) - 1
    ymax = max(y for x, y, z in data) + 1
    zmin = min(z for x, y, z in data) - 1
    zmax = max(z for x, y, z in data) + 1

    space = {x: {y: {z: 0 for z in range(zmin, zmax + 1)} for y in range(ymin, ymax + 1)} for x in range(xmin, xmax + 1)}

    for x, y, z in data:
        space[x][y][z] = 1

    return xmin, xmax, ymin, ymax, zmin, zmax, space


def code1(data):
    xmin, xmax, ymin, ymax, zmin, zmax, space = data
    count = 0

    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            for z in range(zmin, zmax + 1):
                if space[x][y][z] == 1:
                    for x2, y2, z2 in ((x - 1, y, z), (x + 1, y, z),
                                       (x, y - 1, z), (x, y + 1, z),
                                       (x, y, z - 1), (x, y, z + 1)):
                        if space[x2][y2][z2] == 0:
                            count += 1

    return count


def mark_outside(xmin, xmax, ymin, ymax, zmin, zmax, space):
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            for z in range(zmin, zmax + 1):
                if x == xmin or x == xmax or y == ymin or y == ymax or z == zmin or z == zmax:
                    space[x][y][z] = 2

    changed = True
    while changed:
        changed = False
        for x in range(xmin + 1, xmax):
            for y in range(ymin + 1, ymax):
                for z in range(zmin + 1, zmax):
                    if space[x][y][z] == 0:
                        for x2, y2, z2 in ((x - 1, y, z), (x + 1, y, z),
                                           (x, y - 1, z), (x, y + 1, z),
                                           (x, y, z - 1), (x, y, z + 1)):
                            if space[x2][y2][z2] == 2:
                                space[x][y][z] = 2
                                changed = True


def code2(data):
    xmin, xmax, ymin, ymax, zmin, zmax, space = data
    mark_outside(xmin, xmax, ymin, ymax, zmin, zmax, space)
    count = 0

    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            for z in range(zmin, zmax + 1):
                if space[x][y][z] == 1:
                    for x2, y2, z2 in ((x - 1, y, z), (x + 1, y, z),
                                       (x, y - 1, z), (x, y + 1, z),
                                       (x, y, z - 1), (x, y, z + 1)):
                        if space[x2][y2][z2] == 2:
                            count += 1

    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
