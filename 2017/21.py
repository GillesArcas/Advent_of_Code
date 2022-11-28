
EXAMPLES1 = (
    ((2, '21-exemple1.txt'), 12),
)

EXAMPLES2 = (
)

INPUT = (5, '21.txt')


SYMMETRIES2x2 = (
    (0, 1, 2, 3),   # ID
    (2, 0, 3, 1),   # R1
    (3, 2, 1, 0),   # R2
    (1, 3, 0, 2),   # R3
    (2, 3, 0, 1),   # FH
    (1, 0, 3, 2),   # FV
    (0, 2, 1, 3),   # D1
    (3, 1, 2, 0),   # D2
)


SYMMETRIES3x3 = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8),   # ID
    (6, 3, 0, 7, 4, 1, 8, 5, 2),   # R1
    (8, 7, 6, 5, 4, 3, 2, 1, 0),   # R2
    (2, 5, 8, 1, 4, 7, 0, 3, 6),   # R3
    (6, 7, 8, 3, 4, 5, 0, 1, 2),   # FH
    (2, 1, 0, 5, 4, 3, 8, 7, 6),   # FV
    (0, 3, 6, 1, 4, 7, 2, 5, 8),   # D1
    (8, 5, 2, 7, 4, 1, 6, 3, 0),   # D2
)


def read_data(data):
    nb_iter, filename = data
    rules = dict()
    with open(filename) as f:
        for line in f:
            left, right = line.strip().replace('/', '').split(' => ')
            rules[left] = right
    rules = add_symmetries(rules)
    return nb_iter, rules


def add_symmetries(rules):
    extended_rules = dict()
    for left, right in rules.items():
        if len(left) == 4:
            for sym in SYMMETRIES2x2:
                new_left = ''.join([left[_] for _ in sym])
                extended_rules[new_left] = right
        else:
            for sym in SYMMETRIES3x3:
                new_left = ''.join([left[_] for _ in sym])
                extended_rules[new_left] = right
    return extended_rules


def apply_rules(grid, rules):
    if len(grid) % 2 == 0:
        new_grid = [''] * (len(grid) // 2 * 3)
        for i in range(0, len(grid), 2):
            for j in range(0, len(grid), 2):
                pat = grid[i][j:j + 2] + grid[i + 1][j:j + 2]
                new_pat = rules[pat]
                new_grid[i // 2 * 3 + 0] += new_pat[0:3]
                new_grid[i // 2 * 3 + 1] += new_pat[3:6]
                new_grid[i // 2 * 3 + 2] += new_pat[6:9]
    else:
        new_grid = [''] * (len(grid) // 3 * 4)
        for i in range(0, len(grid), 3):
            for j in range(0, len(grid), 3):
                pat = grid[i][j:j + 3] + grid[i + 1][j:j + 3] + grid[i + 2][j:j + 3]
                new_pat = rules[pat]
                new_grid[i // 3 * 4 + 0] += new_pat[0:4]
                new_grid[i // 3 * 4 + 1] += new_pat[4:8]
                new_grid[i // 3 * 4 + 2] += new_pat[8:12]
                new_grid[i // 3 * 4 + 3] += new_pat[12:16]
    return new_grid


def print_grid(grid):
    for _ in grid:
        print(_)


def code1(data):
    nb_iter, rules = data
    grid = ('.#.', '..#', '###')
    for _ in range(nb_iter):
        grid = apply_rules(grid, rules)
    return sum(line.count('#') for line in grid)


def code2(data):
    nb_iter, rules = data
    nb_iter = 18
    grid = ('.#.', '..#', '###')
    for _ in range(nb_iter):
        grid = apply_rules(grid, rules)
    return sum(line.count('#') for line in grid)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
