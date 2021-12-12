import functools
import operator


EXAMPLES1 = (
    ((5, (3, 4, 1, 5)), 12),
)

EXAMPLES2 = (
    ((256, ''), 'a2582a3a0e66e6e86e3812dcb672a272'),
    ((256, 'AoC 2017'), '33efeb34ea91902bb2f59c9920caa6cd'),
    ((256, '1,2,3'), '3efbe78a8d82f29979031a4aa0b16a9d'),
    ((256, '1,2,4'), '63960835bcdc130f0b66d7ff4f6a5a8e'),
 )

INPUT1 = (256, (230,1,2,221,97,252,168,169,57,99,0,254,181,255,235,167))
INPUT2 = (256, '230,1,2,221,97,252,168,169,57,99,0,254,181,255,235,167')


def read_data(data):
    string = list(range(data[0]))
    lengths = data[1]
    return string, lengths


def revslice(string, pos, length):
    liste = list()
    for p in range(pos, pos + length):
        liste.append(string[p % len(string)])
    for p in range(pos, pos + length):
        string[p % len(string)] = liste.pop()


def code1(data):
    string, lengths = data
    pos = 0
    skip = 0
    for length in lengths:
        revslice(string, pos, length)
        pos += (length + skip) % len(string)
        skip += 1
    return string[0] * string[1]


def code2(data):
    string, lengths = data
    lengths = [ord(x) for x in lengths]
    lengths += [17, 31, 73, 47, 23]

    pos = 0
    skip = 0
    for count in range(64):
        for length in lengths:
            revslice(string, pos, length)
            pos += (length + skip) % len(string)
            skip += 1

    xorvalues = list()
    for k in range(0, 256, 16):
        slice16 = string[k:k + 16]
        xorvalues.append(functools.reduce(operator.xor, slice16))

    hexvalue = ''.join(['%02x' % _ for _ in xorvalues])

    return hexvalue


def test(n, code, examples, myinput):
    for fn, result in examples:
        data = read_data(fn)
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT1)
test(2, code2, EXAMPLES2, INPUT2)
