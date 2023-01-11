"""
--- 2015 --- Day 24: It Hangs in the Balance ---
"""


import math
from itertools import combinations


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '24.txt'


def read_data(filename):
    with open(filename) as f:
        return [int(_) for _ in f.readlines()]


def first_comb(data, S):
    firstcomb = []
    for size in range(1, len(data)):
        for comb in combinations(data, size):
            if sum(comb) == S:
                firstcomb.append(comb)
        if firstcomb:
            return firstcomb
    return None


def code1(data):
    S = sum(data) // 3
    firstcomb = first_comb(data, S)
    return min(math.prod(c) for c in firstcomb)


def code2(data):
    S = sum(data) // 4
    firstcomb = first_comb(data, S)
    return min(math.prod(c) for c in firstcomb)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
