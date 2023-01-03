"""
--- 2016 --- Day 20: Firewall Rules ---
"""


EXAMPLES1 = (
    ('20-exemple1.txt', 3),
)

EXAMPLES2 = (
)

INPUT = '20.txt'


def read_data(filename):
    ranges = []
    with open(filename) as f:
        for onerange in f.readlines():
            ranges.append([int(x) for x in onerange.strip().split('-')])
    return sorted(ranges)


def code1(ranges):
    firstrange = ranges[0]
    for onerange in ranges[1:]:
        if onerange[0] <= firstrange[1] + 1:
            firstrange[1] = max(firstrange[1], onerange[1])
        else:
            return firstrange[1] + 1
    return None


def code2(ranges):
    new_ranges = []
    new_ranges.append(ranges[0])
    for onerange in ranges[1:]:
        if onerange[0] <= new_ranges[-1][1] + 1:
            new_ranges[-1][1] = max(new_ranges[-1][1], onerange[1])
        else:
            new_ranges.append(onerange)

    count = 0
    for range1, range2 in zip(new_ranges, new_ranges[1:]):
        count += range2[0] - range1[1] - 1

    # add ending interval (note there is no free starting interval)
    count += 4294967295 - new_ranges[-1][1]

    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
