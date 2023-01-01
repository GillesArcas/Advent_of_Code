"""
--- 2016 --- Day 11: Radioisotope Thermoelectric Generators ---
"""


import re
from itertools import combinations


EXAMPLES1 = (
    ('11-exemple1.txt', 11),
)

EXAMPLES2 = (
)

INPUT = '11.txt'


def readline(line):
    if 'nothing' in line:
        return tuple()
    else:
        x = [_[:2].capitalize() + 'G' for _ in re.findall('[a-z]+ generator', line)]
        y = [_[:2].capitalize() + 'M' for _ in re.findall('[a-z]+-compatible microchip', line)]
        return tuple(sorted(x + y))


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()
    return tuple([0] + [readline(line) for line in lines])


def allowed(floor):
    for item in floor:
        if item[2] == 'M':
            if any(_[2] == 'G' for _ in floor) and item[:2] + 'G' not in floor:
                return False
    return True


def new_states(state):
    numfloor, *floors = state
    floor = floors[numfloor]
    states = []
    if not floor:
        for numfloor2 in ((1,), (0, 2), (1, 3), (2,))[numfloor]:
            newstate = tuple([numfloor2] + list(floors))
            states.append(tuple(newstate))
    else:
        ascloads = [[_] for _ in floor]
        for item1, item2 in combinations(floor, 2):
            ascloads.append([item1, item2])

        for numfloor2 in ((1,), (0, 2), (1, 3), (2,))[numfloor]:
            for load in ascloads:
                newfloor1 = tuple(sorted(set(floor).difference(set(load))))
                newfloor2 = tuple(sorted(list(floors[numfloor2]) + load))
                if allowed(newfloor1) and allowed(newfloor2):
                    newfloors = list(floors)
                    newfloors[numfloor] = newfloor1
                    newfloors[numfloor2] = newfloor2
                    states.append(tuple([numfloor2] + newfloors))
    return states


def endstate(state):
    numfloor, *floors = state
    return numfloor == 3 and all((not _) for _ in floors[:3])


def explore(depth, state):
    dejavu = set()
    queue = []
    queue.append((depth, state))
    while queue:
        depth, state = queue.pop(0)
        if endstate(state):
            return depth
        else:
            for state2 in new_states(state):
                if state2 not in dejavu:
                    dejavu.add(state2)
                    queue.append((depth + 1, state2))


def code1(state):
    return explore(0, state)


def code2(state):
    # 2000 seconds
    _, f1, f2, f3, f4 = state
    f1 = tuple(sorted(list(f1) + ['ElG', 'ElM', 'DiG', 'DiM']))
    state = (0, f1, f2, f3, f4)
    return explore(0, state)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
