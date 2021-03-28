import itertools


DATA = '01.txt'


def code1():
    with open(DATA) as f:
        data = [int(line) for line in f.readlines()]
    print('1>', sum(data))


def code2():
    with open(DATA) as f:
        data = [int(line) for line in f.readlines()]
    values = set()
    value = 0
    for delta in itertools.cycle(data):
        value += delta
        if value in values:
            print('2>', value)
            break
        else:
            values.add(value)


code1()
code2()
