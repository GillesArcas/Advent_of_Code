import re


EXEMPLE = 0
if EXEMPLE == 0:
    DATA = '20.txt'
    SIZE = 12
    RESULT = 13983397496713
elif EXEMPLE == 1:
    DATA = '20-exemple1.txt'
    SIZE = 3
    RESULT = 20899048083289
else:
    assert False


ID, R1, R2, R3, MH, MV, D2, D1 = range(8)
TRANS = (ID, R1, R2, R3, MH, MV, D2, D1)
TRANSTR = ('ID', 'R1', 'R2', 'R3', 'MH', 'MV', 'D2', 'D1')
LAST_TRANS = D1


def apply_trans(border_tile, trans):
    # border_tile = liste des bords N, E, S, O
    dir = lambda k: border_tile[k]
    rev = lambda k: border_tile[k][::-1]
    if trans == ID:
        return border_tile
    elif trans == R1:
        return [rev(3), dir(0), rev(1), dir(2)]
    elif trans == R2:
        return [rev(2), rev(3), rev(0), rev(1)]
    elif trans == R3:
        return [dir(1), rev(2), dir(3), rev(0)]
    elif trans == MH:
        return [dir(2), rev(1), dir(0), rev(3)]
    elif trans == MV:
        return [rev(0), dir(3), rev(2), dir(1)]
    elif trans == D1:
        return [dir(3), dir(2), dir(1), dir(0)]
    elif trans == D2:
        return [rev(1), rev(0), rev(3), rev(2)]


def read_data():
    raw_tiles = dict()
    with open(DATA) as f:
        lines = [line.strip() for line in f.readlines()]
    for n in range(len(lines) // 12 + 1):
        line = lines[n * 12]
        m = re.match(r'Tile (\d+):', line)
        tileid = int(m.group(1))
        tile = lines[n * 12 + 1:n * 12 + 1 + 10]
        raw_tiles[tileid] = tile
    return raw_tiles


def tile_borders(raw_tile):
    raw_tile_t = list(zip(*raw_tile))
    return [raw_tile[0], ''.join(raw_tile_t[9]), raw_tile[9], ''.join(raw_tile_t[0])]


def backtrack(border_tiles, id_tiles):
    """
    border_tiles: dict id:liste_des_bords
    id_tiles: liste des id
    """
    array = [[None for j in range(SIZE)] for i in range(SIZE)]
    i = 0
    j = 0
    while i <= SIZE - 1:
        if array[i][j] is None:
            array[i][j] = [next_tile(array, i, j), ID]
        if ((i == 0 or ok_nord(border_tiles, id_tiles, array[i][j], array[i - 1][j])) and
            (j == 0 or ok_ouest(border_tiles, id_tiles, array[i][j], array[i][j - 1]))):
            if j == SIZE - 1:
                i += 1
                j = 0
            else:
                j += 1
        else:
            tile, trans = array[i][j]
            if trans < LAST_TRANS:
                array[i][j][1] += 1
            elif tile < SIZE * SIZE - 1 and (nexttile := next_tile(array, i, j, after=tile)):
                array[i][j] = [nexttile, ID]
            else:
                i, j = backward(i, j, array)

    print('FOUND')
    print(array)
    n1 = id_tiles[array[0][0][0]]
    n2 = id_tiles[array[0][SIZE - 1][0]]
    n3 = id_tiles[array[SIZE - 1][0][0]]
    n4 = id_tiles[array[SIZE - 1][SIZE - 1][0]]
    print(n1, n2)
    print(n3, n4)
    print(n1 * n2 * n3 * n4)
    return n1 * n2 * n3 * n4, array


def print_array(array, id_tiles):
    for i2 in range(SIZE):
        for j2 in range(SIZE):
            if array[i2][j2] is None:
                print('-------', end=' ')
            else:
                print('%d,%02d' % (id_tiles[array[i2][j2][0]], array[i2][j2][1]), end=' ')
        print()
    print()


def backward(i, j, array):
    if i == j == 0:
        print('NOT FOUND')
        exit()

    array[i][j] = None
    if j > 0:
        j -= 1
    else:
        i -= 1
        j = SIZE - 1

    tile, trans = array[i][j]
    if trans < LAST_TRANS:
        array[i][j][1] += 1
    # elif tile < SIZE * SIZE - 1:
    #     array[i][j] = [tile + 1, ID]
    elif tile < SIZE * SIZE - 1 and (nexttile := next_tile(array, i, j, after=tile)):
        array[i][j] = [nexttile, ID]
    else:
        i, j = backward(i, j, array)
    return i, j


def next_tile(array, i, j, after=-1):
    """
    plus petit de ceux qui n'y sont pas
    """
    y_sont = set()
    for i2 in range(SIZE):
        for j2 in range(SIZE):
            if i2 < i or j2 < j:
                y_sont.add(array[i2][j2][0])
            else:
                cand = [x for x in range(SIZE * SIZE) if x not in y_sont and x > after]
                if cand:
                    return min(cand)
                else:
                    return None


def ok_nord(border_tiles, id_tiles, tile, tile_nord):
    index_tile1, trans1 = tile
    border_tile1 = border_tiles[id_tiles[index_tile1]]
    border_tile1 = apply_trans(border_tile1, trans1)

    index_tile2, trans2 = tile_nord
    border_tile2 = border_tiles[id_tiles[index_tile2]]
    border_tile2 = apply_trans(border_tile2, trans2)

    return border_tile1[0] == border_tile2[2]


def ok_ouest(border_tiles, id_tiles, tile, tile_nord):
    index_tile1, trans1 = tile
    border_tile1 = border_tiles[id_tiles[index_tile1]]
    border_tile1 = apply_trans(border_tile1, trans1)

    index_tile2, trans2 = tile_nord
    border_tile2 = border_tiles[id_tiles[index_tile2]]
    border_tile2 = apply_trans(border_tile2, trans2)

    return border_tile1[3] == border_tile2[1]


def code1():
    raw_tiles = read_data()
    border_tiles = {tileid:tile_borders(raw_tile) for tileid, raw_tile in raw_tiles.items()}
    id_tiles = list(border_tiles)
    assert id_tiles == list(raw_tiles)

    result, array = backtrack(border_tiles, id_tiles)
    assert result == RESULT
    restore_picture(raw_tiles, id_tiles, array)


def reduce_tile(tile):
    return [line[1:-1] for line in tile[1:-1]]


def restore_picture(raw_tiles, id_tiles, array):
    reduce_tiles = {idtile:reduce_tile(tile) for idtile, tile in raw_tiles.items()}
    print(reduce_tiles)
    print()
    print(array)
    print()
    parray = list()
    for line in array:
        larray = list()
        for idx, trans in line:
            red_tile = apply_trans_tile(reduce_tiles[id_tiles[idx]], trans)
            larray.append(red_tile)
        parray.append(larray)

    print(parray)
    print()
    with open('20-picture.txt', 'wt') as f:
        for line in parray:
            for lines in zip(*line):
                print(''.join(lines), file=f)


def apply_trans_tile(tile, trans):
    if trans == ID:
        return tile
    elif trans == R1:
        return rotate_tile(tile)
    elif trans == R2:
        return rotate_tile(rotate_tile(tile))
    elif trans == R3:
        return rotate_tile(rotate_tile(rotate_tile(tile)))
    elif trans == MH:
        return hflip_tile(tile)
    elif trans == MV:
        return vflip_tile(tile)
    elif trans == D1:
        return transpose_tile(tile)
    elif trans == D2:
        return antitranspose_tile(tile)


def rotate_tile(raw_tile):
    return [''.join(_) for _ in zip(*raw_tile[::-1])]


def hflip_tile(raw_tile):
    return raw_tile[::-1]


def vflip_tile(raw_tile):
    raw_tile_t = list(zip(*raw_tile))[::-1]
    raw_tile2 = [''.join(_) for _ in zip(*raw_tile_t)]
    return raw_tile2


def transpose_tile(raw_tile):
    return [''.join(_) for _ in zip(*raw_tile)]


def antitranspose_tile(raw_tile):
    return hflip_tile(rotate_tile(raw_tile))


def code2():
    # code1 doit avoir été fait avant avec le même paramètre pour générer le
    # fichier 20-picture.txt
    with open('20-picture.txt') as f:
        picture = [_.strip() for _ in f.readlines()]
    for trans in (D2,): # TRANS:
        print(TRANSTR[trans])
        picture2 = apply_trans_tile(picture[:], trans)
        print('nb#', sum(sum(c == '#' for c in line) for line in picture2))
        # for line in picture2:
        #     print(line)
        # continue
        cherche_serpent(picture2)


PAT1 = '..................#.'
PAT2 = '#....##....##....###'
PAT3 = '.#..#..#..#..#..#...'


def cherche_serpent(picture):
    nfound = 0
    for i in range(len(picture) - 4):
        for j in range(len(picture[0]) - len(PAT1) - 1):
            if check_serpent_ij(picture, i, j):
                nfound += 1
    if nfound:
        print('Found:', nfound)
        ntot = sum(sum(c == '#' for c in line) for line in picture)
        print('>', ntot - nfound * 15)


def check_serpent_ij(picture, i, j):
    PAT = (PAT1, PAT2, PAT3)
    for i2 in range(3):
        for j2 in range(len(PAT1)):
            if PAT[i2][j2] == '#':
                if picture[i + i2][j + j2] == '#':
                    pass
                else:
                    return False
    return True


#code1()
code2()
