import itertools
from collections import defaultdict


EXAMPLES1 = (
    ('20-exemple1.txt', 35),
    ('20-exemple2.txt', 5326),
)

EXAMPLES2 = (
    ('20-exemple1.txt', 3351),
)

INPUT =  '20.txt'


def read_data(fn):
    with open(fn) as f:
        lookup = f.readline().strip()
        f.readline()
        dots = [line.strip() for line in f.readlines()]
        image = defaultdict(lambda: defaultdict(lambda: '.'))
        for i, line in enumerate(dots):
            for j, pixel in enumerate(line):
                image[i][j] = pixel
    return lookup, image


def valimage(image, i, j, i0, i1, j0, j1, passnum, lookup_table):
    if lookup_table[0] == '.':
        return image[i][j]
    elif passnum % 2 == 1:
        return image[i][j]
    else:
        if i0 - passnum < i < i1 + passnum and j0 - passnum < j < j1 + passnum:
            return image[i][j]
        else:
            return'#'


def lookup(image, i, j, lookup_table, i0, i1, j0, j1, passnum):
    neighbours = [valimage(image, I, J, i0, i1, j0, j1, passnum, lookup_table) for I, J in itertools.product(range(i - 1, i + 2), range(j - 1, j + 2))]
    index = int(''.join([str('.#'.index(_)) for _ in neighbours]), 2)
    return lookup_table[index]


def iteralgo(image, i0, i1, j0, j1, lookup_table, passnum):
    image2 = defaultdict(lambda: defaultdict(lambda: '.'))
    for i in range(i0 - passnum, i1 + passnum + 1):
        for j in range(j0 - passnum, j1 + passnum + 1):
            image2[i][j] = lookup(image, i, j, lookup_table, i0, i1, j0, j1, passnum)
    return image2


def dimensions(image):
    i0 = min(image)
    i1 = max(image)
    j0 = float('inf')
    j1 = -float('inf')
    for i in range(i0, i1 + 1):
        if image[i]:
            j0 = min(j0, min(image[i]))
            j1 = max(j1, max(image[i]))
    return i0, i1, j0, j1


def display(image, i0, i1, j0, j1, passnum):
    for i in range(i0 - passnum, i1 + passnum + 1):
        for j in range(j0 - passnum, j1 + passnum + 1):
            print(image[i][j], sep='', end='')
        print()


def countpixel(image):
    count = 0
    for i in image:
        for j in image[i]:
            if image[i][j] == '#':
                count += 1
    return count


def code1(data):
    lookup_table, image = data
    i0, i1, j0, j1 = dimensions(image)
    for k in range(1, 2 + 1):
        image = iteralgo(image, i0, i1, j0, j1, lookup_table, k)
    return countpixel(image)


def code2(data):
    lookup_table, image = data
    i0, i1, j0, j1 = dimensions(image)
    for k in range(1, 50 + 1):
        image = iteralgo(image, i0, i1, j0, j1, lookup_table, k)
    return countpixel(image)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
