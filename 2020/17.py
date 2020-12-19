import re
from collections import defaultdict


EXEMPLE = 0
if EXEMPLE == 0:
    DATA = '17.txt'
elif EXEMPLE == 1:
    DATA = '17-exemple1.txt'
elif EXEMPLE == 2:
    DATA = '17-exemple2.txt'
else:
    assert False


def init_cubes(xmin, xmax, ymin, ymax, zmin, zmax, wmin, wmax):
    cubes = dict()
    for w in range(wmin, wmax + 1):
        cubes[w] = dict()
        for z in range(zmin, zmax + 1):
            cubes[w][z] = dict()
            for y in range(ymin, ymax + 1):
                cubes[w][z][y] = dict()
                for x in range(xmin, xmax + 1):
                    cubes[w][z][y][x] = 0
    return cubes


def get_cube(cubes, x, y, z, w):
    return cubes[w][z][y][x]


def set_cube(cubes, x, y, z, w, val):
    # print('set', x, y, z, val)
    # print(list(cubes[z]))
    cubes[w][z][y][x] = val


def neighbours_active(cubes, x, y, z, w):
    n = 0
    for x2 in range(x - 1, x + 2):
        for y2 in range(y - 1, y + 2):
            for z2 in range(z - 1, z + 2):
                for w2 in range(w - 1, w + 2):
                    if x == x2 and y == y2 and z == z2 and w == w2:
                        pass
                    else:
                        n += get_cube(cubes, x2, y2, z2, w2)
    return n


def iter(cubes, xmin, xmax, ymin, ymax, zmin, zmax, wmin, wmax):
    cubes2 = init_cubes(xmin - 1, xmax + 1, ymin - 1, ymax + 1, zmin - 1, zmax + 1, wmin - 1, wmax + 1)
    for w in range(wmin, wmax + 1):
        for z in range(zmin, zmax + 1):
            for y in range(ymin, ymax + 1):
                for x in range(xmin, xmax + 1):
                    active = get_cube(cubes, x, y, z, w)
                    n = neighbours_active(cubes, x, y, z, w)
                    if active:
                        if n in (2, 3):
                            set_cube(cubes2, x, y, z, w, 1)
                        else:
                            set_cube(cubes2, x, y, z, w, 0)
                    else:
                        if n == 3:
                            set_cube(cubes2, x, y, z, w, 1)
                        else:
                            set_cube(cubes2, x, y, z, w, 0)
    return cubes2


def active_states(cubes, xmin, xmax, ymin, ymax, zmin, zmax, wmin, wmax):
    n = 0
    for w in range(wmin, wmax + 1):
        for z in range(zmin, zmax + 1):
            for y in range(ymin, ymax + 1):
                for x in range(xmin, xmax + 1):
                    active = get_cube(cubes, x, y, z, w)
                    n += active
    return n


def read_data(niter):
    cubes = dict()
    with open(DATA) as f:
        lines = [line.strip() for line in f.readlines()]
    xmin, xmax = 0 - niter, niter + len(lines[0])
    ymin, ymax = 0 - niter, niter + len(lines)
    zmin, zmax = 0 - niter, niter + 0
    wmin, wmax = 0 - niter, niter + 0

    cubes = init_cubes(xmin - 1, xmax + 1, ymin - 1, ymax + 1, zmin - 1, zmax + 1, wmin - 1, wmax + 1)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            set_cube(cubes, x, y, 0, 0, 1 if char == '#' else 0)

    return cubes, xmin, xmax, ymin, ymax, zmin, zmax, wmin, wmax


def print_cubes(cubes, xmin, xmax, ymin, ymax, zmin, zmax, wmin, wmax):
    for z in range(zmin, zmax + 1):
        print('z=', z)
        for y in range(ymin, ymax + 1):
            print(''.join('#' if cubes[0][z][y][x] else '.' for x in range(xmin, xmax + 1)))
        print()


def code1():
    cubes, xmin, xmax, ymin, ymax, zmin, zmax, wmin, wmax = read_data(6)
    print_cubes(cubes, xmin, xmax, ymin, ymax, 0, 0, 0, 0)

    for i in range(6):
        cubes = iter(cubes, xmin, xmax, ymin, ymax, zmin, zmax, wmin, wmax)
        print_cubes(cubes, xmin, xmax, ymin, ymax, 0, 0, 0, 0)
    print('>', active_states(cubes, xmin, xmax, ymin, ymax, zmin, zmax, wmin, wmax))


def code2():
    pass


code1()
code2()
