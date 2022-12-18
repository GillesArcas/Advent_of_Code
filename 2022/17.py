"""
--- 2022 --- Day 17: Pyroclastic Flow ---
"""


import itertools


EXAMPLES1 = (
    ('17-exemple1.txt', 3068),
)

EXAMPLES2 = (
    ('17-exemple1.txt', 1514285714288),
)

INPUT = '17.txt'


SHAPE1 = """\
####\
""".splitlines()

SHAPE2 = """\
.#.
###
.#.\
""".splitlines()

SHAPE3 = """\
..#
..#
###\
""".splitlines()

SHAPE4 = """\
#
#
#
#\
""".splitlines()

SHAPE5 = """\
##
##\
""".splitlines()

SHAPES = (SHAPE1, SHAPE2, SHAPE3, SHAPE4, SHAPE5)


def read_data(filename):
    with open(filename) as f:
        data = f.read().strip()
    return data


def fit_shape(chamber, shape, xshape, yshape):
    if xshape < 0 or xshape + len(shape[0]) - 1 > 6 or yshape + len(shape) - 1 >= len(chamber) - 1:
        return False

    for y, line1 in enumerate(shape):
        line2 = chamber[yshape + y]
        for x, char in enumerate(line1):
            if char == '#':
                if line2[xshape + x] != '.':
                    return False
    return True


def set_shape(chamber, shape, xshape, yshape):
    for y, line1 in enumerate(shape):
        line2 = chamber[yshape + y]
        line = list(line2)
        for x, char in enumerate(line1):
            if char == '#':
                line[xshape + x] = char
        chamber[yshape + y] = ''.join(line)


def reset_shape(chamber, shape, xshape, yshape):
    for y, line1 in enumerate(shape):
        line2 = chamber[yshape + y]
        line = list(line2)
        for x, char in enumerate(line1):
            if char == '#':
                line[xshape + x] = '.'
        chamber[yshape + y] = ''.join(line)


def code1(data):
    shifts = itertools.cycle(data)
    chamber = ['-------']
    for irock in range(2022):
        shape = SHAPES[irock % 5]
        chamber = ['.' * 7] * (3 + len(shape)) + chamber
        xshape = 2
        yshape = 0

        while True:
            reset_shape(chamber, shape, xshape, yshape)

            xshape2 = xshape + (- 1 if next(shifts) == '<' else 1)
            if fit_shape(chamber, shape, xshape2, yshape):
                xshape = xshape2

            yshape2 = yshape + 1
            if fit_shape(chamber, shape, xshape, yshape2):
                yshape = yshape2
                stop = False
            else:
                stop = True

            set_shape(chamber, shape, xshape, yshape)
            if chamber[0] == '.......':
                del chamber[0]
                yshape -= 1

            # for line in chamber[:20]:
                # print(line)
            # print('=====================')
            # x = input()
            # if x == 'q':
                # exit(1)
            # if x == 't':
                # breakpoint()

            if stop:
                break

    return len(chamber) - 1


def code2(data):
    deltas = []
    length = 0
    shifts = itertools.cycle(data)
    chamber = ['-------']
    for irock in range(10000):
        shape = SHAPES[irock % 5]
        chamber = ['.' * 7] * (3 + len(shape)) + chamber
        xshape = 2
        yshape = 0

        while True:
            reset_shape(chamber, shape, xshape, yshape)

            xshape2 = xshape + (- 1 if next(shifts) == '<' else 1)
            if fit_shape(chamber, shape, xshape2, yshape):
                xshape = xshape2

            yshape2 = yshape + 1
            if fit_shape(chamber, shape, xshape, yshape2):
                yshape = yshape2
                stop = False
            else:
                stop = True

            set_shape(chamber, shape, xshape, yshape)
            if chamber[0] == '.......':
                del chamber[0]
                yshape -= 1

            if stop:
                deltas.append(len(chamber) - 1 - length)
                length = len(chamber) - 1
                break

    deltas = ''.join([str(_) for _ in deltas])
    minlength = 100
    for index in range(len(deltas) - minlength):
        sequence = deltas[index:index + minlength]
        if sequence in deltas[index + minlength:]:
            indexrep = index + minlength + deltas[index + minlength:].index(sequence)
            break

    n = 1000000000000
    lenoff = index
    lenrep = indexrep - index
    seqoff = deltas[:index]
    seqrep = deltas[index:indexrep]
    highoff = sum(int(_) for _ in seqoff)
    highrep = sum(int(_) for _ in seqrep)
    lenrest = (n - lenoff) % lenrep
    highrest = sum(int(_) for _ in seqrep[:lenrest])

    return highoff + highrep * ((n - lenoff) // lenrep) + highrest


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
