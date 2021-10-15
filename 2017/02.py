import itertools


EXAMPLES1 = (
    ('02-exemple1.txt', 18),
)

EXAMPLES2 = (
    ('02-exemple2.txt', 9),
)

INPUT =  '02-input.txt'


def read_mat(fn):
    mat = list()
    with open(fn) as f:
        for line in f:
            mat.append([int(x) for x in line.split()])
    return mat


def code1(mat):
    return sum(max(line) - min(line) for line in mat)


def code2(mat):
    sigma = 0
    for line in mat:
        for x, y in itertools.combinations(sorted(line, reverse=True), 2):
            r = x // y
            if r == x / y:
                sigma += r
                break
    return sigma


def test(n, code, examples, myinput):
    for fn, result in examples:
        data = read_mat(fn)
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(read_mat(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
