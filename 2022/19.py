"""
--- 2022 --- Day 19: Not Enough Minerals ---
"""


import re
import msvcrt
import random
from collections import Counter, defaultdict

kbhit_trace = False


EXAMPLES1 = (
    # ('19-exemple1.txt', 33),
)

EXAMPLES2 = (
    ('19-exemple1.txt', 56 * 62),
)

INPUT = '19.txt'


def read_data(filename):
    kinds = 'ore clay obsidian geode'.split()
    blueprints = []

    with open(filename) as f:
        for line in f.readlines():
            x = re.findall(r'Each (\w+) robot costs ([^.]*)\.', line)
            blueprint = [None] * 4
            for kind, strcosts in x:
                costs = [0, 0, 0, 0]
                y = re.findall(r'(\d+) (\w+)', strcosts)
                for c, k in y:
                    costs[kinds.index(k)] = int(c)
                blueprint[kinds.index(kind)] = costs
            blueprints.append(blueprint)

    return blueprints


cache = dict()


def next_states(blueprint, robots, collected):
    states = set()

    # find robots to build
    may_build = []
    for kind, costs in enumerate(blueprint):
        if all(x <= y for x, y in zip(costs, collected)):
            may_build.append(kind)

    # update collected without building
    newcollected = tuple([x + 1 * y for x, y in zip(collected, robots)])

    # new states with building one
    for robot in reversed(may_build):
        newrobots = list(robots)
        newrobots[robot] += 1
        newrobots = tuple(newrobots)
        newcollected2 = tuple([x - y for x, y in zip(newcollected, blueprint[robot])])
        states.add((newrobots, newcollected2))
        # if robot == 3:
            # break

    # new states without building
    states.add((robots, newcollected))
    # if 3 in may_build:
        # pass
    # else:
        # states.add((robots, newcollected))

    # print('-', len(states), states)
    return states


def filter_on_collected(states):
    sets = defaultdict(set)
    for robots, collected in states:
        sets[robots].add(collected)

    newstates = set()
    for robots, set1 in sets.items():
        ordered_collected = list(sorted(set1))
        # print(ordered_robots)
        newset = set()
        for index, collected in enumerate(ordered_collected):
            for collected2 in ordered_collected[index + 1:]:
                if all(c1 <= c2 for c1, c2 in zip(collected, collected2)):
                    # if random.random() > 0.9:
                        break
            else:
                newstates.add((robots, collected))
                newset.add(collected)
        # print(newset)

    return newstates


def filter_on_robots(states):
    sets = defaultdict(set)
    for robots, collected in states:
        sets[collected].add(robots)

    newstates = set()
    for collected, set1 in sets.items():
        ordered_robots = list(sorted(set1))
        # print(ordered_robots)
        newset = set()
        for index, robots in enumerate(ordered_robots):
            for robots2 in ordered_robots[index + 1:]:
                if all(robot1 <= robot2 for robot1, robot2 in zip(robots, robots2)):
                    break
            else:
                newstates.add((robots, collected))
                newset.add(robots)
        # print(newset)

    return newstates


def filter_on_max(states):
    maxi = 0
    for state in states:
        robots, collected = state
        maxi = max(maxi, collected[3])

    newstates = set()
    for state in states:
        robots, collected = state
        if collected[3] == maxi:
            newstates.add(state)

    return newstates


def develop_blueprint(blueprint, time):
    # best filter : collected then robots
    states = {((1, 0, 0, 0), (0, 0, 0, 0))}
    for t in range(time):
        newstates = set()
        for state in states:
            robots, collected = state
            newstates = newstates.union(next_states(blueprint, robots, collected))
        states = newstates

        if 1:
            states = filter_on_collected(states)

        if 1:
            states = filter_on_robots(states)

        if 0:
            states = filter_on_max(states)

        maxi = 0
        for state in states:
            robots, collected = state
            maxi = max(maxi, collected[3])
        print(t, len(states), maxi)

    return maxi


def code1(blueprints):
    r = 0
    for index, blueprint in enumerate(blueprints):
        n = develop_blueprint(blueprint, 24)
        print(blueprint, n)
        r += (index + 1) * n
    return r


def code2(blueprints):
    r = 1
    for _, blueprint in enumerate(blueprints[:3]):
        n = develop_blueprint(blueprint, 32)
        print(blueprint, n)
        r *= n
    return r


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    # print(f'{n}>', code(read_data(myinput)))


# test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
