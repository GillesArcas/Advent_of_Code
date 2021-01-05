import math
import re
import itertools


DATASET = 0
if DATASET == 0:
    DATA = '12.txt'
    NBSTEPS = 1000
elif DATASET == 1:
    DATA = '12-exemple1.txt'
    NBSTEPS = 10
elif DATASET == 2:
    DATA = '12-exemple2.txt'
    NBSTEPS = 100
else:
    assert False


class Moon:
    def __init__(self, string):
        # string: <x=-1, y=0, z=2>
        self.p = [0, 0, 0]
        self.v = [0, 0, 0]
        self.dv = [0, 0, 0]
        for i, m in enumerate(re.finditer(r'[xyz]=(-?\d+)', string)):
            self.p[i] = int(m.group(1))

    def __str__(self):
        x = self.p + self.v
        return 'pos=<x=%d, y=%d, z=%d>, vel=<x=%d, y=%d, z=%d>' % tuple(x)

    def energy(self):
        return sum(abs(_) for _ in self.p) * sum(abs(_) for _ in self.v)

    def key(self, coord):
        return (self.p[coord], self.v[coord])


def adjust_velocity(moons):
    for moon in moons:
        for axe in range(3):
            moon.dv[axe] = 0

    for moon1, moon2 in itertools.combinations(moons, 2):
        for axe in range(3):
            if moon1.p[axe] == moon2.p[axe]:
                pass
            elif moon1.p[axe] < moon2.p[axe]:
                moon1.dv[axe] += 1
                moon2.dv[axe] -= 1
            else:
                moon1.dv[axe] -= 1
                moon2.dv[axe] += 1

    for moon in moons:
        for axe in range(3):
            moon.v[axe] += moon.dv[axe]
            moon.p[axe] += moon.v[axe]


def state(moons, coord):
    return tuple(sum([[moon.p[coord], moon.v[coord]] for moon in moons], []))


def code1():
    moons = list()
    with open(DATA) as f:
        for s in f:
            moons.append(Moon(s))
    for k in range(1, NBSTEPS + 1):
        print(k)
        adjust_velocity(moons)
        for moon in moons:
            print(moon, moon.energy())
        print('1>', sum(moon.energy() for moon in moons))


def code2():
    moons = list()
    with open(DATA) as f:
        for s in f:
            moons.append(Moon(s))

    repeat_pos = [0] * 3

    for coord in range(3):
        states = dict()
        states[state(moons, coord)] = 0
        for k in itertools.count(start=1):
            adjust_velocity(moons)
            key = state(moons, coord)
            if key in states:
                print(states[key], k, k - states[key])
                repeat_pos[coord] = k
                break
            else:
                states[key] = k
    print('2>', math.lcm(*repeat_pos))


# code1()
code2()
