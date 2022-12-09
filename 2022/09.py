"""
--- 2022 --- Day 9: Rope Bridge ---
"""


EXAMPLES1 = (
    ('09-exemple1.txt', 13),
)

EXAMPLES2 = (
    ('09-exemple1.txt', 1),
    ('09-exemple2.txt', 36),
)

INPUT = '09.txt'


def read_data(filename):
    data = []
    with open(filename) as f:
        for line in f:
            x, y = line.split()
            data.append((x, int(y)))
    return data


XDELTA = {'R': 1, 'L': -1, 'U': 0, 'D': 0}
YDELTA = {'R': 0, 'L': 0, 'U': -1, 'D': 1}


def update_tail(hpos, tpos):
    if tpos == hpos:
        return tpos
    else:
        hx, hy = hpos
        tx, ty = tpos
        if abs(hx - tx) <= 1 and abs(hy - ty) <= 1:
            return tpos
        else:
            if abs(hx - tx) == 2 and abs(hy - ty) <= 1:
                if hx > tx:
                    return (hx - 1, hy)
                else:
                    return (hx + 1, hy)
            elif abs(hy - ty) == 2 and abs(hx - tx) <= 1:
                if hy > ty:
                    return (hx, hy - 1)
                else:
                    return (hx, hy + 1)
            elif abs(hx - tx) == 2 and abs(hy - ty) == 2:
                if hx > tx and hy > ty:
                    return (tx + 1, ty + 1)
                elif hx > tx and hy < ty:
                    return (tx + 1, ty - 1)
                elif hx < tx and hy > ty:
                    return (tx - 1, ty + 1)
                else:
                    return (tx - 1, ty - 1)
            else:
                assert 0, (hpos, tpos)


def update_rope(pos):
    for i in range(9):
        pos[i + 1] = update_tail(pos[i], pos[i + 1])


def code1(data):
    hpos = (0, 0)
    tpos = (0, 0)
    tpos_set = set()
    tpos_set.add(tpos)
    for direction, nsteps in data:
        for _ in range(nsteps):
            x, y = hpos
            hpos = (x + XDELTA[direction], y + YDELTA[direction])
            tpos = update_tail(hpos, tpos)
            tpos_set.add(tpos)
    return len(tpos_set)


def code2(data):
    pos = [(0, 0)] * 10
    tpos_set = set()
    tpos_set.add(pos[9])
    for direction, nsteps in data:
        for _ in range(nsteps):
            x, y = pos[0]
            pos[0] = (x + XDELTA[direction], y + YDELTA[direction])
            update_rope(pos)
            tpos_set.add(pos[9])
    return len(tpos_set)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
