
EXAMPLES1 = (
    ('05-exemple1.txt', 5),
)

EXAMPLES2 = (
    ('05-exemple1.txt', 10),
)

INPUT =  '05-input.txt'


def read_list(fn):
    with open(fn) as f:
        return [int(s) for s in f.readlines()]


def code1(liste):
    n = 0
    ptr = 0
    while True:
        n += 1
        ptrnext = ptr + liste[ptr]
        if 0 <= ptrnext < len(liste):
            liste[ptr] += 1
            ptr = ptrnext
        else:
            return n


def code2(liste):
    n = 0
    ptr = 0
    while True:
        n += 1
        ptrnext = ptr + liste[ptr]
        if 0 <= ptrnext < len(liste):
            if liste[ptr] >= 3:
                liste[ptr] -= 1
            else:
                liste[ptr] += 1
            ptr = ptrnext
        else:
            return n


def test(n, code, examples, myinput):
    for fn, result in examples:
        data = read_list(fn)
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(read_list(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
