"""
--- 2022 --- Day 8: Treetop Tree House ---
"""


EXAMPLES1 = (
    ('08-exemple1.txt', 21),
)

EXAMPLES2 = (
    ('08-exemple1.txt', 8),
)

INPUT = '08.txt'


def read_data(data):
    with open(data) as f:
        lines = [_.strip() for _ in f.readlines()]
    grid = [[None for _ in lines[0]] for _ in lines]
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            grid[i][j] = int(char)
    return grid


def is_visible(i, j, height, grid):
    count = 0
    for ii in range(0, i):
        if grid[ii][j] >= height:
            count += 1
            break
    for ii in range(i + 1, len(grid)):
        if grid[ii][j] >= height:
            count += 1
            break
    for h in grid[i][:j]:
        if h >= height:
            count += 1
            break
    for h in grid[i][j + 1:]:
        if h >= height:
            count += 1
            break
    return count < 4


def scenic_score(i, j, height, grid):
    score_n = 0
    for ii in range(i - 1, -1, -1):
        score_n += 1
        if grid[ii][j] >= height:
            break
    score_s = 0
    for ii in range(i + 1, len(grid)):
        score_s += 1
        if grid[ii][j] >= height:
            break
    score_w = 0
    for jj in range(j - 1, -1, -1):     # grid[i][j - 1:-1:-1] wrong when j == 0 (starts from end of line)
        score_w += 1
        if grid[i][jj] >= height:
            break
    score_e = 0
    for h in grid[i][j + 1:]:
        score_e += 1
        if h >= height:
            break
    return score_n * score_s * score_w * score_e


def code1(grid):
    count = 0
    for i, line in enumerate(grid):
        for j, height in enumerate(line):
            count += is_visible(i, j, height, grid)
    return count


def code2(grid):
    best_score = 0
    for i, line in enumerate(grid):
        for j, height in enumerate(line):
            best_score = max(best_score, scenic_score(i, j, height, grid))
    return best_score


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
