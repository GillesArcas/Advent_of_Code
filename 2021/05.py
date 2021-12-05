import re
from collections import defaultdict


EXAMPLES1 = (
    ('05-exemple1.txt', 5),
)

EXAMPLES2 = (
    ('05-exemple1.txt', 12),
)

INPUT =  '05.txt'


def read_data(fn):
    data = list()
    with open(fn) as f:
        for line in f:
            match = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', line)
            x0, y0, x1, y1 = [int(x) for x in match.group(1, 2, 3, 4)]
            # if (x0, y0) > (x1, y1):
            if (y0, x0) > (y1, x1):
                x0, y0, x1, y1 = x1, y1, x0, y0
            data.append((x0, y0, x1, y1))
    return data


def code1(data):
    points = defaultdict(int)
    for x0, y0, x1, y1 in data:
        if x0 == x1:
            for y in range(y0, y1 + 1):
                points[(x0, y)] += 1
        elif y0 == y1:
            for x in range(x0, x1 + 1):
                points[(x, y0)] += 1

    return sum(x > 1 for x in points.values())


def code2(data):
    points = defaultdict(int)
    for x0, y0, x1, y1 in data:
        if x0 == x1:
            for y in range(y0, y1 + 1):
                points[(x0, y)] += 1
        elif y0 == y1:
            for x in range(x0, x1 + 1):
                points[(x, y0)] += 1
        elif x1 - x0 == y1 - y0:
            # main diagonal
            for x, y in zip(range(x0, x1 + 1), range(y0, y1 + 1)):
                points[(x, y)] += 1
        elif x0 - x1 == y1 - y0:
            # second diagonal
            for x, y in zip(range(x0, x1 - 1, -1), range(y0, y1 + 1)):
                points[(x, y)] += 1

    return sum(x > 1 for x in points.values())


def test(n, code, examples, myinput):
    for fn, result in examples:
        data = read_data(fn)
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
