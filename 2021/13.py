import re


EXAMPLES1 = (
    ('13-exemple1.txt', 17),
)

EXAMPLES2 = (
    ('13-exemple1.txt', None),
)

INPUT =  '13.txt'


def read_data(fn):
    coord = list()
    folds = list()
    with open(fn) as f:
        for line in f:
            if line.strip():
                if not line.startswith('fold'):
                    x, y = (int(_) for _ in line.strip().split(','))
                    coord.append((x, y))
                else:
                    match = re.match(r'fold along ([xy])=(\d+)', line)
                    folds.append((match.group(1), int(match.group(2))))
    dimx = max(x for x, _ in coord) + 1
    dimy = max(y for _, y in coord) + 1
    mat = [[0 for x in range(dimx)] for y in range(dimy)]
    for x, y in coord:
        mat[y][x] = 1
    return mat, folds


def display(mat):
    for y in range(len(mat)):
        print(''.join('.#'[_] for _ in mat[y]))


def fold(mat, axe, num):
    if axe == 'y':
        dimx = len(mat[0])
        dimy = num
        new = [[0 for x in range(dimx)] for y in range(dimy)]
        for y in range(dimy):
            for x in range(dimx):
                if 0 <= y + 2 * (num - y) - 1 < len(mat):
                    new[y][x] = mat[y][x] or mat[y + 2 * (num - y)][x]
                else:
                    new[y][x] = mat[y][x]
    else:
        dimx = num
        dimy = len(mat)
        new = [[0 for x in range(dimx)] for y in range(dimy)]
        for y in range(dimy):
            for x in range(dimx):
                if 0 <= x + 2 * (num - x) < len(mat[0]):
                    new[y][x] = mat[y][x] or mat[y][x + 2 * (num - x)]
                else:
                    new[y][x] = mat[y][x]
    return new


def code1(data):
    mat, folds = data
    mat = fold(mat, folds[0][0], folds[0][1])
    # mat = fold(mat, folds[1][1], folds[1][1])
    # display(mat)
    return sum(sum(line) for line in mat)


def code2(data):
    mat, folds = data
    for axe, num in folds:
        mat = fold(mat, axe, num)
    display(mat)
    return None


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
