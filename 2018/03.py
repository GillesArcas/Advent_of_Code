import re
import collections


DATA = '03.txt'


def get_data():
    data = dict()
    with open(DATA) as f:
        for line in f:
            # #1357 @ 931,293: 13x24
            match = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line)
            id, offx, offy, width, height = (int(_) for _ in match.groups())
            data[id] = (offx, offy, width, height)
    return data


def code1():
    data = get_data()
    array = collections.defaultdict(lambda: collections.defaultdict(int))
    for id, (offx, offy, width, height) in data.items():
        for x in range(offx, offx + width):
            for y in range(offy, offy + height):
                array[y][x] += 1
    n = 0
    for y in range(1000):
        for x in range(1000):
            if array[y][x] > 1:
                n += 1

    print('1>', n)


def code2():
    data = get_data()
    array = collections.defaultdict(lambda: collections.defaultdict(list))
    for id, (offx, offy, width, height) in data.items():
        for x in range(offx, offx + width):
            for y in range(offy, offy + height):
                array[y][x].append(id)

    overlap_ids = set()
    for y in range(1000):
        for x in range(1000):
            if len(array[y][x]) > 1:
                overlap_ids.update(array[y][x])

    print('2>', set(data) - overlap_ids)


code1()
code2()
