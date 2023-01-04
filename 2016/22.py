"""
--- 2016 --- Day 22: Grid Computing ---
"""


import re


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '22.txt'


def read_data(filename):
    nodes = []
    with open(filename) as f:
        for line in f.readlines():
            nodes.append([int(_) for _ in re.findall(r'\d+', line)])
    return nodes


def code1(nodes):
    count = 0
    for node1 in nodes:
        _, _, _, used1, _, _ = node1
        if used1 == 0:
            continue
        for node2 in nodes:
            if node1 != node2:
                _, _, _, _, avail2, _ = node2
                if used1 <= avail2:
                    count += 1
    return count


def print_grid(grid):
    for line in grid:
        print(''.join(line))
    print()


def code2(nodes):
    xmax = 0
    ymax = 0
    for node in nodes:
        x, y, *_ = node
        xmax = max(xmax, x)
        ymax = max(ymax, y)

    grid = [['.' for x in range(xmax + 1)] for y in range(ymax + 1)]

    xmax = 0
    ymax = 0
    for node in nodes:
        x, y, size, used, *_ = node
        if size >= 500:
            grid[y][x] = '#'
        elif used == 0:
            grid[y][x] = 'O'

    print_grid(grid)

    # use grid to count manually the moves to reach point in front of goal
    # ..............................._G
    # ...
    count = 49
    # one move to to move goal
    # ...............................G_
    count += 1
    # four moves to reach point in front of goal
    # .............................._G.
    count += 4
    # repeat to last position
    # _G...............................
    count += 5 * 30
    # last move
    # G_...............................
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
