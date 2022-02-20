import functools
import operator


EXAMPLES1 = (
    ('flqrgnkx', 8108),
)

EXAMPLES2 = (
    ('flqrgnkx', 1242),
)

INPUT = 'ugkiagan'


def read_data(data):
    return data


def revslice(string, pos, length):
    liste = list()
    for p in range(pos, pos + length):
        liste.append(string[p % len(string)])
    for p in range(pos, pos + length):
        string[p % len(string)] = liste.pop()


def knot_hash(string, size=256, iterations=64):
    lengths = [ord(x) for x in string]
    lengths += [17, 31, 73, 47, 23]
    seq = list(range(size))

    pos = 0
    skip = 0
    for _ in range(iterations):
        for length in lengths:
            revslice(seq, pos, length)
            pos += (length + skip) % len(seq)
            skip += 1

    xorvalues = list()
    for k in range(0, 256, 16):
        slice16 = seq[k:k + 16]
        xorvalues.append(functools.reduce(operator.xor, slice16))

    hexvalue = ''.join(['%02x' % _ for _ in xorvalues])

    return hexvalue


def code1(data):
    count = 0
    for n in range(128):
        string = f'{data}-{n}'
        knhash = knot_hash(string)
        knhashbin = format(int(knhash, 16), '0128b')
        count += sum(_ == '1' for _ in knhashbin)
    return count


def neighbours(i, j):
    neigh = ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))
    return ((i, j) for i, j in neigh if 0 <= i < 128 and 0 <= j < 128)


def mark_region(grid, cell, seen):
    if cell not in seen:
        seen.add(cell)
        for i, j in neighbours(*cell):
            if grid[i][j] == '1':
                mark_region(grid, (i, j), seen)


def code2(data):
    grid = list()
    for n in range(128):
        string = f'{data}-{n}'
        knhash = knot_hash(string)
        grid.append(format(int(knhash, 16), '0128b'))

    count = 0
    seen = set()
    for i, line in enumerate(grid):
        for j, cell in enumerate(line):
            if cell == '1' and (i, j) not in seen:
                count += 1
                mark_region(grid, (i, j), seen)
    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
