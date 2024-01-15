"""
--- Day 24: Never Tell Me The Odds ---

Part 2:

Search for X, Y, Z, DX, DY, DZ such as for every x, y, z, dx, dy, dz, it exists
t such as:

x + tdx = X + tDX
y + tdy = Y + tDY
z + tdz = Z + tDZ

t = -(x - X) / (dx - DX) = -(y - Y) / (dy - DY) = -(z - Z) / (dz - DZ)

which gives 3 equations without t:

(x - X) / (dx - DX) = (y - Y) / (dy - DY)
(x - X) / (dx - DX) = (z - Z) / (dz - DZ)
(y - Y) / (dy - DY) = (z - Z) / (dz - DZ)

or:

(x - X) * (dy - DY) - (y - Y) * (dx - DX) = 0
(x - X) * (dz - DZ) - (z - Z) * (dx - DX) = 0
(y - Y) * (dz - DZ) - (z - Z) * (dy - DY) = 0

-dyX + dxY + yDX - xDY + XDY - YDX = -xdy + ydx
-dzX + dxZ + zDX - xDZ + XDZ - ZDX = -xdz + zdx
-dzY + dyZ + zDY - yDZ + YDZ - ZDY = -ydz + zdy

They are 12 unknowns: X, Y, Z, DX, DY, DZ plus all products XDX, etc.

Using 4 hailstones gives 12 linear equations with 12 unknowns.

The terms XDY - YDX, etc. are constant for all hailstones. They are eliminated
by making the difference of the formulas for two hailstones.

      -dyX + dxY + yDX - xDY + XDY - YDX       =      -xdy + ydx
   - (-dy'X + dx'Y + y'DX - x'DY + XDY - YDX)     - (-x'dy' + y'dx')

(dy' - dy)X + (dx - dx')Y + (y - y')DX + (x' - x)DY = x'dy' - xdy + ydx - y'dx'
(dz' - dz)X + (dx - dx')Z + (z - z')DX + (x' - x)DZ = x'dz' - xdz + zdx - z'dx'
(dz' - dz)Y + (dy - dy')Z + (z - z')DY + (y' - y)DZ = y'dz' - ydz + zdy - z'dy'

Using two pairs of hailstones gives 6 equations with 6 unknowns.

Solving rounding errors is done by finding the most common result for a set of
input hailstones. Both approaches (6 or 12 equations) have rounding problems
although using 6 equations has less dispersion around the correct result.
"""


import re
import itertools
from collections import Counter
import numpy as np


EXAMPLES1 = (
    ('24-exemple1.txt', 2),
)

EXAMPLES2 = (
    ('24-exemple1.txt', 47),
)

INPUT = '24.txt'


def read_data(filename):
    with open(filename) as f:
        data = re.findall(r'(\d+), (\d+), (\d+) @ +(-?\d+), +(-?\d+), +(-?\d+)', f.read())
    data = [[int(_) for _ in elem] for elem in data]
    return data


def inter(a1, b1, a2, b2):
    if a1 == a2:
        return None
    else:
        return (b2 - b1) / (a1 - a2), (a1 * b2 - a2 * b1) / (a1 - a2)


def code1(data):
    coeff = [(float(dy) / dx, y - float(dy) / dx * x, x, y, dx, dy) for (x, y, _, dx, dy, _) in data]
    if len(data) == 5:
        cmin, cmax = 7, 27
    else:
        cmin, cmax = 200000000000000, 400000000000000

    count = 0
    for coeff1, coeff2 in itertools.combinations(coeff, 2):
        a1, b1, x1, y1, dx1, dy1 = coeff1
        a2, b2, x2, y2, dx2, dy2 = coeff2
        res = inter(a1, b1, a2, b2)
        if res is not None:
            x, y = res
            t1 = (x - x1) / dx1
            t2 = (x - x2) / dx2

            if cmin <= x <= cmax and cmin <= y <= cmax and t1 >= 0 and t2 >= 0:
                count += 1

    return count


def add_hailstone_to_equation_v1(x, y, z, dx, dy, dz, a:list, b:list):
    """
    -dyX + dxY +  0Z + yDX - xDY + 0DZ +  1XDY + 0XDZ - 1YDX + 0YDZ + 0ZDX + 0ZDY = -xdy + ydx
    -dzX +  0Y + dxZ + zDX + 0DY - xDZ +  0XDY + 1XDZ + 0YDX + 0YDZ - 1ZDX + 0ZDY = -xdz + zdx
      0X - dzY + dyZ + 0DX + zDY - yDZ +  0XDY + 0XDZ + 0YDX + 1YDZ + 0ZDX - 1ZDY = -ydz + zdy
    """
    a.append((-dy,  dx,  0, y, -x,  0, 1, 0, -1, 0,  0,  0))
    a.append((-dz,   0, dx, z,  0, -x, 0, 1,  0, 0, -1,  0))
    a.append((  0, -dz, dy, 0,  z, -y, 0, 0,  0, 1,  0, -1))

    b.append(-x * dy + y * dx)
    b.append(-x * dz + z * dx)
    b.append(-y * dz + z * dy)


def add_hailstone_to_equation_v2(x, y, z, dx, dy, dz, x2, y2, z2, dx2, dy2, dz2, a:list, b:list):
    """
    (dy2 - dy)X + (dx - dx2)Y +          0Z + (y - y2)DX + (x2 - x)DY +        0DZ = x2dy2 - xdy + ydx - y2dx2
    (dz2 - dz)X +          0Y + (dx - dx2)Z + (z - z2)DX +        0DY + (x2 - x)DZ = x2dz2 - xdz + zdx - z2dx2
             0X + (dz2 - dz)Y + (dy - dy2)Z +        0DX + (z - z2)DY + (y2 - y)DZ = y2dz2 - ydz + zdy - z2dy2
    """
    a.append(((dy2 - dy), (dx - dx2),          0, (y - y2), (x2 - x),        0))
    a.append(((dz2 - dz),          0, (dx - dx2), (z - z2),        0, (x2 - x)))
    a.append((         0, (dz2 - dz), (dy - dy2),        0, (z - z2), (y2 - y)))

    b.append(x2 * dy2 - x * dy + y * dx - y2 * dx2)
    b.append(x2 * dz2 - x * dz + z * dx - z2 * dx2)
    b.append(y2 * dz2 - y * dz + z * dy - z2 * dy2)


def code2_v1(data):
    coeff = data
    count = Counter()

    for _, vec in zip(range(1000), itertools.combinations(coeff, 4)):
        a = []
        b = []
        for c in vec:
            add_hailstone_to_equation_v1(*c[:6], a, b)

        if np.linalg.det(a) != 0:
            sol = np.linalg.solve(a, b)
            X, Y, Z = [int(round(_)) for _ in sol[:3]]
            count.update((X + Y + Z,))

    print(count.most_common(5))
    return count.most_common(1)[0][0]


def code2_v2(data):
    coeff = data
    count = Counter()

    for _, vec in zip(range(1000), itertools.combinations(coeff, 3)):
        a = []
        b = []
        add_hailstone_to_equation_v2(*vec[0][:6], *vec[1][:6], a, b)
        add_hailstone_to_equation_v2(*vec[0][:6], *vec[2][:6], a, b)

        if np.linalg.det(a) != 0:
            sol = np.linalg.solve(a, b)
            X, Y, Z = [int(round(_)) for _ in sol[:3]]
            count.update((X + Y + Z,))

    print(count.most_common(5))
    return count.most_common(1)[0][0]


def test(n, code, examples, myinput):
    for fn, expected in examples:
        print(fn)
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


code2 = code2_v2

test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
