import re
import random
import pickle
import itertools
from collections import defaultdict


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '24.txt'


# -- Code interpreter and equivalence with python snippet ---------------------


# -- Reading and parsing


def read_data(fn):
    with open(fn) as f:
        lines = f.readlines()
    return parse_data(lines)


def parse_data(lines):
    code = list()
    for line in lines:
        line = re.sub(' *#.*', '', line)
        op, o1, *o2 = line.split()
        if not o2:
            o2 = None
        else:
            o2 = o2[0]
        try:
            o2 = int(o2)
        except:
            pass
        code.append((op, o1, o2))

    return code


# -- Interpreter


def getvalue(variables, x):
    if x in variables:
        return variables[x]
    else:
        return x


def setvalue(variables, x, v):
    if x in variables:
        variables[x] = v
    else:
        assert 0


def interpreter(code, data, var=None):
    """
    data: list of integers
    """
    data = data[:]

    if var is None:
        variables = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    else:
        variables = var

    for op, o1, o2 in code:
        if op == 'inp':
            setvalue(variables, o1, data.pop(0))
        elif op == 'add':
            setvalue(variables, o1, getvalue(variables, o1) + getvalue(variables, o2))
        elif op == 'mul':
            setvalue(variables, o1, getvalue(variables, o1) * getvalue(variables, o2))
        elif op == 'div':
            setvalue(variables, o1, getvalue(variables, o1) // getvalue(variables, o2))
        elif op == 'mod':
            setvalue(variables, o1, getvalue(variables, o1) % getvalue(variables, o2))
        elif op == 'eql':
            setvalue(variables, o1, int(getvalue(variables, o1) == getvalue(variables, o2)))

    return variables


# -- Calculus


# calculus with original code


def monad_full(code, digits14: list):
    variables = interpreter(code, digits14)
    return getvalue(variables, 'z')


# calculus using digit snippet


DCODE = """\
inp w
mul x 0
add x z
mod x 26
div z a
add x b
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y c
mul y x
add z y\
"""


CONST = (
    (1, 10, 0),
    (1, 12, 6),
    (1, 13, 4),
    (1, 13, 2),
    (1, 14, 9),
    (26, -2, 1),
    (1, 11, 10),
    (26, -15, 6),
    (26, -10, 4),
    (1, 10, 6),
    (26, -10, 3),
    (26, -4, 9),
    (26, -1, 15),
    (26, -1, 5),
)


def monad_snippet(digits14: list):
    dcode = parse_data(DCODE.splitlines())
    variables = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    for digit, const in zip(digits14, CONST):
        variables['a'] = const[0]
        variables['b'] = const[1]
        variables['c'] = const[2]
        variables = interpreter(dcode, [digit], variables)
    return variables['z']


# calculus using python


def digitmonad(w, z, a, b, c):
    if w == z % 26 + b:
        return z // a
    else:
        return z // a * 26 + w + c


def digitmonad_litteral(w, z, a, b, c):
    w = w
    x = z
    x = x % 26
    x = x + b
    x = 0 if x == w else 1
    y = 25
    y = y * x
    y = y + 1
    z = z // a
    z = z * y
    y = w
    y = y + c
    y = y * x
    z = z + y
    return z


def monad_run(digits14: list):
    z = 0
    for digit, const in zip(digits14, CONST):
        z = digitmonad(digit, z, *const)
    return z


def rankmonad(rank, w, z):
    a, b, c = CONST[rank]
    if w == z % 26 + b:
        return z // a
    else:
        return z // a * 26 + w + c


# -- Checking


def check_direct_calculus():
    monadcode = read_data('24.txt')

    for _ in range(1_000):
        nz = random_non_zero()
        z1 = monad_full(monadcode, nz)
        z2 = monad_snippet(nz)
        z3 = monad_run(nz)

        if not (z1 == z2 == z3):
            return False

    return True


# -- Helpers


def valid_model_number(code, data):
    # data = [int(c) for c in str(n)]
    variables = interpreter(code, data)
    return getvalue(variables, 'z') == 0


def random_non_zero():
    digits = random.choices(list(range(1, 10)), k=14)
    return digits


def strzsol(zsol):
    if zsol:
        return f'{len(zsol)} entre {min(zsol)} et {max(zsol)}'
    else:
        return None


# -- Generic search -----------------------------------------------------------


def monad_invimage(rank, zfrom, zto):
    """
    Return all z from zfrom which image by rankmonad is in zto.
    """
    wz = set()
    for w in range(1, 10):
        for z in zfrom:
            zr = rankmonad(rank, w, z)
            if zr in zto:
                wz.add(z)
    return wz


# -- OK


def monad_image(rank, zfrom):
    """
    Return the image of zfrom by rankmonad.
    """
    wz = set()
    for w in range(1, 10):
        for z in zfrom:
            zr = rankmonad(rank, w, z)
            wz.add(zr)
    return wz


def image_z():
    """
    Compute all z reachable from {0} for each rank.
    """
    imgz = [None] * 14
    for rank in range(14):
        zfrom = {0} if (rank == 0) else imgz[rank - 1]
        wz = monad_image(rank, zfrom)
        imgz[rank] = wz
        print('Rank %2d %8d' % (rank, len(wz)))
    return imgz


def backward_wz(imgz):
    """
    Compute all pairs (w, z) starting from z=0 and leading to 0.
    """
    possible = defaultdict(set)
    target = {0}

    for rank in range(13, -1, -1):
        for w, z in itertools.product(range(1, 10), {0} if (rank == 0) else imgz[rank-1]):
            z2 = rankmonad(rank, w, z)
            if z2 in target:
                possible[rank].add((w, z))
        target = {z for _, z in possible[rank]}

    return possible


def generate_all(possible):
    """
    Trace recursively all solutions.
    """
    for w, z in possible[0]:
        generate_rec(0, possible, w, z, [w])


def generate_rec(rank, possible, w, z, nz):
    if len(nz) == 14:
        print('>', ''.join([str(n) for n in nz]), monad_run(nz))
    else:
        zr = rankmonad(rank, w, z)
        pos = {wz for wz in possible[rank + 1] if wz[1] == zr}
        for w, z in pos:
            generate_rec(rank + 1, possible, w, z, nz + [w])


def generate_rnd(possible):
    """
    Generate random solutions one at a time. Simpler, for reference.
    """
    nz = list()
    w, z = random.choice(list(possible[0]))
    nz.append(w)

    for rank in range(13):
        zr = rankmonad(rank, w, z)
        pos = {wz for wz in possible[rank + 1] if wz[1] == zr}
        if not pos:
            return
        w, z = random.choice(list(pos))
        nz.append(w)

    assert len(nz) == 14
    print('>', ''.join([str(n) for n in nz]), monad_run(nz))


# -- Main ---------------------------------------------------------------------


def code1(monad):
    imgz = image_z()
    wz = backward_wz(imgz)
    generate_all(wz)

    with open('24z.dat', 'wb') as f:
        pickle.dump(imgz, f)
    with open('24wz.dat', 'wb') as f:
        pickle.dump(wz, f)

    return None


def code2(monad):
    return None


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


assert check_direct_calculus()
monadcode = read_data('24.txt')
code1(monadcode)
# test(1, code1, EXAMPLES1, INPUT)
# test(2, code2, EXAMPLES2, INPUT)
