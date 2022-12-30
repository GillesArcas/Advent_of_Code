"""
--- 2016 --- Day 6: Signals and Noise ---
"""


from collections import Counter


EXAMPLES1 = (
    ('06-exemple1.txt', 'easter'),
)

EXAMPLES2 = (
    ('06-exemple1.txt', 'advent'),
)

INPUT = '06.txt'


def read_data(filename):
    with open(filename) as f:
        return [_.strip() for _ in f.readlines()]


def code1(data):
    message = []
    columns = [list(_) for _ in zip(*data)]
    for column in columns:
        counter = Counter(column)
        message.append(counter.most_common(1)[0][0])
    return ''.join(message)


def code2(data):
    message = []
    columns = [list(_) for _ in zip(*data)]
    for column in columns:
        counter = Counter(column)
        message.append(counter.most_common()[-1][0])
    return ''.join(message)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
