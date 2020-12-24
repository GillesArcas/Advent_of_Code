import re


EXEMPLE = 0
if EXEMPLE == 0:
    DATA = '24.txt'
elif EXEMPLE == 1:
    DATA = '24-exemple1.txt'
else:
    assert False


def neighbour(x, y, z, direction):
    if direction == 'e':
        return x + 1, y - 1, z
    if direction == 'se':
        return x, y - 1, z + 1
    if direction == 'sw':
        return x - 1, y, z + 1
    if direction == 'w':
        return x - 1, y + 1, z
    if direction == 'nw':
        return x, y + 1, z - 1
    if direction == 'ne':
        return x + 1, y, z - 1
    assert False, (x, y, z, direction)


WHITE, BLACK = True, False


def nb_black_neighbours(tiles, x, y, z):
    n = 0
    for direction in 'e se sw w nw ne'.split():
        neigh = neighbour(x, y, z, direction)
        if neigh in tiles:
            if tiles[neigh] == BLACK:
                n += 1
        else:
            pass  # tile white by default
    return n


def nb_black_tiles(tiles):
    return sum(tile == BLACK for tile in tiles.values())


def dilatation(tiles):
    # add all neighbours of black tiles in tiles if not already in tiles
    tiles2 = dict()
    for coord, color in tiles.items():
        tiles2[coord] = color
        if color == WHITE:
            continue
        for direction in 'e se sw w nw ne'.split():
            neigh = neighbour(*coord, direction)
            if neigh not in tiles:
                tiles2[neigh] = WHITE
    return tiles2


def splitline(line):
    return list(re.findall('(e|se|sw|w|nw|ne)', line))


def read_data():
    with open(DATA) as f:
        lines = [line.strip() for line in f.readlines()]
    return [splitline(line) for line in lines]


def code1():
    tiles = dict()
    tiles[(0, 0, 0)] = WHITE
    for directions in read_data():
        x = y = z = 0
        for direction in directions:
            x, y, z = neighbour(x, y, z, direction)
        if (x, y, z) in tiles:
            tiles[(x, y, z)] = not tiles[(x, y, z)]
        else:
            tiles[(x, y, z)] = BLACK  # WHITE flipped
    print('>', nb_black_tiles(tiles))
    return tiles


def code2(tiles):
    for day in range(1, 100 + 1):
        tiles = dilatation(tiles)
        tiles2 = dict()
        for coord, color in tiles.items():
            nb = nb_black_neighbours(tiles, *coord)
            if color == BLACK:
                if nb == 0 or nb > 2:
                    tiles2[coord] = WHITE
                else:
                    tiles2[coord] = BLACK
            else:
                if nb == 2:
                    tiles2[coord] = BLACK
                else:
                    tiles2[coord] = WHITE
        tiles = tiles2.copy()
        print('Day', day, nb_black_tiles(tiles))


tiles = code1()
code2(tiles)
