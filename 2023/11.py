"""
--- Day 11: Cosmic Expansion ---
"""


import re
import itertools


EXAMPLES1 = (
    ('11-exemple1.txt', 374),
)

EXAMPLES2 = (
    ('11-exemple1.txt', 1030),
)

INPUT = '11.txt'


def read_data(filename):
    with open(filename) as f:
        return f.read()


def code1(grid):
    # expand empty lines
    grid = re.sub(r'(^\.+$)', r'\1\n\1', grid, flags=re.M)
    grid = grid.splitlines()
    grid = '\n'.join([''.join(_) for _ in zip(*grid)])
    grid = re.sub(r'(^\.+$)', r'\1\n\1', grid, flags=re.M)
    grid = grid.splitlines()
    grid = [''.join(_) for _ in zip(*grid)]

    galaxies = []
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == '#':
                galaxies.append((i, j))

    lensum = 0
    for (i1, j1), (i2, j2) in itertools.combinations(galaxies, 2):
        lensum += abs(i1 - i2) + abs(j1 - j2)
    return lensum


def code2(grid):
    grid = grid.splitlines()
    empty_rows = [all(_ == '.' for _ in line) for line in grid]
    empty_cols = [all(grid[i][j] == '.' for i in range(len(grid))) for j in range(len(grid[0]))]
    for i, val in enumerate(empty_rows[1:], 1):
        empty_rows[i] = empty_rows[i - 1] + val
    for i, val in enumerate(empty_cols[1:], 1):
        empty_cols[i] = empty_cols[i - 1] + val

    galaxies = []
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == '#':
                galaxies.append((i, j))

    lensum = 0
    for (i1, j1), (i2, j2) in itertools.combinations(galaxies, 2):
        i1, i2 = sorted((i1, i2))
        j1, j2 = sorted((j1, j2))
        factor = 10 if len(grid) == 10 else 1000000
        emptyrows = empty_rows[i2] - empty_rows[i1]
        emptycols = empty_cols[j2] - empty_cols[j1]
        lensum += i2 - i1 - emptyrows + factor * emptyrows +\
                  j2 - j1 - emptycols + factor * emptycols
    return lensum


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
