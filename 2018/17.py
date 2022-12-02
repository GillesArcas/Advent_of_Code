"""
--- 2018 --- Day 17: Reservoir Research ---
"""


import re
from collections import defaultdict


EXAMPLES1 = (
    ('17-exemple1.txt', 57),
    ('17-exemple2.txt', None),
    ('17-exemple3.txt', None),
)

EXAMPLES2 = (
    ('17-exemple1.txt', 29),
)

INPUT = '17.txt'


XPAT = r'x=(\d+), y=(\d+)\.\.(\d+)'
YPAT = r'y=(\d+), x=(\d+)\.\.(\d+)'


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()

    grid = defaultdict(lambda: defaultdict(lambda: '.'))
    original_exemple = True
    for index, line in enumerate(lines):
        # xy line
        match = re.match(XPAT, line)
        if match:
            x, y1, y2 = [int(_) for _ in match.group(1, 2, 3)]
            for y in range(y1, y2 + 1):
                grid[y][x] = '#'
            continue

        # yx line
        match = re.match(YPAT, line)
        if match:
            y, x1, x2 = [int(_) for _ in match.group(1, 2, 3)]
            for x in range(x1, x2 + 1):
                grid[y][x] = '#'
            continue

        # grid line (additional test cases eg exemple2)
        original_exemple = False
        for x, char in enumerate(line.strip()):
            grid[index][x] = char

    ymin_data = min(grid)
    ymin, ymax = 0, max(grid)
    xmin, xmax = float('inf'), float('-inf')
    for line in grid.values():
        xmin = min(xmin, min(line))
        xmax = max(xmax, max(line))

    if original_exemple:
        grid[0][500] = '+'

    return xmin - 1, xmax + 1, ymin, ymax, grid, ymin_data


def print_grid(xmin, xmax, ymin, ymax, grid):
    for y in range(ymin, ymax + 1):
        print(''.join(grid[y][x] for x in range(xmin, xmax + 1)))
    print()


def iterate(xmin, xmax, ymin, ymax, grid):
    changed = False
    for y in range(ymin, ymax + 1):
        line = ''.join(grid[y].values())
        for x in range(xmin, xmax + 1):
            if grid[y][x] == '.':
                if grid[y - 1][x] == '+':
                    grid[y][x] = '|'
                elif grid[y - 1][x] == '|':
                    grid[y][x] = '|'
            elif grid[y][x] == '|':
                if grid[y + 1][x] in '#~':
                    flow_down = will_flow_down(x, y, grid, xmin, xmax)
                    grid[y][x] = '|' if flow_down else '~'
                    x2 = x - 1
                    while True:
                        if grid[y][x2] == '#':
                            break
                        elif grid[y + 1][x2] in '#~':
                            grid[y][x2] = '|' if flow_down else '~'
                        elif grid[y + 1][x2] in '|':
                            break
                        elif grid[y + 1][x2] in '.':
                            grid[y][x2] = '|'
                            break
                        x2 -= 1
                    x2 = x + 1
                    while True:
                        if grid[y][x2] == '#':
                            break
                        elif grid[y + 1][x2] in '#~':
                            grid[y][x2] = '|' if flow_down else '~'
                        elif grid[y + 1][x2] in '|':
                            break
                        elif grid[y + 1][x2] in '.':
                            grid[y][x2] = '|'
                            break
                        x2 += 1
        if not changed:
            changed = line != ''.join(grid[y].values())
            first_y_modified = y
    return changed, first_y_modified


def will_flow_down(x, y, grid, xmin, xmax):
    for xx in range(x - 1, xmin, -1):
        if grid[y][xx] == '#':
            break
        elif grid[y + 1][xx] == '.':
            return True
    for xx in range(x + 1, xmax):
        if grid[y][xx] == '#':
            break
        elif grid[y + 1][xx] == '.':
            return True
    return False


def code1(data):
    xmin, xmax, ymin, ymax, grid, ymindata = data
    first_y_modified = 1
    while True:
        changed, first_y_modified = iterate(xmin, xmax, first_y_modified - 1, ymax, grid)
        # print_grid(xmin, xmax, ymin, ymax, grid)
        if not changed:
            break

    print_grid(xmin, xmax, ymin, ymax, grid)

    return sum(sum(_ in '|~' for _ in grid[y].values()) for y in range(ymindata, ymax + 1))


def code2(data):
    xmin, xmax, ymin, ymax, grid, ymindata = data
    first_y_modified = 1
    while True:
        changed, first_y_modified = iterate(xmin, xmax, first_y_modified - 1, ymax, grid)
        if not changed:
            break
    return sum(sum(_ == '~' for _ in grid[y].values()) for y in range(ymindata, ymax + 1))


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
