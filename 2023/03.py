"""
--- Day 3: Gear Ratios ---
"""


import re
import math
from collections import defaultdict


EXAMPLES1 = (
    ('03-exemple1.txt', 4361),
)

EXAMPLES2 = (
    ('03-exemple1.txt', 467835),
)

INPUT = '03.txt'


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()

    return [_.strip() for _ in lines]


def neighbours(grid, i, j):
    neigh = set()
    for i2 in range(i - 1, i + 2):
        for j2 in range(j - 1, j + 2):
            if (i2, j2) != (i, j) and 0 <= i2 < len(grid) and 0 <= j2 < len(grid[0]):
                neigh.add((i2, j2))
    return neigh


def hseg_neighbours(grid, i, j1, j2):
    # neighbours of grid[i][j1:j2]
    return set().union(*(neighbours(grid, i, j) for j in range(j1, j2)))


def code1(grid):
    mysum = 0
    for i, line in enumerate(grid):
        for match in re.finditer(r'\d+', line):
            neigh = hseg_neighbours(grid, i, match.start(), match.end())
            if any(grid[i2][j2] not in '0123456789.' for i2, j2 in neigh):
                mysum += int(match.group(0))
    return mysum


def code2(grid):
    stars = defaultdict(set)
    for i, line in enumerate(grid):
        for match in re.finditer(r'\d+', line):
            neigh = hseg_neighbours(grid, i, match.start(), match.end())
            for i2, j2 in neigh:
                if grid[i2][j2] == '*':
                    stars[(i2, j2)].add((i, match.start(), int(match.group(0))))
    mysum = 0
    for starneighbours in stars.values():
        if len(starneighbours) == 2:  # == 2 or >= 2 give same results here
            mysum += math.prod(value for _, _, value in starneighbours)
    return mysum


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
