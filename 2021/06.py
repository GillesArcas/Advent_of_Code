
EXAMPLES1 = (
    ('06-exemple1.txt', 5934),
)

EXAMPLES2 = (
    ('06-exemple1.txt', 26984457539),
)

INPUT =  '06.txt'


def read_data(fn):
    with open(fn) as f:
        return [int(n) for n in f.readline().strip().split(',')]


def code1(data):
    for day in range(80):
        more = list()
        for index, fish in enumerate(data):
            if fish == 0:
                data[index] = 6
                more.append(8)
            else:
                data[index] -= 1
        data.extend(more)
    return len(data)


def code2(data):
    count = [0] * 9
    for n in data:
        count[n] += 1

    for day in range(256):
        newcount = [0] * 9
        for days, n in enumerate(count):
            if days == 0:
                newcount[6] += n
                newcount[8] += n
            else:
                newcount[days - 1] += n
        count = newcount
    return sum(count)


def test(n, code, examples, myinput):
    for fn, result in examples:
        data = read_data(fn)
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
