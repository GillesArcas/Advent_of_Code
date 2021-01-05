import math
from collections import defaultdict


DATASET = 0
if DATASET == 0:
    DATA = '10.txt'
elif DATASET == 1:
    DATA = '10-exemple1.txt'
elif DATASET == 2:
    DATA = '10-exemple2.txt'
else:
    assert False


def code1():
    with open(DATA) as f:
        data = [_.strip() for _ in f.readlines()]

    asteroids = list()
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '#':
                asteroids.append((x, y))

    maxseen = 0
    bestast = None
    for (x, y) in asteroids:
        seen = set()
        for (x2, y2) in asteroids:
            if (x2, y2) != (x, y):
                dx, dy = x2 - x, y2 - y
                gcd = math.gcd(dx, dy)
                dx, dy = dx // gcd, dy // gcd
                seen.add((dx, dy))
        if len(seen) > maxseen:
            maxseen = len(seen)
            bestast = (x, y)

    print('1>', maxseen)
    return bestast, asteroids


def angle(p):
    """
    p = (x, y), return angle from y axis
    """
    x, y = p
    p = x, -y
    a = math.pi / 2 - math.atan2(*reversed(p))
    if a < 0:
        a += 2 * math.pi
    return a


def code2(p, asteroids):
    x, y = p
    angle_to_ast = defaultdict(list)
    for (x2, y2) in asteroids:
        if (x2, y2) != p:
            dx, dy = x2 - x, y2 - y
            a = angle((dx, dy))
            angle_to_ast[a].append((x2, y2))

    for a, ast in angle_to_ast.items():
        angle_to_ast[a] = sorted(ast, key=lambda p: abs(p[0] - x) + abs(p[1] - y))

    angles = sorted(angle_to_ast.keys())
    a = 0
    for k in range(200):
        while not angle_to_ast[angles[a]]:
            a = (a + 1) % len(angles)
        p = angle_to_ast[angles[a]].pop(0)
        print(k, angles[a], p)
        a = (a + 1) % len(angles)

    print('2>', p, p[0] * 100 + p[1])


p, asteroids = code1()
code2(p, asteroids)
