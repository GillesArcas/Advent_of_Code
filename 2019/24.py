def get_data(n):
    if n == 0:  # problem
        tiles = '''\
            ####.
            #....
            #..#.
            .#.#.
            ##.##'''
    elif n == 1:  # example
        tiles = '''\
            ....#
            #..#.
            #..##
            ..#..
            #....'''

    return [list(line.strip()) for line in tiles.splitlines()]


def print_tiles(tiles):
    for line in tiles:
        print(''.join(line))


def neighbours(i, j):
    return [(i2, j2) for (i2, j2) in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))
            if 0 <= i2 < 5 and 0 <= j2 < 5]


def nb_neighbour_bugs(tiles, i, j):
    return sum(tiles[i2][j2] == '#' for (i2, j2) in neighbours(i, j))


def next_generation(tiles):
    next_tiles = [['.'] * 5 for _ in range(5)]
    for i in range(5):
        for j in range(5):
            nb = nb_neighbour_bugs(tiles, i, j)
            if tiles[i][j] == '#':
                if nb == 1:
                    next_tiles[i][j] = '#'
            else:
                if nb in (1, 2):
                    next_tiles[i][j] = '#'
    return next_tiles


def biorating(tiles):
    s = ''.join(''.join(line) for line in tiles)
    return sum(2 ** i for i, c in enumerate(s) if s[i] == '#')


def code1(n):
    tiles = get_data(n)
    cache = set()
    cache.add(''.join(''.join(line) for line in tiles))
    while 1:
        tiles = next_generation(tiles)
        key = ''.join(''.join(line) for line in tiles)
        if key in cache:
            break
        else:
            cache.add(key)
    print_tiles(tiles)
    print('1>', biorating(tiles))


def neighbours2(k, i, j):
    coords = [(k, i - 1, j), (k, i + 1, j), (k, i, j - 1), (k, i, j + 1)]

    for index, (k, i2, j2) in enumerate(coords):
        if i2 == -1:
            coords[index] = (k - 1, 1, 2)
        if i2 == 5:
            coords[index] = (k - 1, 3, 2)
        if j2 == -1:
            coords[index] = (k - 1, 2, 1)
        if j2 == 5:
            coords[index] = (k - 1, 2, 3)

    if (i, j) == (1, 2):
        coords.remove((k, 2, 2))
        coords.extend([(k + 1, 0, j) for j in range(5)])
    if (i, j) == (3, 2):
        coords.remove((k, 2, 2))
        coords.extend([(k + 1, 4, j) for j in range(5)])
    if (i, j) == (2, 1):
        coords.remove((k, 2, 2))
        coords.extend([(k + 1, i, 0) for i in range(5)])
    if (i, j) == (2, 3):
        coords.remove((k, 2, 2))
        coords.extend([(k + 1, i, 4) for i in range(5)])

    return coords


def nb_neighbour_bugs2(tiles, n, i, j):
    return sum(tiles[n2][i2][j2] == '#' for (n2, i2, j2) in neighbours2(n, i, j))


def next_generation2(rectiles):
    next_rectiles = {n: [['.'] * 5 for _ in range(5)] for n in range(-200, 201)}
    for n in range(-199, 200):
        for i in range(5):
            for j in range(5):
                nb = nb_neighbour_bugs2(rectiles, n, i, j)
                if rectiles[n][i][j] == '#':
                    if nb == 1:
                        next_rectiles[n][i][j] = '#'
                else:
                    if nb in (1, 2):
                        next_rectiles[n][i][j] = '#'
        next_rectiles[n][2][2] = '?'
    return next_rectiles


def count_bugs(rectiles):
    sm = 0
    for n in range(-199, 200):
        for i in range(5):
            for j in range(5):
                if rectiles[n][i][j] == '#':
                    sm += 1
    return sm


def code2(n):
    tiles = get_data(n)
    print_tiles(tiles)
    rectiles = dict()
    rectiles = {n: [['.'] * 5 for _ in range(5)] for n in range(-200, 201)}
    rectiles[0] = tiles
    for i in range(200):
        print('gen', i)
        rectiles = next_generation2(rectiles)
    for n in range(-5, 6):
        print(f'Depth {n}:')
        print_tiles(rectiles[n])
    print('2>', count_bugs(rectiles))


# code1(0)
code2(0)
