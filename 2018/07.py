import re
import collections


DATA = '07.txt'


def get_data():
    succ = collections.defaultdict(list)
    pred = collections.defaultdict(list)
    with open(DATA) as f:
        for line in f:
            match = re.match(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.', line)
            succ[match.group(1)].append(match.group(2))
            pred[match.group(2)].append(match.group(1))

    roots = [node for node in succ if not pred[node]]

    return succ, pred, roots


def code1():
    succ, pred, roots = get_data()

    done = list()
    available = sorted(roots)

    while available:
        nextnode = available.pop(0)
        done.append(nextnode)
        available += [node for node in succ[nextnode] if all(_ in done for _ in pred[node])]
        available = sorted(available)

    print('1>', ''.join(done))


def code2():
    print('2>', 0)


code1()
code2()
