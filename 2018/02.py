import collections
import itertools


DATA = '02.txt'


def code1():
    with open(DATA) as f:
        data = [line.strip() for line in f.readlines()]
    n2 = 0
    n3 = 0
    for s in data:
        counter = collections.Counter(s)
        if any(n == 2 for n in counter.values()):
            n2 += 1
        if any(n == 3 for n in counter.values()):
            n3 += 1

    print('1>', n2 * n3)


def code2():
    with open(DATA) as f:
        data = [line.strip() for line in f.readlines()]
    for id1, id2 in itertools.combinations(data, 2):
        if sum(c1 != c2 for c1, c2 in zip(id1, id2)) == 1:
            print('2>', ''.join((c1 for c1, c2 in zip(id1, id2) if c1 == c2)))


code1()
code2()
