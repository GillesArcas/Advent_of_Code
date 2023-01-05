"""
--- 2015 --- Day 2: I Was Told There Would Be No Math ---
"""


import re


EXAMPLES1 = (
    ('02-exemple1.txt', 58 + 43),
)

EXAMPLES2 = (
    ('02-exemple1.txt', 34 + 14),
)

INPUT = '02.txt'


def read_data(filename):
    with open(filename) as f:
        return [[int(n) for n in re.findall(r'\d+', line)] for line in f.readlines()]


def code1(dimensions):
    total = 0
    for x, y, z in dimensions:
        sides = x * y, y * z, x * z
        total += 2 * (sides[0] + sides[1] + sides[2]) + min(sides)
    return total


def code2(dimensions):
    total = 0
    for x, y, z in dimensions:
        perimeters = 2 * (x + y), 2 * (y + z), 2 * (x + z)
        total += min(perimeters) + x * y * z
    return total


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
