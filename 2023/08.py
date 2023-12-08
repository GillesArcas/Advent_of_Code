"""
--- Day 8: Haunted Wasteland ---
"""


import re
import itertools
import math


EXAMPLES1 = (
    ('08-exemple1.txt', 2),
    ('08-exemple2.txt', 6),
)

EXAMPLES2 = (
    ('08-exemple3.txt', 6),
)

INPUT = '08.txt'


def read_data(filename):
    nodes = {}
    with open(filename) as f:
        instructions = f.readline().strip()
        f.readline()
        for line in f:
            node, left, right = re.findall(r'\w+', line)
            nodes[node] = (left, right)
    return instructions, nodes


def code1(data):
    instructions, nodes = data
    node = 'AAA'
    for count, instruction in enumerate(itertools.cycle(instructions), 1):
        left, right = nodes[node]
        node = left if (instruction == 'L') else right
        if node == 'ZZZ':
            return count


def code2_naive(data):
    instructions, nodes = data
    curnodes = [node for node in nodes if node[-1] == 'A']
    for count, instruction in enumerate(itertools.cycle(instructions), 1):
        nextnodes = []
        for node in curnodes:
            left, right = nodes[node]
            nextnodes.append(left if (instruction == 'L') else right)
        if all(node[-1] == 'Z' for node in curnodes):
            return count


def find_z_period(node, nodes, instructions):
    ztimes = []
    for count, instruction in enumerate(itertools.cycle(instructions), 1):
        left, right = nodes[node]
        node = left if (instruction == 'L') else right
        if node[-1] == 'Z':
            ztimes.append(count)
            if len(ztimes) == 10:
                return ztimes


def code2(data):
    instructions, nodes = data
    curnodes = [node for node in nodes if node[-1] == 'A']

    # this enables to assume that Z occurs with a period to the time of its first occurrence
    all_ztimes = [find_z_period(node, nodes, instructions) for node in curnodes]
    for ztimes in all_ztimes:
        assert all(_ % ztimes[0] == 0 for _ in ztimes)

    periods = [ztimes[0] for ztimes in all_ztimes]
    return math.lcm(*periods)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
