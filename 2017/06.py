import math
import itertools
from collections import defaultdict


EXAMPLES1 = (
    ((0,2, 7,0), 5),
)

EXAMPLES2 = (
    ((0,2, 7,0), 4),
)

INPUT =  (0, 5, 10, 0, 11, 14, 13, 4, 11, 8, 8, 7, 1, 4, 12, 11)


def redis(data):
    max_index = max(range(len(data)), key=data.__getitem__)
    max_value = data[max_index]
    data[max_index] = 0
    for index in range(max_index + 1, max_index + 1 + max_value):
        data[index % len(data)] += 1


def code1(data):
    data = list(data)
    nbredis = 0
    dejavu = set()
    dejavu.add(tuple(data))
    while True:
        redis(data)
        nbredis += 1
        if tuple(data) in dejavu:
            return nbredis
        else:
            dejavu.add(tuple(data))


def code2(data):
    data = list(data)
    nbredis = 0
    dejavu = dict()
    dejavu[tuple(data)] = 0
    while True:
        redis(data)
        nbredis += 1
        if tuple(data) in dejavu:
            return nbredis - dejavu[tuple(data)]
        else:
            dejavu[tuple(data)] = nbredis


def test(n, code, examples, myinput):
    for data, result in examples:
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(myinput))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
