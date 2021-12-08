from collections import defaultdict


EXAMPLES1 = (
    ('08-exemple1.txt', 26),
)

EXAMPLES2 = (
    ('08-exemple2.txt', 5353),
    ('08-exemple1.txt', 61229),
)

INPUT =  '08.txt'


def read_data(fn):
    data = list()
    with open(fn) as f:
        for line in f:
            line = line.strip()
            left, right = line.split(' | ')
            data.append((left.split(), right.split()))
    return data


def code1(data):
    count = 0
    for left, right in data:
        for word in right:
            if len(word) in (2, 3, 4, 7):
                count += 1
    return count


def included(x, y):
    return all(_ in y for _ in x)


def check(len2words):
    assign = [None] * 10
    assign[1] = len2words[2][0]
    assign[7] = len2words[3][0]
    assign[4] = len2words[4][0]
    assign[8] = len2words[7][0]
    assign[3] = [x for x in len2words[5] if included(assign[1], x)][0]
    len2words[5].remove(assign[3])
    assign[9] = [x for x in len2words[6] if included(assign[3], x)][0]
    len2words[6].remove(assign[9])
    assign[5] = [x for x in len2words[5] if included(x, assign[9])][0]
    len2words[5].remove(assign[5])
    assign[2] = len2words[5][0]
    assign[0] = [x for x in len2words[6] if included(assign[1], x)][0]
    len2words[6].remove(assign[0])
    assign[6] = len2words[6][0]
    return assign


def code2(data):
    total = 0
    for left, right in data:
        left = [''.join(sorted(w)) for w in left]
        right = [''.join(sorted(w)) for w in right]
        #assert all(w in left for w in right)

        len2words = defaultdict(list)
        for word in left:
            len2words[len(word)].append(word)

        assign = check(len2words)
        #print(assign)

        digits = [assign.index(word) for word in right]
        n = int(''.join(str(_) for _ in digits))
        #print(n)
        total += n

    return total


def test(n, code, examples, myinput):
    for fn, result in examples:
        data = read_data(fn)
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
