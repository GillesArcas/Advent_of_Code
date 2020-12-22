import functools


DATASET = 1
if DATASET == 0:
    DATA = '11-exemple.txt'
else:
    DATA = '11.txt'


def read_pos(bord):
    with open(DATA) as f:
        if bord:
            pos = [list('.' + _.strip()  + '.') for _ in f.readlines()]
            floor = list('.' * len(pos[0]))
            return [floor, *pos, floor]
        else:
            pos = [list( _.strip()) for _ in f.readlines()]
            return pos


def iterate(pos):
    pos2 = [_[:] for _ in pos]
    for i, line in enumerate(pos[1:-1], 1):
        for j, x in enumerate(line[1:-1], 1):
            n_occupied = 0
            n_empty = 0
            for i2 in range(i - 1, i + 2):
                for j2 in range(j - 1, j + 2):
                    if pos[i2][j2] == '#':
                        n_occupied += 1
                    elif pos[i2][j2] == 'L':
                        n_empty += 1
            if x == 'L' and n_occupied == 0:
                pos2[i][j] = '#'
            elif x == '#' and n_occupied >= 5:
                pos2[i][j] = 'L'
    return pos2


def iterate2(pos):
    pos2 = [_[:] for _ in pos]
    for i, line in enumerate(pos):
        for j, x in enumerate(line):
            n_occupied = 0
            n_occupied = count_neighbour_dir(n_occupied, pos, i, j, range(-1, -1000, -1), [0] * 1000) # N
            n_occupied = count_neighbour_dir(n_occupied, pos, i, j, range(+1, +1000, +1), [0] * 1000) # S
            n_occupied = count_neighbour_dir(n_occupied, pos, i, j, [0] * 1000, range(-1, -1000, -1)) # W
            n_occupied = count_neighbour_dir(n_occupied, pos, i, j, [0] * 1000, range(+1, +1000, +1)) # E
            n_occupied = count_neighbour_dir(n_occupied, pos, i, j, range(-1, -1000, -1), range(+1, +1000, +1)) # NE
            n_occupied = count_neighbour_dir(n_occupied, pos, i, j, range(+1, +1000, +1), range(+1, +1000, +1)) # SE
            n_occupied = count_neighbour_dir(n_occupied, pos, i, j, range(+1, +1000, +1), range(-1, -1000, -1)) # SW
            n_occupied = count_neighbour_dir(n_occupied, pos, i, j, range(-1, -1000, -1), range(-1, -1000, -1)) # NW
            if x == 'L' and n_occupied == 0:
                pos2[i][j] = '#'
            elif x == '#' and n_occupied >= 5:
                pos2[i][j] = 'L'
    return pos2


def count_neighbour_dir(n_occupied, pos, i, j, delta_i, delta_j):
    for di, dj in zip(delta_i, delta_j):
        i2 = i + di
        j2 = j + dj
        if i2 < 0 or j2 < 0 or i2 >= len(pos) or j2 >= len(pos[0]):
            return n_occupied
        if pos[i2][j2] == '#':
            n_occupied += 1
            return n_occupied
        if pos[i2][j2] == 'L':
            return n_occupied
    return n_occupied


def code1():
    niter = 0
    pos = read_pos(bord=True)
    for _ in pos:print(_)
    print()
    while True:
        pos2 = iterate(pos)
        niter += 1
        for _ in pos2:print(_)
        print()
        if pos2 == pos:
            break
        else:
            pos = pos2
    print('>', sum(sum(c == '#' for c in line) for line in pos))


def code2():
    niter = 0
    pos = read_pos(bord=False)
    for _ in pos:print(''.join(_))
    print()
    while True:
        pos2 = iterate2(pos)
        niter += 1
        for _ in pos2:print(''.join(_))
        print()
        if pos2 == pos:
            break
        else:
            pos = pos2
    print('>', sum(sum(c == '#' for c in line) for line in pos))


#code1()
code2()
