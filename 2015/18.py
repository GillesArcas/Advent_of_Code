"""
--- 2015 --- Day 18: Like a GIF For Your Yard ---
"""


EXAMPLES1 = (
    # ('18-exemple1.txt', None),
)

EXAMPLES2 = (
)

INPUT = '18.txt'


def read_data(filename):
    grid = []
    with open(filename) as f:
        for line in f.readlines():
            grid.append(list(line.strip()))
    return grid


def print_grid(grid):
    for line in grid:
        print(''.join(line))
    print()


def neighbours(grid, i, j):
    neigh = []
    for i2 in range(i - 1, i + 2):
        for j2 in range(j - 1, j + 2):
            if (i2, j2) != (i, j) and 0 <= i2 < len(grid) and 0 <= j2 < len(grid[0]):
                neigh.append((i2, j2))
    return neigh


def iteration(grid):
    new_grid = [line[:] for line in grid]
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            n = sum(grid[i2][j2] == '#' for i2, j2 in neighbours(grid, i, j))
            if char == '#':
                if 2 <= n <= 3:
                    new_grid[i][j] = '#'
                else:
                    new_grid[i][j] = '.'
            else:
                if n == 3:
                    new_grid[i][j] = '#'
                else:
                    new_grid[i][j] = '.'
    return new_grid


def code1(grid):
    for _ in range(100):
        grid = iteration(grid)
    return sum(line.count('#') for line in grid)


def code2(grid):
    for i in range(100):
        for i, j in ((0, 0), (0, 99), (99, 0), (99, 99)):
            grid[i][j] = '#'
        grid = iteration(grid)
    for i, j in ((0, 0), (0, 99), (99, 0), (99, 99)):
        grid[i][j] = '#'
    return sum(line.count('#') for line in grid)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
