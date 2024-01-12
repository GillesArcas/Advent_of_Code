"""
--- Day 21: Step Counter ---
"""

"""
Explications partie 2:

En traçant les premières valeurs du nombre de points atteints, puis leurs
accroissements et les accroissements des accrossements, on constate que les
accroissements des accrossements sont périodiques pour un écart donné entre
termes.

u connu jusqu'au rang p+q
vn+1 = un+1 - un ou un+1 = un + vn+1
wn+q = vn+q - vn ou vn+q = vn + wn+q

w est périodique de période q, wn+q = wn à partir du rang p+q

On en déduit que :

vp+aq+b = vp+b + awp+b

Ensuite, on développe pour trouver le formule dgénérale de un.

up+q+1 = up+q + vp+q+1
       = up+q + vp+1 + wp+1
...
up+q+q = up+q + vp+1 + ... + vp+q + wp+1 ...  + wp+q

up+2q+1 = up+2q + vp+2q+1
        = (up+q + vp+1 + ... + vp+q + wp+1 ...  + wp+q) + vp+2q+1
        = (up+q + vp+1 + ... + vp+q + wp+1 ...  + wp+q) + vp+q+1 + wp+2q+1
        = (up+q + vp+1 + ... + vp+q + wp+1 ...  + wp+q) + vp+q+1 + wp+q+1
        = (up+q + vp+1 + ... + vp+q + wp+1 ...  + wp+q) + vp+1 + wp+q+1 + wp+q+1
        = (up+q + vp+1 + ... + vp+q + wp+1 ...  + wp+q)
                + vp+1 +            + 2wp+1

etc
"""


EXAMPLES1 = (
    ('21-exemple1.txt', 16),
)

EXAMPLES2 = (
    ('21-exemple1.txt', 16733044),
)

INPUT = '21.txt'


def read_data(filename):
    with open(filename) as f:
        grid = [_.strip() for _ in f.readlines()]
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == 'S':
                return (i, j), grid
    return None


def empty_neighbours(grid, i, j):
    neigh = set()
    for i2, j2 in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
        if 0 <= i2 < len(grid) and 0 <= j2 < len(grid[0]) and grid[i2][j2] != '#':
            neigh.add((i2, j2))
    return neigh


def show_grid(grid, reached):
    array = [list(line) for line in grid]
    for pos in reached:
        array[pos[0]][pos[1]] = 'O'
    for row in array:
        print(''.join(row))
    print()


def code1(data):
    start, grid = data
    nsteps = 6 if len(grid) == 11 else 64
    reached = set()
    reached.add(start)
    for step in range(nsteps):
        newreached = set()
        for pos in reached:
            newreached.update(empty_neighbours(grid, *pos))
        reached = newreached
        # print(step + 1, len(reached))
        # show_grid(grid, reached)

    return len(reached)


def empty_neighbours2(grid, i, j):
    neigh = set()
    for i2, j2 in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
        if grid[i2 % len(grid)][j2 % len(grid[0])] != '#':
            neigh.add((i2, j2))
    return neigh


def offset_period(values):
    """
    Heuristic, offset is not minimal
    """
    offset = 500
    lenpat = 10
    pattern = values[offset:offset + lenpat]
    for i in range(offset + lenpat, len(values)):
        if values[i:i + lenpat] == pattern:
            return offset, i - offset
    return None


def nth(values, delta, delta2, offset, period, i):
    sigmadelta = sum(delta[offset:offset + period])
    sigmadelta2 = sum(delta2[offset:offset + period])
    nperiod = (i - (offset + period)) // period
    rest = (i - (offset + period)) % period
    return (
        values[offset + period] +
        nperiod * sigmadelta +
        ((nperiod * (nperiod + 1)) // 2) * sigmadelta2 +
        sum(delta[offset:offset + rest]) +
        (nperiod + 1) * sum(delta2[offset:offset + rest])
    )


def code2(data):
    start, grid = data

    # store first terms of sequence for analysis (may required some time, use pypy)
    reached = set()
    reached.add(start)
    values = []
    for step in range(800):
        newreached = set()
        for pos in reached:
            newreached.update(empty_neighbours2(grid, *pos))
        reached = newreached
        print(step + 1, len(reached))
        values.append(len(reached))

    # store increments
    delta = [y - x for x, y in zip(values, values[1:])]

    # analyse increments of increments to find periodicity
    for p in range(1, 400):
        delta2 = [y - x for x, y in zip(delta, delta[p:])]
        if (periodicity := offset_period(delta2)) is not None:
            break
    else:
        # periodicity not found
        return None

    # periodicity found
    offset, period = periodicity

    nsteps = 5000 if len(grid) == 11 else 26501365
    return nth(values, delta, delta2, offset, period, nsteps - 1)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        print(fn)
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
