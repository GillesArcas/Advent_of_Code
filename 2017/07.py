import re


EXAMPLES1 = (
    ('07-exemple1.txt', 'tknk'),
)

EXAMPLES2 = (
    ('07-exemple1.txt', 60),
)

INPUT =  '07-input.txt'


def read_data(fn):
    tower = dict()
    with open(fn) as f:
        for line in f:
            line = line.strip()
            match = re.match(r'(\w+) \((\d+)\)', line)
            name = match.group(1)
            weight = int(match.group(2))
            if match := re.search('-> (.*)', line):
                nexts = match.group(1).split(', ')
            else:
                nexts = []
            prev = []
            # print(name, weight, nexts)
            tower[name] = (name, weight, nexts, prev)

    # restore prev link
    for name, node in tower.items():
        for succ in node[2]:
            tower[succ][3].append(name)

    return tower


def code1(tower):
    for name, node in tower.items():
        if not node[3]:
            return name


def fixweights(tower, nexts, weights):
    print(nexts, weights)
    minw = min(weights)
    maxw = max(weights)
    if weights.count(minw) == 1:
        node = tower[nexts[weights.index(minw)]]
        print(node[0], node[1], minw, maxw, maxw - minw, node[1] + (maxw - minw))
        return node[1] + (maxw - minw)
    else:
        node = tower[nexts[weights.index(maxw)]]
        print(node[0], node[1], minw, maxw, maxw - minw, node[1] - (maxw - minw))
        return node[1] - (maxw - minw)


def code2span(tower, node):
    nexts = tower[node][2]
    if not nexts:
        return tower[node][1]
    else:
        weights = [code2span(tower, node2) for node2 in nexts]
        if weights.count(weights[0]) == len(weights):
            return tower[node][1] + sum(weights)
        else:
            return fixweights(tower, nexts, weights)


def code2span(tower, node):
    """
    give the lowest solution
    """
    nexts = tower[node][2]
    if not nexts:
        return tower[node][1]
    else:
        weights = [code2span(tower, node2) for node2 in nexts]
        if weights.count(weights[0]) == len(weights):
            return tower[node][1] + sum(weights)
        else:
            return fixweights(tower, nexts, weights)


class ScanAbort(Exception):
    pass


def code2spanrec(tower, node):
    nexts = tower[node][2]
    if not nexts:
        return tower[node][1]
    else:
        weights = [code2spanrec(tower, node2) for node2 in nexts]
        if weights.count(weights[0]) == len(weights):
            return tower[node][1] + sum(weights)
        else:
            raise ScanAbort(fixweights(tower, nexts, weights))


def code2span(tower, node):
    """
    give the highest solution
    """
    try:
        return code2spanrec(tower, node)
    except ScanAbort as e:
        return e.args[0]


def code2test(tower, node):
    """
    trace les noeuds non équilibrés
    """
    nexts = tower[node][2]
    if not nexts:
        pass
    else:
        weights = [code2test(tower, node2) for node2 in nexts]
        if weights.count(weights[0]) == len(weights):
            pass
        else:
            print(tower[node][0], nexts, weights)


def code2(tower):
    root = code1(tower)
    return code2span(tower, root)


def test(n, code, examples, myinput):
    for fn, result in examples:
        data = read_data(fn)
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
