from collections import Counter


EXAMPLES1 = (
    ('14-exemple1.txt', 1588),
)

EXAMPLES2 = (
    ('14-exemple1.txt', None),
)

INPUT =  '14.txt'


def read_data(fn):
    insertions = dict()
    with open(fn) as f:
        template = f.readline().strip()
        f.readline()
        for line in f:
            line = line.strip()
            insertions[line[:2]] = line[6]
    return template, insertions


def apply(template, insertions):
    new = list()
    for k in range(len(template) - 1):
        new.append(template[k])
        if template[k:k + 2] in insertions:
            new.append(insertions[template[k:k + 2]])
    new.append(template[-1])
    return ''.join(new)


def code1(data):
    template, insertions = data
    for k in range(10):
        template = apply(template, insertions)
    counter = Counter(template)
    return max(counter.values()) - min(counter.values())


def applycount(elemcount, paircount, insertions):
    paircount2 = Counter()
    for pair in paircount:
        if pair in insertions:
            elemcount[insertions[pair]] += paircount[pair]
            paircount2[pair[0] + insertions[pair]] += paircount[pair]
            paircount2[insertions[pair] + pair[1]] += paircount[pair]
        else:
            paircoint2[pair] = paircount[pair]
    return paircount2


def xapplycount(data, nb):
    template, insertions = data
    elemcount = Counter(template)
    paircount = Counter([template[k:k + 2] for k in range(len(template) - 1)])
    for k in range(1, nb + 1):
        paircount = applycount(elemcount, paircount, insertions)
        if k <= 5:
            # compare with naive solution
            template = apply(template, insertions)
            print('step', k, template, elemcount, len(template), sum(elemcount.values()))
    return max(elemcount.values()) - min(elemcount.values())


def code1(data):
    return xapplycount(data, 10)


def code2(data):
    return xapplycount(data, 40)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
