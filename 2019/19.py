import itertools
import functools

import intcode


DATA = '19.txt'


def code1():
    with open(DATA) as f:
        strcode = f.readline().strip()
        code = intcode.parse_data(strcode)
    computer = intcode.Intcode(code)
    computer.verbose_output = False

    zone = [['.'] * 50 for _ in range(50)]
    nbeams = 0

    for x in range(50):
        for y in range(50):
            computer.reset()
            computer.run([x, y], return_output=True)
            if computer.outvalues[0] == 1:
                zone[y][x] = '#'
                nbeams += 1

    for _ in zone:
        print(''.join(_))
    print('1>', nbeams)


def code2():
    """
    hypoteses: xmin and xmax are increasing and there is no gap between xmin and xmax
    """
    with open(DATA) as f:
        strcode = f.readline().strip()
        code = intcode.parse_data(strcode)
    computer = intcode.Intcode(code)
    computer.verbose_output = False

    @functools.lru_cache(maxsize=None)
    def beam_bounds(xmin, y):
        for x in itertools.count(xmin):
            computer.reset()
            computer.run([x, y], return_output=True)
            if computer.outvalues[0] == 1:
                xmin = x
                break
        for x in itertools.count(x + 1):
            computer.reset()
            computer.run([x, y], return_output=True)
            if computer.outvalues[0] == 0:
                xmax = x - 1
                break
        return xmin, xmax

    y0 = 100
    xmin, xmax = beam_bounds(0, y0)

    for y in itertools.count(y0 + 1):
        xmin, xmax = beam_bounds(xmin, y)
        if xmax - xmin + 1 >= 100:
            computer.reset()
            computer.run([xmax - 99, y + 99], return_output=True)
            if computer.outvalues[0] == 1:
                print('2>', xmax - 99, y, (xmax - 99) * 10000 + y)
                break


code2()
