"""
--- 2022 --- Day 23: Unstable Diffusion ---
"""


from collections import defaultdict


EXAMPLES1 = (
    ('23-exemple1.txt', None),
    ('23-exemple2.txt', 110)
)

EXAMPLES2 = (
    ('23-exemple2.txt', 20),
)

INPUT = '23.txt'


def read_data(filename):
    with open(filename) as f:
        lines = [_.strip() for _ in f.readlines()]

    grid = defaultdict(lambda: defaultdict(lambda: '.'))
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[y][x] = char

    return grid


def grid_bounds(grid):
    xmin = float('inf')
    xmax = float('-inf')
    ymin = float('inf')
    ymax = float('-inf')
    for y, line in grid.items():
        for x, char in line.items():
            if char == '#':
                xmin = min(xmin, x)
                xmax = max(xmax, x)
                ymin = min(ymin, y)
                ymax = max(ymax, y)
    return xmin, xmax, ymin, ymax


def print_grid(grid):
    xmin, xmax, ymin, ymax = grid_bounds(grid)
    print(xmin, xmax, ymin, ymax)
    for y in range(ymin - 1, ymax + 2):
        line = []
        for x in range(xmin - 1, xmax + 2):
            line.append(grid[y][x])
        print(''.join(line))
    print()


def neighbours(grid, x, y):
    neigh = set()
    if grid[y - 1][x] == '#': neigh.add('N')
    if grid[y + 1][x] == '#': neigh.add('S')
    if grid[y][x - 1] == '#': neigh.add('W')
    if grid[y][x + 1] == '#': neigh.add('E')
    if grid[y - 1][x - 1] == '#': neigh.add('NW')
    if grid[y + 1][x - 1] == '#': neigh.add('SW')
    if grid[y - 1][x + 1] == '#': neigh.add('NE')
    if grid[y + 1][x + 1] == '#': neigh.add('SE')
    return neigh


def proposal(nbround, grid, x, y):
    neigh = neighbours(grid, x, y)

    if not neigh:
        return None

    for _ in range(nbround, nbround + 4):
        rule = _ % 4
        if rule == 0:
            if not neigh.intersection({'N', 'NE', 'NW'}):
                return x, y - 1
        if rule == 1:
            if not neigh.intersection({'S', 'SE', 'SW'}):
                return x, y + 1
        if rule == 2:
            if not neigh.intersection({'W', 'NW', 'SW'}):
                return x - 1, y
        if rule == 3:
            if not neigh.intersection({'E', 'NE', 'SE'}):
                return x + 1, y

    return None


def do_round(nbround, grid):
    proposals = defaultdict(lambda: defaultdict(lambda: None))
    propcount = defaultdict(int)
    xmin, xmax, ymin, ymax = grid_bounds(grid)

    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            if grid[y][x] == '#':
                proposals[y][x] = proposal(nbround, grid, x, y)
                propcount[proposals[y][x]] += 1

    newgrid = defaultdict(lambda: defaultdict(lambda: '.'))
    changed = False
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            if grid[y][x] == '#':
                if proposals[y][x] and propcount[proposals[y][x]] == 1:
                    xnew, ynew = proposals[y][x]
                    newgrid[ynew][xnew] = '#'
                    changed = True
                else:
                    newgrid[y][x] = '#'

    return newgrid, changed


def code1(grid):
    for nbround in range(10):
        grid, _ = do_round(nbround, grid)

    count = 0
    xmin, xmax, ymin, ymax = grid_bounds(grid)
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            if grid[y][x] == '.':
                count += 1

    return count


def code2(grid):
    for nbround in range(1_000_000):
        grid, changed = do_round(nbround, grid)
        if not changed:
            return nbround + 1


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
