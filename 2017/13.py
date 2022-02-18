import re
import itertools


EXAMPLES1 = (
    ('13-exemple1.txt', 24),
)

EXAMPLES2 = (
    ('13-exemple1.txt', 10),
)

INPUT = '13.txt'


def read_data(fn):
    layers = dict()
    with open(fn) as f:
        for line in f:
            match = re.match(r'(\d+): (\d+)', line)
            layers[int(match.group(1))] = int(match.group(2))
    return layers


def scanners_pos(layers):
    last = max(layers)

    # positions and orientations of scanners in layers
    scanners = [0] * (last + 1)
    directions = [1] * (last + 1)

    yield scanners
    while 1:
        scanners = scanners[:]
        for n in range(last + 1):
            if n in layers:  # layers[n] > 0:
                scanners[n] += directions[n]
                if scanners[n] == 0:
                    directions[n] = 1
                if scanners[n] == layers[n] - 1:
                    directions[n] = -1
        # print(t, scanners)
        yield scanners


def display(layers, scanners, pos):
    for iline in range(max(layers.values())):
        line = [None] * len(scanners)
        for j in range(len(scanners)):
            if iline == 0:
                if j in layers:
                    if scanners[j] == iline:
                        if pos == j:
                            line[j] = '(S)'
                        else:
                            line[j] = '[S]'
                    else:
                        if pos == j:
                            line[j] = '( )'
                        else:
                            line[j] = '[ ]'
                else:
                    if pos == j:
                        line[j] = '(.)'
                    else:
                        line[j] = '...'
            else:
                if j in layers:
                    if iline >= layers[j]:
                        line[j] = '   '
                    elif scanners[j] == iline:
                        line[j] = '[S]'
                    else:
                        line[j] = '[ ]'
                else:
                    line[j] = '   '
        print(' '.join(line))
    print('---')


def cross_scanners(layers, scanners, scannerspos, trace=False):
    last = max(layers)
    severity = 0
    caught = False
    for t in range(0, last + 1):
        pos = t
        if trace:
            print(f'Picosecond {t}:')
            display(layers, scanners, pos)
        if pos in layers and scanners[pos] == 0:
            severity += pos * layers.get(pos, 0)
            caught = True
        scanners = next(scannerspos)
        if trace:
            display(layers, scanners, pos)
    return severity, caught


def code1(data):
    layers = data
    last = max(layers)
    scannerspos = scanners_pos(layers)
    scanners = next(scannerspos)
    return cross_scanners(layers, scanners, scannerspos)[0]


def periode(data):
    # Period 24504480
    layers = data
    last = max(layers)
    scannerspos = scanners_pos(layers)
    scanners = next(scannerspos)
    for delta in itertools.count(1):
        if delta % 1000 == 0:
            print(delta)
        scanners = next(scannerspos)
        if all(scanners[x] == 0 for x in layers):
            return delta


def caught(layers, scanners_list):
    return any(scanners_list[t][t] == 0 for t in layers)


def code2(data):
    layers = data
    last = max(layers)
    scannerspos = scanners_pos(layers)
    scanners_list = list()
    for _ in range(last + 1):
        scanners_list.append(next(scannerspos))

    for delta in itertools.count():
        if caught(layers, scanners_list):
            scanners_list.pop(0)
            scanners_list.append(next(scannerspos))
        else:
            return delta


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
