"""
--- 2015 ---
"""


import re
from collections import defaultdict
from itertools import permutations


EXAMPLES1 = (
    ('09-exemple1.txt', 605),
)

EXAMPLES2 = (
    ('09-exemple1.txt', 982),
)

INPUT = '09.txt'


def read_data(filename):
    distances = defaultdict(dict)
    with open(filename) as f:
        for line in f.readlines():
            match = re.match(r'(\w+) to (\w+) = (\d+)', line)
            city1, city2, dist = match.group(1, 2, 3)
            dist = int(dist)
            distances[city1][city2] = dist
            distances[city2][city1] = dist
    return distances


def code1(distances):
    cities = distances.keys()
    print(cities)
    mini = float('inf')
    for travel in permutations(cities, len(cities)):
        dist = sum(distances[city1][city2] for city1, city2 in zip(travel, travel[1:]))
        if dist < mini:
            mini = dist
            print(dist, travel)
    return mini


def code2(distances):
    cities = distances.keys()
    print(cities)
    maxi = 0
    for travel in permutations(cities, len(cities)):
        dist = sum(distances[city1][city2] for city1, city2 in zip(travel, travel[1:]))
        if dist > maxi:
            maxi = dist
            print(dist, travel)
    return maxi


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
