
EXAMPLES1 = (
    ('22-exemple1.txt', 5587),
)

EXAMPLES2 = (
)

INPUT = '22.txt'


# directions coded as 0: north, 1: east, etc
RIGHT = (1, 2, 3, 0)
LEFT = (3, 0, 1, 2)
REVERSE = (2, 3, 0, 1)
IDELTA = [-1, 0, 1, 0]
JDELTA = [0, 1, 0, -1]


def read_data(data):
    with open(data) as f:
        x = [_.strip() for _ in f.readlines()]

    grid = dict()
    for i, line in enumerate(x):
        for j, char in enumerate(line):
            if char == '#':
                setgrid(grid, i, j, char)

    i_start = len(x) // 2
    j_start = len(x[0]) // 2
    return grid, i_start, j_start, 0


def getgrid(grid, i, j):
    if i not in grid or j not in grid[i]:
        return '.'
    else:
        return grid[i][j]


def setgrid(grid, i, j, char):
    if i not in grid:
        grid[i] = dict()
    grid[i][j] = char


def display_grid(grid):
    imin = min(grid)
    imax = max(grid)
    jmin = float('inf')
    jmax = float('-inf')
    for line in grid.values():
        jmin = min(jmin, *line)
        jmax = max(jmax, *line)

    print('-' * 20)
    print(grid)
    for i in range(imin, imax + 1):
        print(''.join([getgrid(grid, i, j) for j in range(jmin, jmax + 1)]))
    print('-' * 20)


def burst1(grid, i, j, direction):
    if getgrid(grid, i, j) == '#':
        direction = RIGHT[direction]
        setgrid(grid, i, j, '.')
        infected = False
    else:
        direction = LEFT[direction]
        setgrid(grid, i, j, '#')
        infected = True
    i += IDELTA[direction]
    j += JDELTA[direction]
    return grid, i, j, direction, infected


def code1(data):
    grid, i, j, direction = data
    nb_infected = 0
    for _ in range(10000):
        grid, i, j, direction, infected = burst1(grid, i, j, direction)
        nb_infected += infected
    return nb_infected


def burst2(grid, i, j, direction):
    if getgrid(grid, i, j) == '#':      # infected
        direction = RIGHT[direction]
        setgrid(grid, i, j, 'flagged')
        infected = False
    elif getgrid(grid, i, j) == 'flagged':
        direction = REVERSE[direction]
        setgrid(grid, i, j, '.')
        infected = False
    elif getgrid(grid, i, j) == 'weakened':
        direction = direction
        setgrid(grid, i, j, '#')
        infected = True
    else:
        direction = LEFT[direction]     # clean
        setgrid(grid, i, j, 'weakened')
        infected = False
    i += IDELTA[direction]
    j += JDELTA[direction]
    return grid, i, j, direction, infected


def code2(data):
    grid, i, j, direction = data
    nb_infected = 0
    for _ in range(10_000_000):
        grid, i, j, direction, infected = burst2(grid, i, j, direction)
        nb_infected += infected
    return nb_infected


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
