import re
from collections import defaultdict


EXAMPLES1 = (
    ('22-exemple0.txt', 39),
    ('22-exemple1.txt', 590784),
    ('22-exemple1-short.txt', 590784),
    ('22-exemple2.txt', 474140),
)

EXAMPLES2 = (
    ('22-exemple0.txt', 39),
    ('22-exemple1-short.txt', 590784),
    ('22-exemple2.txt', 2758514936282235),
)

INPUT = '22.txt'


def read_list(fn):
    steps = list()
    with open(fn) as f:
        for line in f:
            match = re.match(r'(o[nf]+) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)', line)
            on, x1, x2, y1, y2, z1, z2 = match.group(1, 2, 3, 4, 5, 6, 7)
            steps.append((int(on == 'on'), int(x1), int(x2), int(y1), int(y2), int(z1), int(z2)))
    return steps


def code1(steps):
    cubes = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for on, x1, x2, y1, y2, z1, z2 in steps:
        if -50 <= x1 <= x2 <= 50 and -50 <= y1 <= y2 <= 50 and -50 <= z1 <= z2 <= 50:
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    for z in range(z1, z2 + 1):
                        cubes[x][y][z] = on

    count = 0
    for square in cubes.values():
        for line in square.values():
            count += sum(line.values())
    return count


def inter_seg(x1, x2, x1_, x2_):
    if x1 == x1_ and x2 == x2_:
        return (x1, x2), None, None
    else:
        min1 = min(x1, x1_)
        max1 = max(x1, x1_)
        min2 = min(x2, x2_)
        max2 = max(x2, x2_)
        if max1 > min2:
            return None, (x1, x2), (x1_, x2_)
        elif x1 == x1_:
            return (max1, min2), None, (min2 + 1, max2)
        elif x2 == x2_:
            return (max1, min2), (min1, max1 - 1), None
        else:
            return (max1, min2), (min1, max1 - 1), (min2 + 1, max2)


def included(coord1, coord2):
    x11, x12, y11, y12, z11, z12 = coord1
    x21, x22, y21, y22, z21, z22 = coord2
    return x21 <= x11 and x12 <= x22 and y21 <= y11 and y12 <= y22 and z21 <= z11 and z12 <= z22


def inter_cuboid(cuboid1, cuboid2):
    # cuboid1 = step cuboid
    on1, x11, x12, y11, y12, z11, z12 = cuboid1
    on2, x21, x22, y21, y22, z21, z22 = cuboid2

    interx, interx2, interx3 = inter_seg(x11, x12, x21, x22)
    intery, intery2, intery3 = inter_seg(y11, y12, y21, y22)
    interz, interz2, interz3 = inter_seg(z11, z12, z21, z22)

    new_cuboids = set()
    if interx is None or intery is None or interz is None:
        new_cuboids.add(cuboid2)
    else:
        for segx in (interx, interx2, interx3):
            if segx is None:
                continue
            for segy in (intery, intery2, intery3):
                if segy is None:
                    continue
                for segz in (interz, interz2, interz3):
                    if segz is None:
                        continue
                    if included((*segx, *segy, *segz), cuboid2[1:]) and not included((*segx, *segy, *segz), cuboid1[1:]):
                        new_cuboids.add((on2, *segx, *segy, *segz))
                    else:
                        pass

    return new_cuboids


def vol_cuboid(cuboid):
    on, x1, x2, y1, y2, z1, z2 = cuboid
    return (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)


def code2(steps):
    cuboids = list()
    cuboids.append(steps[0])
    for step in steps[1:]:
        new_cuboids = set()
        for cuboid in cuboids:
            new_cuboids.update(inter_cuboid(step, cuboid))
        if step[0]:
            new_cuboids.add(step)
        cuboids = new_cuboids

    return sum(vol_cuboid(cuboid) for cuboid in cuboids)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_list(fn)
        result = code(data)
        assert result == expected, (data, expected, result)

    print(f'{n}>', code(read_list(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
