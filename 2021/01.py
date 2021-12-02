
EXAMPLES1 = (
    ('01-exemple1.txt', 7),
)

EXAMPLES2 = (
    ('01-exemple1.txt', 5),
)

INPUT =  '01.txt'


def read_list(fn):
    liste = list()
    with open(fn) as f:
        for line in f:
            liste.append(int(line))
    return liste


def code1(liste):
    res = 0
    for x, y in zip(liste, liste[1:]):
        if x < y:
            res += 1
    return res


def code2(liste):
    return code1([a + b + c for a, b, c in zip(liste, liste[1:], liste[2:])])


def test(n, code, examples, myinput):
    for fn, result in examples:
        data = read_list(fn)
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(read_list(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
