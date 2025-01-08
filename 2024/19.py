"""
--- Day 19: Linen Layout ---
"""


import functools


EXAMPLES1 = (
    ('19-exemple1.txt', 6),
)

EXAMPLES2 = (
    ('19-exemple1.txt', 16),
)

INPUT = '19.txt'


def read_data(filename):
    with open(filename) as f:
        pieces = f.readline().strip().split(', ')
        f.readline()
        patterns = []
        for line in f.readlines():
            patterns.append(line.strip())
    return patterns, pieces


def matchpat(pattern, pieces):
    if pattern == '':
        return True
    else:
        for piece in pieces:
            if pattern.startswith(piece) and matchpat(pattern[len(piece):], pieces):
                return True
        return False


@functools.cache
def countpat(pattern, pieces):
    if pattern == '':
        return 1
    else:
        count = 0
        for piece in pieces:
            if pattern.startswith(piece):
                count += countpat(pattern[len(piece):], pieces)
        return count


def code1(data):
    patterns, pieces = data
    return sum(matchpat(pattern, pieces) for pattern in patterns)


def code2(data):
    patterns, pieces = data
    return sum(countpat(pattern, tuple(pieces)) for pattern in patterns)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
