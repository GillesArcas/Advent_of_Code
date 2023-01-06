"""
--- 2015 --- Day 14: Reindeer Olympics ---
"""


import re
from collections import defaultdict


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '14.txt'


def read_data(filename):
    reinders = {}
    with open(filename) as f:
        for line in f:
            reinder = line.split(' ', 1)[0]
            reinders[reinder] = [int(_) for _ in re.findall(r'\d+', line)]
    return reinders


def distance(speed, run, rest, duration):
    nbperiods = duration // (run + rest)
    remain = min(run, duration % (run + rest))
    dist = nbperiods * run * speed + remain * speed
    return dist


def code1(reinders):
    duration = 2503
    maxi = 0
    for _, data in reinders.items():
        dist = distance(*data, duration)
        maxi = max(maxi, dist)
    return maxi


def code2(reinders):
    duration = 2503
    points = defaultdict(int)
    for t in range(1, duration + 1):
        maxdist = 0
        for reinder, data in reinders.items():
            dist = distance(*data, t)
            if dist > maxdist:
                maxdist = dist
                maxreinder = reinder
        points[maxreinder] += 1
    return max(points.values())


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
