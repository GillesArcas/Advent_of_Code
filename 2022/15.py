"""
--- 2022 --- Day 15: Beacon Exclusion Zone ---
"""


import re


EXAMPLES1 = (
    (('15-exemple1.txt', 10, 20), 26),
)

EXAMPLES2 = (
    (('15-exemple1.txt', 10, 20), 56000011),
)

INPUT = ('15.txt', 2000000, 4000000)


PAT = r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)'


def read_data(_):
    filename, yline, maxcoord = _
    with open(filename) as f:
        reports = [[int(_) for _ in _] for _ in re.findall(PAT, f.read())]
    return reports, yline, maxcoord


def update_line(yline, line, xs, ys, xb, yb):
    d = abs(xs - xb) + abs(ys - yb)
    ymin = ys - d
    ymax = ys + d
    if yline < ymin or yline > ymax:
        xminline = None
        xmaxline = None
    elif yline < ys:
        xminline = xs - (yline - ymin)
        xmaxline = xs + (yline - ymin)
    elif yline > ys:
        xminline = xs - (ymax - yline)
        xmaxline = xs + (ymax - yline)
    else:
        assert 0

    if xminline:
        for x in range(xminline, xmaxline + 1):
            if x in line:
                pass
            else:
                line[x] = '#'
        if yb == yline:
            line[xb] = 'B'


def trace_sensors(reports, sensors):
    xming = float('inf')
    xmaxg = float('-inf')
    yming = float('inf')
    ymaxg = float('-inf')
    for xs, ys, xb, yb in reports:
        d = abs(xs - xb) + abs(ys - yb)
        xming = min(xming, xs - d)
        xmaxg = max(xmaxg, xs + d)
        yming = min(yming, ys - d)
        ymaxg = max(ymaxg, ys + d)

    grid = {y: {x: '.' for x in range(xming, xmaxg + 1)} for y in range(yming, ymaxg + 1)}

    for i in sensors:
        xs, ys, xb, yb = reports[i]
        d = abs(xs - xb) + abs(ys - yb)
        ymin = ys - d
        ymax = ys + d
        for y in range(ymin, ymax + 1):
            if y < ys:
                for x in range(xs - (y - ymin), xs + (y - ymin) + 1):
                    grid[y][x] = '#'
            else:
                for x in range(xs - (ymax - y), xs + (ymax - y) + 1):
                    grid[y][x] = '#'

    for i in sensors:
        xs, ys, xb, yb = reports[i]
        grid[ys][xs] = 'S'
        grid[yb][xb] = 'B'

    for y in range(yming, ymaxg + 1):
        print(''.join([grid[y][x] for x in range(xming, xmaxg + 1)]))
    print()


def code1(data):
    reports, yline, _ = data
    line = {}
    for xs, ys, xb, yb in reports:
        update_line(yline, line, xs, ys, xb, yb)
    return sum(_ == '#' for _ in line.values())


def on_border(xs, ys, xb, yb, x, y):
    """
    True if distance from source to beacon equal to distance from source to tested point
    """
    db = abs(xs - xb) + abs(ys - yb)
    d = abs(xs - x) + abs(ys - y)
    return db == d


def condition(reports, couple1, couple2, x, y):
    """
    True if point x, y touches the source zones on each side
    """
    cond1 = (on_border(*reports[couple1[0]], x, y - 1) and
             on_border(*reports[couple1[1]], x, y + 1))
    cond2 = (on_border(*reports[couple1[1]], x, y - 1) and
             on_border(*reports[couple1[0]], x, y + 1))

    cond3 = (on_border(*reports[couple2[0]], x, y + 1) and
             on_border(*reports[couple2[1]], x, y - 1))
    cond4 = (on_border(*reports[couple2[1]], x, y + 1) and
             on_border(*reports[couple2[0]], x, y - 1))

    return (cond1 or cond2) and (cond3 or cond4)



def code2(data):
    """
    Find all pairs of source which zones are separated by diagonals of 1 pixel
    wide. The position is at the intersection of two diagonals. Seems to work
    by chance on the example. However, there is only one set of sources for the
    input.
    """
    reports, _, maxcoord = data

    offsets = []
    for xs, ys, xb, yb in reports:
        d = abs(xs - xb) + abs(ys - yb)
        offsets.append((xs + ys - d, xs + ys + d, -xs + ys - d, -xs + ys + d))

    catch1 = []
    catch2 = []
    for report1, (a11, a12, a13, a14) in enumerate(offsets):
        for report2, (a21, a22, a23, a24) in enumerate(offsets):
            if report1 == report2:
                continue
            if a21 - a12 == 2:
                catch1.append((tuple(sorted((report1, report2))), (a12 + a21) // 2))
            if a23 - a14 == 2:
                catch2.append((tuple(sorted((report1, report2))), (a14 + a23) // 2))

    for couple1, offset1 in catch1:
        for couple2, offset2 in catch2:
            if couple1 == couple2:
                continue
            x = (offset1 - offset2) // 2
            y = -x + offset1
            if not (0 <= x <= maxcoord and 0 <= y <= maxcoord):
                continue

            if condition(reports, couple1, couple2, x, y):
                return 4000000 * x + y

    return None


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
