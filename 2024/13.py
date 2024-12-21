"""
--- Day 13: Claw Contraption ---
"""


import re
import numpy as np


EXAMPLES1 = (
    ('13-exemple1.txt', 480),
)

EXAMPLES2 = (
)

INPUT = '13.txt'


PATTERN = \
r"""Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)
"""


def read_data(filename):
    with open(filename) as f:
        text = f.read()
        for match in re.findall(PATTERN, text):
            yield [int(_) for _ in match]


def solveprize(ax, ay, bx, by, px, py, iterlimit):
    # unreachable for part 2
    for ia in range(iterlimit):
        for ib in range(iterlimit):
            if ia * ax + ib * bx == px and ia * ay + ib * by == py:
                return ia, ib
    return None


def solveprize(ax, ay, bx, by, px, py):
    # rouding errors
    a = np.array([[ax, bx], [ay, by]])
    b = np.array([px, py])
    r = np.linalg.solve(a, b)
    if r[0] % 1 == 0 and r[1] % 1 == 0:
        tokens += 3 * r[0] + r[1]
    return tokens


def solveprize(ax, ay, bx, by, px, py):
    a = np.array([[ax, bx], [ay, by]])
    b = np.array([px, py])
    r = np.linalg.solve(a, b)
    na = int(r[0])
    nb = int(r[1])
    for ia in range(na - 10, na + 10):
        for ib in range(nb - 10, nb + 10):
            if ia * ax + ib * bx == px and ia * ay + ib * by == py:
                return ia, ib
    return None


def solvecode(data, offset):
    data = [(ax, ay, bx, by, offset + px, offset + py) for ax, ay, bx, by, px, py in data]
    tokens = 0
    for x in data:
        r = solveprize(*x)
        if r:
            ia, ib = r
            tokens += 3 * ia + ib
    return tokens


def code1(data):
    return solvecode(data, 0)


def code2(data):
    return solvecode(data, 10000000000000)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
