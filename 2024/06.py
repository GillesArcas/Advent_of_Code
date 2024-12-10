"""
--- Day 6: Guard Gallivant ---
"""


import copy


EXAMPLES1 = (
    ('06-exemple1.txt', 41),
)

EXAMPLES2 = (
    ('06-exemple1.txt', 6),
)

INPUT = '06.txt'


def read_data(filename):
    with open(filename) as f:
        return [list(_.strip()) for _ in f.readlines()]


def findstart(mymap):
    for i, line in enumerate(mymap):
        for j, c in enumerate(line):
            if c in '<>^v':
                return i, j


iFWD = {'<': 0, '>': 0, '^': -1, 'v': 1}
jFWD = {'<': -1, '>': 1, '^': 0, 'v': 0}
TURNRIGHT = {'<': '^', '>': 'v', '^': '>', 'v': '<'}


def finalpos(mymap):
    i, j = findstart(mymap)
    direction = mymap[i][j]
    while True:
        inext = i + iFWD[direction]
        jnext = j + jFWD[direction]
        if not (0 <= inext < len(mymap) and 0 <= jnext < len(mymap[0])):
            return mymap
        if mymap[inext][jnext] == '#':
            direction = TURNRIGHT[direction]
        else:
            i, j = inext, jnext
            if mymap[i][j] == direction:
                return None
            else:
                mymap[i][j] = direction


def code1(mymap):
    return sum(line.count('<') + line.count('>') + line.count('^') + line.count('v') for line in finalpos(mymap))


def code2(mymap):
    i, j = findstart(mymap)
    pos = finalpos(copy.deepcopy(mymap))
    result = 0
    for ii, line in enumerate(pos):
        print(ii)
        for jj, char in enumerate(line):
            if (i, j) == (ii, jj):
                continue
            if char in '<>^v':
                mymap2 = copy.deepcopy(mymap)
                mymap2[ii][jj] = '#'
                pos2 = finalpos(mymap2)
                if pos2 is None:
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
