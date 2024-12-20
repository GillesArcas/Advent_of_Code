"""
--- Day 12: Garden Groups ---
"""


import collections


EXAMPLES1 = (
    ('12-exemple1.txt', 140),
    ('12-exemple2.txt', 1930),
)

EXAMPLES2 = (
    ('12-exemple1.txt', 80),
    ('12-exemple2.txt', 1206),
    ('12-exemple3.txt', 236),
    ('12-exemple4.txt', 368),
)

INPUT = '12.txt'


def read_data(filename):
    with open(filename) as f:
        return [list(_.strip()) for _ in f.readlines()]


def neighbours(mymap, i, j):
    for ii, jj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
        if 0 <= ii < len(mymap) and 0 <= jj < len(mymap[0]):
            if mymap[ii][jj] == mymap[i][j]:
                yield ii, jj


def find_region(data, i, j):
    region = set()
    region.add((i, j))
    stack = [(i, j)]
    while stack:
        i, j = stack.pop()
        for ii, jj in neighbours(data, i, j):
            if (ii, jj) not in region:
                region.add((ii, jj))
                stack.append((ii, jj))
    return region


def find_regions(data):
    regions = []
    notseen = set()
    for i, line in enumerate(data):
        for j, _ in enumerate(line):
            notseen.add((i, j))
    while notseen:
        region = find_region(data, *list(notseen)[0])
        regions.append(region)
        notseen = notseen.difference(region)
    return regions


def perimeter(region):
    p = 0
    for i, j in region:
        for ii, jj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if (ii, jj) not in region:
                p += 1
    return p


def code1(data):
    regions = find_regions(data)
    result = 0
    for region in regions:
        result += len(region) * perimeter(region)
    return result


def find_sides(region):
    hside = collections.defaultdict(set)
    vside = collections.defaultdict(set)
    for i, j in region:
        if (i - 1, j) not in region:
            hside[i, 0].add((j, j + 1))
        if (i + 1, j) not in region:
            hside[i, 1].add((j, j + 1))
        if (i, j - 1) not in region:
            vside[j, 0].add((i, i + 1))
        if (i, j + 1) not in region:
            vside[j, 1].add((i, i + 1))

    nsides = 0
    for sides in (hside, vside):
        for liste in sides.values():
            liste = sorted(liste)
            nsides += 1
            for x, y in zip(liste[:-1], liste[1:]):
                if x[1] != y[0]:
                    nsides += 1
    return nsides


def code2(data):
    regions = find_regions(data)
    result = 0
    for region in regions:
        result += len(region) * find_sides(region)
    return result


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
