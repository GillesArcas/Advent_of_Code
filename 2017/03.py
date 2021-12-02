import math
import itertools
from collections import defaultdict


EXAMPLES1 = (
    (1, 0),
    (12, 3),
    (23, 2),
    (1024, 31),
)

EXAMPLES2 = (
)

INPUT =  289326


def iterij():
    i = 0
    j = 0
    yield i, j
    for radius in itertools.count(1):
        j += 1
        yield i, j

        root = 2 * radius + 1

        for _ in range(1, root - 1):
            i -= 1
            yield i, j
        for _ in range(root - 1):
            j -= 1
            yield i, j
        for _ in range(root - 1):
            i += 1
            yield i, j
        for _ in range(root - 1):
            j += 1
            yield i, j


def code1(data):
    for i, j in itertools.islice(iterij(), data):
        pass
    return abs(i) + abs(j)


def code2(data):
    array = defaultdict(lambda: defaultdict(int))
    array[0][0] = 1
    for i, j in iterij():
        array[i][j] = sum(array[i + i2][j + j2] for i2 in (-1, 0, 1) for j2 in (-1, 0, 1))
        if array[i][j] > data:
            return array[i][j]


def test(n, code, examples, myinput):
    for data, result in examples:
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(myinput))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
