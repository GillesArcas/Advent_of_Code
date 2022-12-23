"""
--- 2022 --- Day 22: Monkey Map ---
"""


import re


# coordinates x,y of faces in data
COORD_EX = {1: (2, 0), 2: (0, 1), 3: (1, 1), 4: (2, 1), 5: (2, 2), 6: (3, 2)}

COORD_IN = {1: (1, 0), 2: (2, 0), 3: (1, 1), 4: (0, 2), 5: (1, 2), 6: (0, 3)}

FACES_EX = {
    '1N': '2N-', '1E': '6E-', '1S': '4N+', '1W': '3N+',
    '2N': '1N-', '2E': '3W+', '2S': '5S-', '2W': '6S-',
    '3N': '1W+', '3E': '4W+', '3S': '5W-', '3W': '2E+',
    '4N': '1S+', '4E': '6N-', '4S': '5N+', '4W': '3E+',
    '5N': '4S+', '5E': '6W+', '5S': '2S-', '5W': '3S-',
    '6N': '4E-', '6E': '1E-', '6S': '2W-', '6W': '5E+'
}

FACES_IN = {
    '1N': '6W+', '1E': '2W+', '1S': '3N+', '1W': '4W-',
    '2N': '6S+', '2E': '5E-', '2S': '3E+', '2W': '1E+',
    '3N': '1S+', '3E': '2S+', '3S': '5N+', '3W': '4N+',
    '4N': '3W+', '4E': '5W+', '4S': '6N+', '4W': '1W-',
    '5N': '3S+', '5E': '2E-', '5S': '6E+', '5W': '4E+',
    '6N': '4S+', '6E': '5S+', '6S': '2N+', '6W': '1N+'
}


EXAMPLES1 = (
    (('22-exemple1.txt', 4, COORD_EX, FACES_EX), 6032),
)

EXAMPLES2 = (
    (('22-exemple1.txt', 4, COORD_EX, FACES_EX), 5031),
)

INPUT = ('22.txt', 50, COORD_IN, FACES_IN)


def read_data(_):
    filename, dim, coords, faces = _

    with open(filename) as f:
        lines = [_.strip('\n') for _ in f.readlines()]

    maxi = max(len(line) for line in lines[:-2])

    grid = []
    for line in lines[:-2]:
        grid.append(list(line.ljust(maxi)))

    xstart = next(x for x, c in enumerate(grid[0]) if c == '.')

    steps = re.split(r'([LR])',lines[-1].strip())
    steps = [int(_) if _.isdigit() else _ for _ in steps]

    return dim, coords, faces, grid, steps, xstart


def print_grid(grid):
    for line in grid:
        print(''.join(line))
    print()


def move(grid, x, y, facing, nsteps):
    _ = 0
    xprev, yprev = x, y
    while _ < nsteps:
        _ += 1
        if grid[y][x] in '.<>v^':
            xprev, yprev = x, y
        if facing == '>':
            x = (x + 1) % len(grid[0])
        elif facing == '<':
            x = (x - 1) % len(grid[0])
        elif facing == 'v':
            y = (y + 1) % len(grid)
        elif facing == '^':
            y = (y - 1) % len(grid)

        if grid[y][x] == '.':
            pass
        elif grid[y][x] == '#':
            return xprev, yprev
        else:
            _ -= 1
    return x, y


def turn(facing, lr):
    return ('v<^>' if lr == 'R' else '^>v<')['>v<^'.index(facing)]


def code1(data):
    dim, coords, faces, grid, steps, xstart = data
    ystart = 0
    facing = '>'

    x, y = xstart, ystart
    for _ in steps:
        if isinstance(_, int):
            x, y = move(grid, x, y, facing, _)
        else:
            facing = turn(facing, _)

    return 1000 * (y + 1) + 4 * (x + 1) + '>v<^'.index(facing)


def inv(facing):
    return 'NESW'['SWNE'.index(facing)]


def extract_faces(grid, coords, dim):
    faces = {}
    for facenum, (x, y) in coords.items():
        faces[facenum] = [line[x * dim:(x + 1)* dim] for line in grid[y * dim:(y + 1) * dim]]
    return faces


def merge_faces(faces, coords, dim):
    xmax = max(_[0] for _ in coords.values())
    ymax = max(_[1] for _ in coords.values())

    grid = [[' '] * ((xmax + 1) * dim) for _ in range((ymax + 1) * dim)]
    for index, face in enumerate(faces, 1):
        coord = coords[index]
        for y in range(0, dim):
            line = grid[coord[1] * dim + y]
            line[coord[0] * dim:coord[0] * dim + dim] = faces[index][y]
    return grid


def update_x(dim, side, sideprev, xprev, yprev, sign):
    if side in (sideprev, inv(sideprev)):
        if sign == '+':
            x = xprev
        else:
            x = dim - 1 - xprev
    else:
        if sign == '+':
            x = yprev
        else:
            x = dim - 1 - yprev
    return x


def update_y(dim, side, sideprev, xprev, yprev, sign):
    if side in (sideprev, inv(sideprev)):
        if sign == '+':
            y = yprev
        else:
            y = dim - 1 - yprev
    else:
        if sign == '+':
            y = xprev
        else:
            y = dim - 1 - xprev
    return y


def change_face(facetrans, dim, fprev, xprev, yprev, sideprev):
    trans = facetrans[str(fprev) + sideprev]
    face, side, sign = list(trans)
    face = int(face)
    facing = 'v<^>'['NESW'.index(side)]

    if side == 'N':
        x = update_x(dim, side, sideprev, xprev, yprev, sign)
        y = 0
    elif side == 'E':
        x = dim - 1
        y = update_y(dim, side, sideprev, xprev, yprev, sign)
    elif side == 'S':
        x = update_x(dim, side, sideprev, xprev, yprev, sign)
        y = dim - 1
    else:
        x = 0
        y = update_y(dim, side, sideprev, xprev, yprev, sign)

    return face, x, y, facing


def move2(facetrans, faces, dim, face, x, y, facing, nsteps):
    # face: number of face 1..6 (idem fprev)
    # facing: direction of cursor ^<v> (idem facingprev)
    # side: side of face 'N', 'E', 'S', 'W' (idem sideprev)
    # side determined by facing when overflow

    for _ in range(nsteps):
        fprev, xprev, yprev, facingprev = face, x, y, facing

        if facing == '>':
            if x < dim - 1:
                x += 1
            else:
                # comes from E
                face, x, y, facing = change_face(facetrans, dim, fprev, xprev, yprev, sideprev='E')
        elif facing == '<':
            if x > 0:
                x -= 1
            else:
                # comes from W
                face, x, y, facing = change_face(facetrans, dim, fprev, xprev, yprev, sideprev='W')
        elif facing == 'v':
            if y < dim - 1:
                y += 1
            else:
                # comes from S
                face, x, y, facing = change_face(facetrans, dim, fprev, xprev, yprev, sideprev='S')
        elif facing == '^':
            if y > 0:
                y -= 1
            else:
                # comes from N
                face, x, y, facing = change_face(facetrans, dim, fprev, xprev, yprev, sideprev='N')

        if faces[face][y][x] != '#':  # may be '.' or debug characters '^>v<'
            faces[face][y][x] = facing
        else:
            return fprev, xprev, yprev, facingprev

    return face, x, y, facing


def code2(data):
    dim, coords, facetrans, grid, steps, xstart = data
    faces = extract_faces(grid, coords, dim)

    fstart = 1
    xstart = 0
    ystart = 0
    facing = '>'

    f, x, y = fstart, xstart, ystart
    for _ in steps:
        if isinstance(_, int):
            f, x, y, facing = move2(facetrans, faces, dim, f, x, y, facing, _)
        else:
            facing = turn(facing, _)

    grid = merge_faces(faces, coords, dim)
    # print_grid(grid)

    coord = coords[f]
    x = coord[0] * dim + x
    y = coord[1] * dim + y
    return 1000 * (y + 1) + 4 * (x + 1) + '>v<^'.index(facing)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
