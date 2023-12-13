"""
--- Day 13: Point of Incidence ---
"""


import re


EXAMPLES1 = (
    ('13-exemple1.txt', 405),
)

EXAMPLES2 = (
    ('13-exemple1.txt', 400),
)

INPUT = '13.txt'


def read_data(filename):
    with open(filename) as f:
        data = f.read()
    data += '\n'
    return [_.splitlines() for _ in re.findall(r'(?:[.#]+\n)+', data)]


def test_h(grid):
    for i in range(1, len(grid)):
        if all(grid[i - k - 1] == grid[i + k] for k in range(i) if i + k < len(grid)):
            return i
    return 0


def nthcol(grid, j):
    return [grid[i][j] for i in range(len(grid))]


def test_v(grid):
    for j in range(1, len(grid[0])):
        if all(nthcol(grid, j - k -1) == nthcol(grid, j + k) for k in range(j) if j + k < len(grid[0])):
            return j
    return 0


def code1(grids):
    count = 0
    for grid in grids:
        nh = test_h(grid)
        nv = test_v(grid)
        count += 100 * nh + nv
    return count


def difference(x1, x2):
    return sum(y1 != y2 for y1, y2 in zip(x1, x2))


def test_h2(grid):
    for i in range(1, len(grid)):
        if sum(difference(grid[i - k - 1], grid[i + k]) for k in range(i) if i + k < len(grid)) == 1:
            return i
    return 0


def test_v2(grid):
    for j in range(1, len(grid[0])):
        if sum(difference(nthcol(grid, j - k -1), nthcol(grid, j + k)) for k in range(j) if j + k < len(grid[0])) == 1:
            return j
    return 0


def code2(grids):
    count = 0
    for grid in grids:
        nh = test_h2(grid)
        nv = test_v2(grid)
        count += 100 * nh + nv
    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
