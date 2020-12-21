import math


with open('03.txt') as f:
    lines = [_.strip() for _ in f.readlines()]


# ligne i --> j = 3i indéfini en i = 0


def n_trees(right, down):
    ntrees = 0
    for i, line in enumerate(lines[down::down], 1):
        if line[(right * i) % len(line)] == '#':
            ntrees += 1
    return ntrees


def code1():
    print(n_trees(3, 1))


def code2():
    STEPS = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    for steps in STEPS:
        print(n_trees(*steps))
    print(math.prod(n_trees(*steps) for steps in STEPS))


code2()
