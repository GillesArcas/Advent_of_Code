"""
--- 2018 --- Day 23: Experimental Emergency Teleportation ---
"""


import re


EXAMPLES1 = (
    ('23-exemple1.txt', 7),
)

EXAMPLES2 = (
    ('23-exemple2.txt', 36),
)

INPUT = '23.txt'


PATTERN = r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)'


def read_data(filename):
    with open(filename) as f:
        data = [[int(_) for _ in _] for _ in re.findall(PATTERN, f.read())]
    return data


def code1(data):
    vmax, imax = max((v[-1], i) for i, v in enumerate(data))
    xmax, ymax, zmax, rmax = data[imax]
    count = 0
    for x, y, z, _ in data:
        if abs(xmax - x) + abs(ymax - y) + abs(zmax - z) <= rmax:
            count += 1
    return count


def envelope(data):
    xmin, xmax = float('inf'), float('-inf')
    ymin, ymax = float('inf'), float('-inf')
    zmin, zmax = float('inf'), float('-inf')
    for x, y, z, r in data:
        xmin, xmax = min(xmin, x - r), max(xmax, x + r)
        ymin, ymax = min(ymin, y - r), max(ymax, y + r)
        zmin, zmax = min(zmin, z - r), max(zmax, z + r)
    return xmin, xmax, ymin, ymax, zmin, zmax


def cube_in_range(xmin, xmax, ymin, ymax, zmin, zmax, botcoord):
    # one of the vertex of the octant inside octahedron
    x, y, z, r = botcoord
    for xv in (xmin, xmax):
        for yv in (ymin, ymax):
            for zv in (zmin, zmax):
                vertex = xv, yv, zv
                d = abs(xv - x) + abs(yv - y) + abs(zv - z)
                if d <= r:
                    return True
    # center of octant inside octahedron
    d = abs((xmin + xmax) / 2 - x) + abs((ymin + ymax) / 2 - y) + abs((zmin + zmax) / 2 - z)
    if d <= r:
        return True
    # one of the vertex of the octahedron, or its center, inside octant
    vertex = ((x - r, 0, 0), (0, y - r, 0), (0, 0, z - r),
              (x + r, 0, 0), (0, y + r, 0), (0, 0, z + r), (x, y, z))
    for xv, yv, zv in vertex:
        if xmin <= xv <= xmax and ymin <= yv <= ymax and zmin <= zv <= zmax:
            return True
    return False


def bots_in_range(data, octant):
    nbots = 0
    for botcoord in data:
        if cube_in_range(*octant, botcoord):
            nbots += 1
    return nbots


def best_place_in_octant(data, octant):
    xmin, xmax, ymin, ymax, zmin, zmax = octant
    nmax = 0
    dmin = float('inf')

    for xt in range(xmin, xmax + 1):
        for yt in range(ymin, ymax + 1):
            for zt in range(zmin, zmax + 1):

                dt = abs(xt) + abs(yt) + abs(zt)
                n = 0
                for x, y, z, r in data:
                    if abs(xt - x) + abs(yt - y) + abs(zt - z) <= r:
                        n += 1

                if n > nmax:
                    nmax = n
                    dmin = dt
                    pos = xt, yt, zt
                elif n == nmax and nmax > 0:
                    if dt < dmin:
                        dmin = dt
                        pos = xt, yt, zt
    return dmin


# octants to keep at each depth
OCTANTS_TO_KEEP = 1000

# minimum number of bots intersecting with an octant to divide it
MIN_BOTS_TO_DIVIDE = 500


def code2(data):
    # Principle of solution from Eric/Topaz:
    # - subdivision in octants
    # - counting the bot ranges intersecting with octants
    # https://www.reddit.com/r/adventofcode/comments/aa9uvg/day_23_aoc_creators_logic/ecrftas/

    xmin, xmax, ymin, ymax, zmin, zmax = envelope(data)

    depth = 0
    queue = []
    queue.append((depth, xmin, xmax, ymin, ymax, zmin, zmax))
    maxnbots = {}

    while queue:
        depth2, *octant = queue.pop(0)

        if depth2 != depth:
            queue.append((depth2, *octant))
            queue = list(sorted(queue, reverse=True, key=lambda x: bots_in_range(data, x[1:])))[:OCTANTS_TO_KEEP]
            depth2, *octant = queue.pop(0)

        depth = depth2
        xmin, xmax, ymin, ymax, zmin, zmax = octant

        nbots = 0
        for botcoord in data:
            if cube_in_range(*octant, botcoord):
                nbots += 1

        if depth not in maxnbots:
            maxnbots[depth] = (0, None)
        if nbots > maxnbots[depth][0]:
            maxnbots[depth] = (nbots, octant)
            # print(depth, nbots)

        if nbots > MIN_BOTS_TO_DIVIDE and max(xmax - xmin, ymax - ymin, zmax - zmin) > 1:
            xmed = (xmin + xmax) // 2
            ymed = (ymin + ymax) // 2
            zmed = (zmin + zmax) // 2

            for xmin2, xmax2 in ((xmin, xmed), (xmed + 1, xmax)):
                for ymin2, ymax2 in ((ymin, ymed), (ymed + 1, ymax)):
                    for zmin2, zmax2 in ((zmin, zmed), (zmed + 1, zmax)):
                        queue.append((depth + 1, xmin2, xmax2, ymin2, ymax2, zmin2, zmax2))

    return best_place_in_octant(data, maxnbots[depth][1])


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
