"""
--- Day 8: Resonant Collinearity ---
"""


import itertools
from collections import defaultdict


EXAMPLES1 = (
    ('08-exemple1.txt', 14),
)

EXAMPLES2 = (
    ('08-exemple1.txt', 34),
)

INPUT = '08.txt'


def read_data(filename):
    antennas = defaultdict(set)
    with open(filename) as f:
        array = f.readlines()
    for i, line in enumerate(array):
        for j, char in enumerate(line.strip()):
            if char != '.':
                antennas[char].add((i, j))
    return len(array), len(array[0].strip()), antennas


def code1(data):
    idim, jdim, antennas = data
    antinodes = [[0 for j in range(jdim)] for i in range(idim)]

    for coords in antennas.values():
        for coord0, coord1 in itertools.combinations(coords, 2):
            i1 = 2 * coord0[0] - coord1[0]
            j1 = 2 * coord0[1] - coord1[1]
            i2 = 2 * coord1[0] - coord0[0]
            j2 = 2 * coord1[1] - coord0[1]
            for i, j in ((i1, j1), (i2, j2)):
                if 0 <= i < idim and 0 <= j < jdim:
                    antinodes[i][j] = 1

    #for line in antinodes:
    #    print(''.join([str(_) for _ in line]))

    return sum(sum(line) for line in antinodes)


def code2(data):
    idim, jdim, antennas = data
    antinodes = [[0 for j in range(jdim)] for i in range(idim)]

    for coords in antennas.values():
        for coord0, coord1 in itertools.combinations(coords, 2):
            antinodes[coord0[0]][coord0[1]] = 1
            antinodes[coord1[0]][coord1[1]] = 1

            i = 2 * coord0[0] - coord1[0]
            j = 2 * coord0[1] - coord1[1]
            while 0 <= i < idim and 0 <= j < jdim:
                antinodes[i][j] = 1
                i += coord0[0] - coord1[0]
                j += coord0[1] - coord1[1]

            i = 2 * coord1[0] - coord0[0]
            j = 2 * coord1[1] - coord0[1]
            while 0 <= i < idim and 0 <= j < jdim:
                antinodes[i][j] = 1
                i += coord1[0] - coord0[0]
                j += coord1[1] - coord0[1]

    #for line in antinodes:
    #    print(''.join([str(_) for _ in line]))

    return sum(sum(line) for line in antinodes)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
