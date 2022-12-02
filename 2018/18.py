"""
--- 2018 --- Day 18: Settlers of The North Pole ---
"""


EXAMPLES1 = (
    ('18-exemple1.txt', 1147),
)

EXAMPLES2 = (
)

INPUT = '18.txt'


def read_data(filename):
    grid = []
    with open(filename) as f:
        for line in f:
            grid.append(line.strip())
    return grid


def print_grid(grid):
    for line in grid:
        print(line)
    print()


def neighbours(grid, i, j):
    neigh = []
    for i2 in range(i - 1, i + 2):
        for j2 in range(j - 1, j + 2):
            if (i2, j2) != (i, j) and 0 <= i2 < len(grid) and 0 <= j2 < len(grid[0]):
                neigh.append((i2, j2))
    return neigh


def step(grid):
    newgrid = []
    for i in range(len(grid)):
        line = [None] * len(grid[0])
        for j in range(len(grid[0])):
            neigh = [grid[i2][j2] for (i2, j2) in neighbours(grid, i, j)]
            count = {c:neigh.count(c) for c in '.|#'}
            match grid[i][j]:
                case '.': c = '|' if count['|'] >= 3 else '.'
                case '|': c = '#' if count['#'] >= 3 else '|'
                case '#': c = '#' if count['|'] >= 1 and count['#'] >= 1 else '.'
            line[j] = c
        newgrid.append(''.join(line))
    return newgrid


def grid_score(grid):
    count = {c:sum(line.count(c) for line in grid) for c in '|#'}
    return count['|'] * count['#']


def steps(grid, n):
    # print_grid(grid)
    for _ in range(n):
        grid = step(grid)
        # print_grid(grid)
    return grid


def grid_period(grid):
    """
    Return offset, period
    """
    grids = {}
    grids[''.join(grid)] = 0
    for t in range(1, 1_000_000):
        grid = step(grid)
        sgrid = ''.join(grid)
        if sgrid in grids:
            return grids[sgrid] - 1, t - grids[sgrid]
        else:
            grids[sgrid] = t


def steps_opt(grid, n):
    offset, period = grid_period(grid)
    grid = steps(grid, offset)
    grid = steps(grid, (n - offset) % period)
    return grid


def code1(grid):
    return grid_score(steps(grid, 10))


def code2(grid):
    minutes = 1000000000
    return grid_score(steps_opt(grid, minutes))


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
