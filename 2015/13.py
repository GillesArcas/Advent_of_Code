"""
--- 2015 --- Day 13: Knights of the Dinner Table ---
"""


import re
from collections import defaultdict
from itertools import permutations


EXAMPLES1 = (
    ('13-exemple1.txt', 330),
)

EXAMPLES2 = (
)

INPUT = '13.txt'


def read_data(filename):
    units = defaultdict(dict)
    with open(filename) as f:
        for line in f:
            match = re.match(r'(\w+) would (lose|gain) (\d+) happiness units by sitting next to (\w+)', line)
            x, lg, n, y = match.group(1, 2, 3, 4)
            n = int(n)
            if lg == 'lose':
                n = -n
            units[x][y] = n
    return units


def code1(units):
    people = units.keys()
    maxi = 0
    for perm in permutations(people, len(people)):
        gain = sum(units[person1][person2] + units[person2][person1] for person1, person2 in zip(perm, perm[1:]))
        gain += units[perm[-1]][perm[0]] + units[perm[0]][perm[-1]]
        if gain > maxi:
            maxi = gain
            print(gain, perm)
    return maxi


def code2(units):
    people = list(units.keys())
    for person in people:
        units[person]['me'] = 0
        units['me'][person] = 0
    people = units.keys()

    maxi = 0
    for perm in permutations(people, len(people)):
        gain = sum(units[person1][person2] + units[person2][person1] for person1, person2 in zip(perm, perm[1:]))
        gain += units[perm[-1]][perm[0]] + units[perm[0]][perm[-1]]
        if gain > maxi:
            maxi = gain
            print(gain, perm)
    return maxi


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
