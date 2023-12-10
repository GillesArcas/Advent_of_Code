"""
--- Day 10: Pipe Maze ---
"""


import re
import itertools


EXAMPLES1 = (
    ('10-exemple1.txt', 4),
    ('10-exemple2.txt', 8),
)

EXAMPLES2 = (
    ('10-exemple3.txt', 4),
    ('10-exemple4.txt', 8),
    ('10-exemple5.txt', 10),
)

INPUT = '10.txt'


def read_data(filename):
    with open(filename) as f:
        lines = [_.strip() for _ in f.readlines()]
    for i, line in enumerate(lines):
        if (j := line.find('S')) >= 0:
            return (i, j), lines
    assert False


def first_pipe(i, j, grid):
    if grid[i][j + 1] == '-' and grid[i + 1][j] == '|':
        return 'F'
    elif grid[i][j + 1] == 'J' and grid[i + 1][j] == '|':
        return 'F'
    elif grid[i - 1][j] == '|' and grid[i + 1][j] == 'L':
        return '|'
    elif grid[i][j + 1] == '7' and grid[i + 1][j] == 'J':
        return 'F'
    elif grid[i][j - 1] == 'F' and grid[i + 1][j] == '|':
        return '7'
    else:
        # other cases omitted
        assert False


def nextpipes(i, j, grid):
    match grid[i][j]:
        case '|':
            return (i - 1, j), (i + 1, j)
        case '-':
            return (i, j - 1), (i, j + 1)
        case 'L':
            return (i - 1, j), (i, j + 1)
        case 'J':
            return (i - 1, j), (i, j - 1)
        case '7':
            return (i + 1, j), (i, j - 1)
        case 'F':
            return (i + 1, j), (i, j + 1)
        case _:
            assert False


def pipepath(start, grid):
    path = [start]
    origin = None
    while True:
        node = path[-1]
        node1, node2 = nextpipes(*node, grid)
        path.append(node1 if (node1 != origin) else node2)
        origin = node
        if path[-1] == start:
            return path


def enclosed(node, grid):
    i0, j0 = node
    east_nodes = grid[i0][j0 + 1:]
    east_walls = re.findall('[|]|L-*7|F-*J', east_nodes)
    return len(east_walls) % 2


def code1(data):
    (istart, jstart), grid = data
    grid[istart] = grid[istart].replace('S', first_pipe(istart, jstart, grid))
    path = pipepath((istart, jstart), grid)
    return len(path) // 2


def code2(data):
    (istart, jstart), grid = data
    grid[istart] = grid[istart].replace('S', first_pipe(istart, jstart, grid))
    path = pipepath((istart, jstart), grid)
    pathpipes = set(path)

    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if (i, j) not in pathpipes:
                grid[i] = grid[i][:j] + '.' + grid[i][j + 1:]

    area = 0
    for node in itertools.product(range(len(grid)), range(len(grid[0]))):
        if node not in pathpipes:
            if enclosed(node, grid):
                area += 1
    return area


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
