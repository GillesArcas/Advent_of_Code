"""
--- Day 4: Ceres Search ---
"""


EXAMPLES1 = (
    ('04-exemple1.txt', 18),
)

EXAMPLES2 = (
    ('04-exemple1.txt', 9),
)

INPUT = '04.txt'


def read_data(filename):
    with open(filename) as f:
        return [_.strip() for _ in f.readlines()]


def diag1(mat):
    i = 0
    for j in range(len(mat[0]) - 1, -1, -1):
        s = ''
        for k in range(0, len(mat[0]) - j):
            s += mat[i + k][j + k]
        yield s
    for i in range(1, len(mat)):
        j = 0
        s = ''
        for k in range(0, len(mat) - i):
            s += mat[i + k][j + k]
        yield s


def diag2(mat):
    i = 0
    for j in range(len(mat[0])):
        s = ''
        for k in range(j + 1):
            s += mat[i + k][j - k]
        yield s
    for i in range(1, len(mat)):
        j = len(mat[0]) - 1
        s = ''
        for k in range(0, len(mat) - i):
            s += mat[i + k][j - k]
        yield s


def allstrings(mat):
    # marche pas
    yield from mat
    yield from diag1(mat)
    mat = [''.join(_) for _ in zip(*mat)]
    yield from mat
    yield from diag1(mat)


def allstrings(mat):
    yield from mat
    yield from diag1(mat)
    yield from diag2(mat)
    yield from [''.join(_) for _ in zip(*mat)]


def code1(mat):
    return sum(_.count('XMAS') + _.count('SAMX') for _ in allstrings(mat))


def match(mat, i, j):
    if mat[i][j] == 'A':
        m1m1 = mat[i - 1][j - 1]
        p1p1 = mat[i + 1][j + 1]
        m1p1 = mat[i - 1][j + 1]
        p1m1 = mat[i + 1][j - 1]
        if ((m1m1 == 'M' and p1p1 == 'S') or (m1m1 == 'S' and p1p1 == 'M')) and\
           ((m1p1 == 'M' and p1m1 == 'S') or (m1p1 == 'S' and p1m1 == 'M')):
            return True
    return False


def code2(mat):
    result = 0
    for i in range(1, len(mat) - 1):
        for j in range(1, len(mat[0]) - 1):
            if match(mat, i, j):
                result += 1
    return result


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
