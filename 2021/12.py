from collections import defaultdict, Counter


EXAMPLES1 = (
    ('12-exemple1.txt', 10),
    ('12-exemple2.txt', 19),
    ('12-exemple3.txt', 226),
)

EXAMPLES2 = (
    ('12-exemple1.txt', 36),
    ('12-exemple2.txt', 103),
    ('12-exemple3.txt', 3509),
)

INPUT =  '12.txt'


def read_data(fn):
    data = defaultdict(list)
    with open(fn) as f:
        for line in f:
            x, y = line.strip().split('-')
            data[x].append(y)
            data[y].append(x)
    return data


def possible1(node, path):
    if node == node.upper():
        return True
    else:
        return node not in path


def possible2(node, path):
    if node == node.upper():
        return True
    elif node in ('start', 'end') and node in path:
        return False
    elif node not in path:
        return True
    else:
        counter = Counter([x for x in path if x.lower() == x])
        return 2 not in counter.values()


def search(data, possible):
    paths = list()
    paths.append(['start'])
    finished = list()
    while paths:
        path0 = paths.pop()
        for node in data[path0[-1]]:
            path = path0[:]
            if not possible(node, path):
                pass
            else:
                path.append(node)
                if node == 'end':
                    finished.append(path)
                else:
                    paths.append(path)
    return len(finished)


def code1(data):
    return search(data, possible1)


def code2(data):
    return search(data, possible2)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
