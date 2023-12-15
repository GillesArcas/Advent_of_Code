"""
--- Day 14: Parabolic Reflector Dish ---
"""


EXAMPLES1 = (
    ('14-exemple1.txt', 136),
)

EXAMPLES2 = (
    ('14-exemple1.txt', 64),
)

INPUT = '14.txt'


def read_data(filename):
    with open(filename) as f:
        return [list(_.strip()) for _ in f.readlines()]


def tilt_col_north(col):
    s = ''.join(col)
    while 1:
        s2 = s.replace('.O', 'O.')
        if s2 == s:
            return list(s)
        else:
            s = s2


def tilt_col_south(col):
    s = ''.join(col)
    while 1:
        s2 = s.replace('O.', '.O')
        if s2 == s:
            return list(s)
        else:
            s = s2


def tilt_col_west(row):
    s = ''.join(row)
    while 1:
        s2 = s.replace('.O', 'O.')
        if s2 == s:
            return list(s)
        else:
            s = s2


def tilt_col_east(row):
    s = ''.join(row)
    while 1:
        s2 = s.replace('O.', '.O')
        if s2 == s:
            return list(s)
        else:
            s = s2


def tilt_north(grid):
    for j in range(len(grid[0])):
        col = [grid[i][j] for i in range(len(grid))]
        col = tilt_col_north(col)
        for i in range(len(grid)):
            grid[i][j] = col[i]


def tilt_south(grid):
    for j in range(len(grid[0])):
        col = [grid[i][j] for i in range(len(grid))]
        col = tilt_col_south(col)
        for i in range(len(grid)):
            grid[i][j] = col[i]


def tilt_west(grid):
    for i in range(len(grid)):
        row = grid[i]
        row = tilt_col_west(row)
        grid[i] = row


def tilt_east(grid):
    for i in range(len(grid)):
        row = grid[i]
        row = tilt_col_east(row)
        grid[i] = row


def weight_north(grid):
    count = 0
    for i in range(len(grid)):
        count += sum(grid[i][j] == 'O' for j in range(len(grid[0]))) * (len(grid) - i)
    return count


def code1(grid):
    tilt_north(grid)
    return weight_north(grid)


def offset_period(values):
    """
    Heuristic
    """
    offset = 500
    lenpat = 10
    pattern = values[offset:offset + lenpat]
    for i in range(offset + lenpat, len(values)):
        if values[i:i + lenpat] == pattern:
            return offset, i - offset
    return None


def code2(grid):
    values = []
    for _ in range(1000):
        tilt_north(grid)
        tilt_west(grid)
        tilt_south(grid)
        tilt_east(grid)
        values.append(weight_north(grid))

    offset, period = offset_period(values)
    assert all(values[n] == values[offset + (n - offset) % period] for n in range(offset, 1000))

    return values[offset + (1000000000 - 1 - offset) % period]


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
