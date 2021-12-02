import re


EXAMPLES1 = (
    ('02-exemple1.txt', 150),
)

EXAMPLES2 = (
    ('02-exemple1.txt', 900),
)

INPUT =  '02.txt'


def read_list(fn):
    """
    return the list of coordinate deltas (x, z)
    """
    liste = list()
    with open(fn) as f:
        for line in f:
            if match := re.match(r'forward (\d+)', line):
                liste.append((int(match.group(1)), 0))
            elif match := re.match(r'down (\d+)', line):
                liste.append((0, int(match.group(1))))
            elif match := re.match(r'up (\d+)', line):
                liste.append((0, -int(match.group(1))))
            else:
                assert 0, line
    return liste


def code1(liste):
    dx, dz = zip(*liste)
    return sum(dx) * sum(dz)


def code2(liste):
    dx, dz, aim = 0, 0, 0
    for x, z in liste:
        if z == 0:
            # forward
            dx += x
            dz += aim * x
        else:
            aim += z
    return dx * dz


def test(n, code, examples, myinput):
    for fn, result in examples:
        data = read_list(fn)
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(read_list(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
