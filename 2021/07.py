
EXAMPLES1 = (
    ('07-exemple1.txt', 37),
)

EXAMPLES2 = (
    ('07-exemple1.txt', 168),
)

INPUT =  '07.txt'


def read_data(fn):
    with open(fn) as f:
        return [int(n) for n in f.readline().strip().split(',')]


def code1(data):
    # best position not restricted to positions in data
    mincost = float('inf')
    for n in range(min(data), max(data) + 1):
        cost = sum(abs(n - p) for p in data)
        mincost = min(mincost, cost)
    return mincost


def code2(data):
    # best position not restricted to positions in data
    mincost = float('inf')
    for n in range(min(data), max(data) + 1):
        cost = sum((abs(n - p) * (abs(n - p) + 1)) // 2 for p in data)
        mincost = min(mincost, cost)
    return mincost


def test(n, code, examples, myinput):
    for fn, result in examples:
        data = read_data(fn)
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
