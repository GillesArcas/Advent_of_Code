"""
startfree, lenfree
"""


EXAMPLES1 = (
    ('10-exemple1.txt', 36),
)

EXAMPLES2 = (
    ('10-exemple1.txt', 81),
)

INPUT = '10.txt'


def read_data(filename):
    mymap = []
    with open(filename) as f:
        for line in f.readlines():
            mymap.append([int(_) for _ in line.strip()])
    return mymap


def nextneighbours(mymap, i, j):
    for ii, jj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
        if 0 <= ii < len(mymap) and 0 <= jj < len(mymap[0]):
            if mymap[ii][jj] == mymap[i][j] + 1:
                yield ii, jj


def headscore(mymap, i, j):
    if mymap[i][j] == 9:
        return {(i, j)}
    else:
        x = [headscore(mymap, ii, jj) for ii, jj in nextneighbours(mymap, i, j)]
        return set().union(*x)


def code1(mymap):
    score = 0
    for i, line in enumerate(mymap):
        for j, val in enumerate(line):
            if val == 0:
                score += len(headscore(mymap, i, j))
    return score


def headscore2(mymap, i, j):
    if mymap[i][j] == 9:
        return 1
    else:
        x = [headscore2(mymap, ii, jj) for ii, jj in nextneighbours(mymap, i, j)]
        return sum(x)


def code2(mymap):
    score = 0
    for i, line in enumerate(mymap):
        for j, val in enumerate(line):
            if val == 0:
                score += headscore2(mymap, i, j)
    return score


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
