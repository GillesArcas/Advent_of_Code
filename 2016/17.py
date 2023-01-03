"""
--- 2016 --- Day 17: Two Steps Forward ---
"""


import hashlib


EXAMPLES1 = (
    ('17-exemple1.txt', 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'),
)

EXAMPLES2 = (
    ('17-exemple1.txt', 830),
)

INPUT = '17.txt'


def read_data(filename):
    with open(filename) as f:
        return f.read().strip()


def possible_moves(passcode, path, i, j):
    neigh = ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))
    h = hashlib.md5((passcode + path).encode()).hexdigest()
    states = [c in 'bcdef' for c in h[:4]]
    for (ii, jj), isopen, move in zip(neigh, states, 'UDLR'):
        if 0 <= ii < 4 and 0 <= jj < 4 and isopen:
            yield (ii, jj), move


def code1(passcode):
    stack = []
    path = ''
    stack.append(((0, 0), path))
    while stack:
        (i, j), path = stack.pop(0)
        if (i, j) == (3, 3):
            return path
        else:
            for newpos, move in possible_moves(passcode, path, i, j):
                stack.append((newpos, path + move))
    return None


def code2(passcode):
    stack = []
    path = ''
    stack.append(((0, 0), path))
    maxlen = 0
    while stack:
        (i, j), path = stack.pop(0)
        if (i, j) == (3, 3):
            if len(path) > maxlen:
                maxlen = len(path)
        else:
            for newpos, move in possible_moves(passcode, path, i, j):
                stack.append((newpos, path + move))
    return maxlen


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
