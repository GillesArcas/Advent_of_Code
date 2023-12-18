"""
--- Day 12: Hot Springs ---
"""


import re
from functools import cache


EXAMPLES1 = (
    ('12-exemple1.txt', 21),
)

EXAMPLES2 = (
    ('12-exemple1.txt', 525152),
)

INPUT = '12.txt'


def read_data(filename):
    data = []
    with open(filename) as f:
        for line in f:
            springs, s = line.strip().split()
            data.append((springs, tuple(int(_) for _ in s.split(','))))
    return data


@cache
def match_group(springs, n):
    regex = re.compile('[^.]{%d}([^#]|$)' % n)
    rests = []
    for i, char in enumerate(springs):
        if char == '.':
            pass
        elif match := regex.match(springs[i:]):
            rests.append(springs[i + match.end(0):])
        if char == '#':
            break
    return rests


@cache
def spring_arrangements(springs, groups):
    if not groups and re.match('[^#]*$', springs):
        return 1
    elif not groups:
        return 0
    else:
        count = 0
        for springs_rest in match_group(springs, groups[0]):
            count += spring_arrangements(springs_rest, groups[1:])
        return count


def unfold_groups(springs, groups, nfolds):
    return '?'.join([springs] * nfolds), groups * nfolds


def code1(data):
    count = 0
    for springs, groups in data:
        count += spring_arrangements(springs, groups)
    return count


def code2(data):
    count = 0
    for springs, groups in data:
        count += spring_arrangements(*unfold_groups(springs, groups, 5))
    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
