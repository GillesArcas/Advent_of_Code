"""
--- 2022 --- Day 14: Regolith Reservoir ---
"""


import re


EXAMPLES1 = (
    ('14-exemple1.txt', 24),
)

EXAMPLES2 = (
    ('14-exemple1.txt', 93),
)

INPUT = '14.txt'


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()

    paths = []
    for line in lines:
        strcoords = re.findall(r'(\d+),(\d+)', line)
        paths.append([(int(x), int(y)) for x, y in strcoords])

    xmin = float('inf')
    xmax = float('-inf')
    ymin = 0
    ymax = float('-inf')
    for path in paths:
        for x, y in path:
            xmin = min(xmin, x)
            xmax = max(xmax, x)
            ymax = max(ymax, y)
    xmin -= 1
    xmax += 1

    grid = {y: {x: '.' for x in range(xmin, xmax + 1)} for y in range(ymin, ymax + 1)}

    grid[0][500] = '+'
    for path in paths:
        x0, y0 = path[0]
        for x1, y1 in path[1:]:
            if x1 == x0:
                y0s, y1s = sorted((y0, y1))
                for y in range(y0s, y1s + 1):
                    grid[y][x0] = '#'
            elif y1 == y0:
                x0s, x1s = sorted((x0, x1))
                for x in range(x0s, x1s + 1):
                    grid[y0][x] = '#'
            x0, y0 = x1, y1

    # print_grid(grid)

    return grid


def print_grid(grid):
    xmin = min(grid[0])
    xmax = max(grid[0])
    ymin = 0
    ymax = max(grid)

    for y in range(ymin, ymax + 1):
        print(''.join([grid[y][x] for x in range(xmin, xmax + 1)]))
    print()


def simulate_falling_unit(grid):
    ymax = max(grid)
    changed = False
    xunit, yunit = 500, 0
    while yunit < ymax:
        if grid[yunit + 1][xunit] == '.':
            yunit += 1
        else:
            if grid[yunit + 1][xunit - 1] == '.':
                xunit -= 1
                yunit += 1
            elif grid[yunit + 1][xunit + 1] == '.':
                xunit += 1
                yunit += 1
            else:
                grid[yunit][xunit] = 'O'
                changed = True
                break
    return changed


def code1(grid):
    while simulate_falling_unit(grid):
        pass

    print_grid(grid)
    return sum(list(line.values()).count('O') for line in grid.values())


def code2(grid):
    ymin = 0
    ymax = max(grid)

    # make a new grid to cope with new rule
    xgrid = {y: {x: '.' for x in range(500 - ymax - 2, 500 + ymax + 3)} for y in range(ymin, ymax + 1 + 1)}
    for y, line in grid.items():
        for x, unit in line.items():
            xgrid[y][x] = unit

    # add bottom wall
    xgrid[ymax + 2] = {x: '#' for x in range(500 - ymax - 2, 500 + ymax + 3)}

    while simulate_falling_unit(xgrid) and xgrid[0][500] != 'O':
        pass

    print_grid(xgrid)
    return sum(list(line.values()).count('O') for line in xgrid.values())


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
