"""
--- Day 18: Lavaduct Lagoon ---
"""


import re
import math
from collections import defaultdict
from itertools import pairwise
from PIL import Image, ImageDraw


EXAMPLES1 = (
    ('18-exemple1.txt', 62),
)

EXAMPLES2 = (
    ('18-exemple1.txt', 952408144115),
)

INPUT = '18.txt'


def read_data(filename):
    data = []
    with open(filename) as f:
        for line in f:
            match = re.match(r'([UDLR]) (\d+) \((#[a-f0-9]{6})\)', line)
            data.append((match[1], int(match[2]), match[3]))
    return data


def valid_coord(i, j, grid):
    return 0 <= i < len(grid) and 0 <= j < len(grid[0])


def neighbours(i, j, grid):
    neighs = []
    for i2, j2 in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
        if valid_coord(i2, j2, grid):
            neighs.append((i2, j2))
    return neighs


def code1(data):
    deltai = {'U': -1, 'D': 1, 'L': 0, 'R': 0}
    deltaj = {'U': 0, 'D': 0, 'L': -1, 'R': 1}

    i, j = 0, 0
    mini, minj = float('inf'), float('inf')
    maxi, maxj = -float('inf'), -float('inf')
    for direction, steps, color in data:
        for _ in range(steps):
            i, j = i + deltai[direction], j + deltaj[direction]
            mini = min(mini, i)
            maxi = max(maxi, i)
            minj = min(minj, j)
            maxj = max(maxj, j)

    wi = maxi - mini + 1
    wj = maxj - minj + 1
    i0 = -mini
    j0 = -minj

    grid = [['.'] * wj for _ in range(wi)]
    i, j = i0, j0
    grid[i][j] = '#'
    for direction, steps, color in data:
        for _ in range(steps):
            i, j = i + deltai[direction], j + deltaj[direction]
            grid[i][j] = '#'

    # initialize outside points with points from side of grid
    stack = set()
    for j, char in enumerate(grid[0]):
        if char == '.':
            stack.add((0, j))
    for j, char in enumerate(grid[-1]):
        if char == '.':
            stack.add((len(grid) - 1, j))
    for i, line in enumerate(grid):
        if line[0] == '.':
            stack.add((i, 0))
    for i, line in enumerate(grid):
        if line[-1] == '.':
            stack.add((i, len(line) - 1))

    # fill outside of shape
    while stack:
        i, j = stack.pop()
        for i2, j2 in neighbours(i, j, grid):
            if grid[i2][j2] == '.':
                grid[i2][j2] = 'X'
                stack.add((i2, j2))

    count = 0
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char in '.#':
                count += 1

    return count


def display_rectangles(ilist, jlist, corners, rectangles, fillshape=False):
    imin = rectangles[0][0]['i1']
    jmin = rectangles[0][0]['j1']
    imax = rectangles[-1][-1]['i2']
    jmax = rectangles[-1][-1]['j2']
    w = 1000
    h = 1000
    ia = (h - 1) / (imax - imin)
    ib = -ia * imin + 5
    ja = (w - 1) / (jmax - jmin)
    jb = -ja * jmin + 5

    img = Image.new("RGB", (w+10, h+10))
    imgdraw = ImageDraw.Draw(img)

    x1 = int(round(ja * jmin + jb))
    x2 = int(round(ja * jmax + jb))
    for i in ilist:
        y = int(round(ia * i + ib))
        line = [(x1, y), (x2, y)]
        imgdraw.line(line, fill='#333333', width=0)
    y1 = int(round(ia * imin + ib))
    y2 = int(round(ia * imax + ib))
    for j in jlist:
        x = int(round(ja * j + jb))
        line = [(x, y1), (x, y2)]
        imgdraw.line(line, fill='#333333', width=0)

    for i, row in enumerate(rectangles):
        for j, rect in enumerate(row):
            if rect['N']:
                x1 = int(round(ja * rect['j1'] + jb))
                x2 = int(round(ja * rect['j2'] + jb))
                y1 = int(round(ia * rect['i1'] + ib))
                line = [(x1, y1), (x2, y1)]
                imgdraw.line(line, fill='#ff0000', width=0)
            if rect['S']:
                x1 = int(round(ja * rect['j1'] + jb))
                x2 = int(round(ja * rect['j2'] + jb))
                y2 = int(round(ia * rect['i2'] + ib))
                line = [(x1, y2), (x2, y2)]
                imgdraw.line(line, fill='#00ff00', width=0)
            if rect['W']:
                x1 = int(round(ja * rect['j1'] + jb))
                y1 = int(round(ia * rect['i1'] + ib))
                y2 = int(round(ia * rect['i2'] + ib))
                line = [(x1, y1), (x1, y2)]
                imgdraw.line(line, fill='#0000ff', width=0)
            if rect['E']:
                x2 = int(round(ja * rect['j2'] + jb))
                y1 = int(round(ia * rect['i1'] + ib))
                y2 = int(round(ia * rect['i2'] + ib))
                line = [(x2, y1), (x2, y2)]
                imgdraw.line(line, fill='#ffffff', width=0)

    for i, j in corners:
        x = int(round(ja * j + jb))
        y = int(round(ia * i + ib))
        line = [(x, y), (x, y)]
        imgdraw.line(line, fill='#00ff00', width=0)
    i, j = corners[0]
    x = int(round(ja * j + jb))
    y = int(round(ia * i + ib))
    box = [(x - 5, y - 5), (x + 5, y + 5)]
    imgdraw.ellipse(box, fill='#984318', width=3)

    if fillshape:
        for i, row in enumerate(rectangles):
            for j, rect in enumerate(row):
                if rect['IN']:
                    print('IN', i, j)
                    x1 = int(round(ja * rect['j1'] + jb))
                    x2 = int(round(ja * rect['j2'] + jb))
                    y1 = int(round(ia * rect['i1'] + ib))
                    y2 = int(round(ia * rect['i2'] + ib))

                    imgdraw.rectangle((x1, y1, x2, y2), fill='#123456', outline='#123456', width=1)

    img.show()


"""
Part 2 is solved using a grid of rectangles rather than a grid of pixels. The
rectangles are constructed from all the coordinates given by the contour. After
initialization of the rectangles, the contour is followed and the side of the 
rectangles are labelled as belonging to the contour. A simple search enables
after that to labelled each rectangle if it belongs to the shape. 

For reference, a more direct approach seems to use the shoelace formula.
"""


def code(moves):
    deltai = {'U': -1, 'D': 1, 'L': 0, 'R': 0}
    deltaj = {'U': 0, 'D': 0, 'L': -1, 'R': 1}

    # list of corners
    corners = []
    i, j = 0, 0
    corners.append((i, j))
    for direction, steps, _ in moves:
        i, j = i + steps * deltai[direction], j + steps * deltaj[direction]
        corners.append((i, j))
    assert corners[0] == corners[-1]

    # lists of involved coordinates
    ilist = list(sorted({i for i, j in corners}))
    jlist = list(sorted({j for i, j in corners}))

    # init rectangles, each element describes a rectangle [i1, j1, i2, j2, N, W, S, E, IN]
    # with N = 0/1 if north side belongs to border, same for W, S, E, and with IN = 0/1
    # if rectangle is inside contour
    rectangles = []
    for i, (i1, i2) in enumerate(pairwise(ilist)):
        row = []
        for j, (j1, j2) in enumerate(pairwise(jlist)):
            row.append(dict(i1=i1, j1=j1, i2=i2, j2=j2, N=0, W=0, S=0, E=0, IN=0))
        rectangles.append(row)

    # links from corners to rectangles with NW: coordinates of rectangle north west of corner, etc
    corner_to_rect = {}
    for i, j in corners:
        corner_to_rect[i, j] = dict(NW=(None, None), NE=(None, None), SW=(None, None), SE=(None, None))
    for i, (i1, i2) in enumerate(pairwise(ilist)):
        for j, (j1, j2) in enumerate(pairwise(jlist)):
            if (i1, j1) in corners:
                corner_to_rect[i1, j1]['SE'] = i, j
            if (i1, j2) in corners:
                corner_to_rect[i1, j2]['SW'] = i, j
            if (i2, j1) in corners:
                corner_to_rect[i2, j1]['NE'] = i, j
            if (i2, j2) in corners:
                corner_to_rect[i2, j2]['NW'] = i, j

    # add border description to rectangles
    i1, j1 = 0, 0
    for direction, steps, _ in moves:
        i2, j2 = i1 + steps * deltai[direction], j1 + steps * deltaj[direction]

        if direction == 'U':
            I1, J1 = corner_to_rect[i1, j1]['NW']
            I2, J2 = corner_to_rect[i2, j2]['SW']
            if I1 is not None:
                assert J1 == J2 and I1 >= I2, (I1, J1, I2, J2)
                for i in range(I2, I1 + 1):
                    rectangles[i][J1]['E'] = 1
            I1, J1 = corner_to_rect[i1, j1]['NE']
            I2, J2 = corner_to_rect[i2, j2]['SE']
            if I1 is not None:
                assert J1 == J2 and I1 >= I2, (I1, J1, I2, J2)
                for i in range(I2, I1 + 1):
                    rectangles[i][J1]['W'] = 1

        if direction == 'D':
            I1, J1 = corner_to_rect[i1, j1]['SW']
            I2, J2 = corner_to_rect[i2, j2]['NW']
            if I1 is not None:
                assert J1 == J2
                for i in range(I1, I2 + 1):
                    rectangles[i][J1]['E'] = 1
            I1, J1 = corner_to_rect[i1, j1]['SE']
            I2, J2 = corner_to_rect[i2, j2]['NE']
            if I1 is not None:
                assert J1 == J2
                for i in range(I1, I2 + 1):
                    rectangles[i][J1]['W'] = 1

        if direction == 'R':
            I1, J1 = corner_to_rect[i1, j1]['NE']
            I2, J2 = corner_to_rect[i2, j2]['NW']
            if I1 is not None:
                assert I1 == I2 and J2 >= J1, (I1, J1, I2, J2)
                for j in range(J1, J2 + 1):
                    rectangles[I1][j]['S'] = 1
            I1, J1 = corner_to_rect[i1, j1]['SE']
            I2, J2 = corner_to_rect[i2, j2]['SW']
            if I1 is not None:
                assert I1 == I2 and J2 >= J1, (I1, J1, I2, J2)
                for j in range(J1, J2 + 1):
                    rectangles[I1][j]['N'] = 1

        if direction == 'L':
            I1, J1 = corner_to_rect[i1, j1]['NW']
            I2, J2 = corner_to_rect[i2, j2]['NE']
            if I1 is not None and I2 is not None:
                assert I1 == I2 and J1 >= J2, (I1, J1, I2, J2)
                for j in range(J2, J1 + 1):
                    rectangles[I1][j]['S'] = 1
            I1, J1 = corner_to_rect[i1, j1]['SW']
            I2, J2 = corner_to_rect[i2, j2]['SE']
            if I1 is not None and I2 is not None:
                assert I1 == I2 and J1 >= J2, (I1, J1, I2, J2)
                for j in range(J2, J1 + 1):
                    rectangles[I1][j]['N'] = 1

        i1, j1 = i2, j2

    # draw
    # display_rectangles(ilist, jlist, corners, rectangles)

    # find one inner rectangle (top row, N and W border)
    for j, rect in enumerate(rectangles[0]):
        if rect['N'] and rect['W']:
            i_in, j_in = 0, j
            break

    # fill shape (assume connexity)
    stack = []
    stack.append((i_in, j_in))
    while stack:
        i, j = stack.pop()
        if not rectangles[i][j]['IN']:
            rectangles[i][j]['IN'] = 1
            if i > 0 and not rectangles[i][j]['N']:
                stack.append((i - 1, j))
            if i + 1 < len(rectangles) and not rectangles[i][j]['S']:
                stack.append((i + 1, j))
            if j > 0 and not rectangles[i][j]['W']:
                stack.append((i, j - 1))
            if j + 1 < len(rectangles[0]) and not rectangles[i][j]['E']:
                stack.append((i, j + 1))

    # draw
    # display_rectangles(ilist, jlist, corners, rectangles, fillshape=True)

    # count
    count = 0
    east_south_corners = defaultdict(list)
    for i, row in enumerate(rectangles):
        for j, rect in enumerate(row):
            if rect['IN']:
                count += (rect['i2'] - rect['i1']) * (rect['j2'] - rect['j1'])
                if rect['S']:
                    count += rect['j2'] - rect['j1']
                    east_south_corners[rect['i2'], rect['j1']].append(('S', (i, j)))
                    east_south_corners[rect['i2'], rect['j2']].append(('S', (i, j)))
                if rect['E']:
                    count += rect['i2'] - rect['i1']
                    east_south_corners[rect['i1'], rect['j2']].append(('E', (i, j)))
                    east_south_corners[rect['i2'], rect['j2']].append(('E', (i, j)))
    p = sum(len(_) == 2 and _[0][0] != _[1][0] and _[0][1] == _[1][1]for _ in east_south_corners.values())
    q = sum(len(_) == 2 and _[0][0] != _[1][0] and _[0][1] != _[1][1]for _ in east_south_corners.values())
    count = count + p - q

    return count


def code2(data):
    for index, (_, _, color) in enumerate(data):
        direction = 'RDLU'[int(color[-1])]
        steps = int(color[1:-1], 16)
        data[index] = direction, steps, color

    return code(data)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
