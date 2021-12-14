import functools
import operator
import math
from collections import Counter


EXAMPLES1 = (
    ('11-exemple1.txt', 3),
)

EXAMPLES2 = (
 )

INPUT = '11.txt'


def read_data(fn):
    with open(fn) as f:
        return f.readline().strip().split(',')


def distance(data):
    counter = Counter(data)
    # project on two axes (n-s and nw-se)
    counter['s'] += counter['sw']
    counter['nw'] += counter['sw']
    counter['sw'] = 0
    counter['n'] += counter['ne']
    counter['se'] += counter['ne']
    counter['ne'] = 0
    # find coordinates on each axe
    if counter['s'] > counter['n']:
        s, n = counter['s'] - counter['n'], 0
    else:
        s, n = 0, counter['n'] - counter['s']
    if counter['se'] > counter['nw']:
        se, nw = counter['se'] - counter['nw'], 0
    else:
        se, nw = 0, counter['nw'] - counter['se']
    # apply shortening transforms (s+nw = sw and n+se = ne)
    if s > nw:
        s, nw, sw = s - nw, 0, nw
    else:
        s, nw, sw = 0, nw - s, s
    if n > se:
        n, se, ne = n - se, 0, se
    else:
        n, se, ne = 0, se - n, n
    return s + n + se + nw + sw + ne


def code1(data):
    return distance(data)


def code2(data):
    maxdist = 0
    for last in range(len(data)):
        dist = distance(data[:last + 1])
        if dist > maxdist:
            maxdist = dist
    return maxdist


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
